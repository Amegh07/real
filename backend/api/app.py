"""
API Layer (Phase 7)
-------------------
Exposes simulation data via a REST API for the React frontend.
Phase 7 adds: economy history, job market, agent detail, and world stats.
Built with FastAPI.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import threading
import time
import statistics

from config import SIMULATION_CONFIG
from simulation.engine import SimulationEngine
from utils.logger import get_logger, configure_logging

logger = get_logger(__name__)

# Global instances
engine = None
run_thread = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, run_thread
    configure_logging(SIMULATION_CONFIG.get("log_level", "INFO"))
    
    logger.info("Initializing SimulationEngine...")
    engine = SimulationEngine(SIMULATION_CONFIG)
    engine.setup()
    
    logger.info("Starting background simulation thread...")
    engine.is_running = True
    
    def run_sim():
        try:
            while engine.is_running:
                engine.tick()
                engine._print_tick_summary()
                
                if engine.max_ticks and engine.tick_number >= engine.max_ticks:
                    engine.is_running = False
                    break
                    
                time.sleep(engine.tick_delay)
        except Exception as e:
            logger.error(f"Simulation engine crashed: {e}", exc_info=True)
            engine.is_running = False

    run_thread = threading.Thread(target=run_sim, daemon=True)
    run_thread.start()
    
    yield
    
    logger.info("Shutting down simulation...")
    if engine:
        engine.is_running = False
        engine._print_final_summary()
    if run_thread:
        run_thread.join(timeout=2.0)


app = FastAPI(title="Reality Simulator API", version="7.0", lifespan=lifespan)

# Allow React app to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────
# Helper: compute world aggregate stats
# ─────────────────────────────────────────────────────────

def _compute_world_stats(agents: list) -> dict:
    """Compute aggregate statistics across all agents."""
    if not agents:
        return {}
    
    happiness_vals = [a.happiness for a in agents]
    hunger_vals    = [a.hunger for a in agents]
    energy_vals    = [a.energy for a in agents]
    money_vals     = [a.money for a in agents]
    
    # Gini coefficient for wealth inequality (0=equal, 1=total inequality)
    def gini(values):
        if not values or sum(values) == 0:
            return 0.0
        sv = sorted(v for v in values if v >= 0)
        n = len(sv)
        cumsum = 0
        for i, v in enumerate(sv):
            cumsum += (2 * (i + 1) - n - 1) * v
        return round(cumsum / (n * sum(sv)), 4)

    top_earner = max(agents, key=lambda a: a.money)
    alerts = sum(1 for a in agents if a.hunger < 15 or a.energy < 15 or a.happiness < 15)
    
    return {
        "avg_happiness":   round(statistics.mean(happiness_vals), 1),
        "avg_hunger":      round(statistics.mean(hunger_vals), 1),
        "avg_energy":      round(statistics.mean(energy_vals), 1),
        "avg_money":       round(statistics.mean(money_vals), 2),
        "wealth_gini":     gini(money_vals),
        "top_earner":      top_earner.name,
        "top_earner_cash": round(top_earner.money, 2),
        "agents_in_crisis": alerts,
    }


# ─────────────────────────────────────────────────────────
# Core Endpoints
# ─────────────────────────────────────────────────────────

@app.get("/api/world")
def get_world():
    if not engine:
        return {"error": "Engine not ready"}
    snap = engine.world_state.get_snapshot()
    agents = engine.agent_manager.get_all_agents()
    snap["stats"] = _compute_world_stats(agents)
    snap["economy"]["population"] = len(agents)
    snap["economy"]["employed"]   = engine.economy._employment_count()
    return snap


@app.get("/api/agents")
def get_agents():
    if not engine:
        return {"error": "Engine not ready"}
    return engine.agent_manager.get_all_snapshots()


@app.get("/api/agents/{agent_id}")
def get_agent_detail(agent_id: str):
    """Full agent detail including memory log and relationships."""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not ready")
    agent = engine.agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    snap = agent.get_snapshot()
    snap["relationships"] = engine.agent_manager.rel_graph.get_snapshot(agent_id)
    return snap


@app.get("/api/events")
def get_events(limit: int = 50):
    if not engine:
        return {"error": "Engine not ready"}
    return {"events": engine.event_bus.get_recent_events(limit)}


@app.get("/api/status")
def get_status():
    if not engine:
        return {"running": False, "tick": 0}
    agents = engine.agent_manager.get_all_agents()
    return {
        "running":    engine.is_running,
        "tick":       engine.tick_number,
        "day":        engine.world_state.day,
        "time_of_day": engine.world_state.time_of_day,
        "weather":    engine.world_state.weather,
        "population": len(agents),
    }


# ─────────────────────────────────────────────────────────
# Phase 7: New Endpoints
# ─────────────────────────────────────────────────────────

@app.get("/api/economy/history")
def get_economy_history(limit: int = 100):
    """Returns the last N ticks of economy data for charts."""
    if not engine:
        return {"history": []}
    history = list(engine.economy_history)
    return {"history": history[-limit:]}


@app.get("/api/jobs")
def get_jobs():
    """Returns the current job market: slots, filled, wages, descriptions."""
    if not engine:
        return {"jobs": []}
    from economy.economy import JOB_REGISTRY
    eco = engine.economy
    jobs = []
    for name, data in JOB_REGISTRY.items():
        filled = len(eco.job_assignments.get(name, []))
        slots  = data["slots"] if data["slots"] < 999 else 99  # cap "unlimited" for display
        jobs.append({
            "name":         name,
            "filled":       filled,
            "slots":        slots,
            "wage":         round(data["wage"] * eco.inflation_rate, 2),
            "base_wage":    data["wage"],
            "happiness_bonus": data["happiness_bonus"],
            "energy_cost":  data["energy_cost"],
            "description":  data["description"],
            "fill_rate":    round(filled / max(slots, 1), 2),
        })
    return {"jobs": jobs}


# ─────────────────────────────────────────────────────────
# Simulation Control
# ─────────────────────────────────────────────────────────

@app.post("/api/control/pause")
def pause():
    if engine:
        engine.is_running = False
    return {"status": "paused"}


@app.post("/api/control/resume")
def resume():
    global run_thread
    if engine and not engine.is_running:
        engine.is_running = True

        def run_sim():
            try:
                while engine.is_running:
                    engine.tick()
                    engine._print_tick_summary()
                    if engine.max_ticks and engine.tick_number >= engine.max_ticks:
                        break
                    time.sleep(engine.tick_delay)
            except Exception as e:
                logger.error(f"Simulation engine crashed: {e}", exc_info=True)
                engine.is_running = False

        run_thread = threading.Thread(target=run_sim, daemon=True)
        run_thread.start()

    return {"status": "resumed"}


@app.post("/api/control/speed")
def set_speed(tps: float = 1.0):
    """Set the tick delay. tps = ticks per second. Range: 0.1–10."""
    if engine:
        engine.tick_delay = round(max(0.1, min(10.0, 1.0 / tps)), 3)
    return {"tick_delay": engine.tick_delay if engine else None}
