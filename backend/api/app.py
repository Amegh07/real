"""
API Layer (Phase 6)
-------------------
Exposes simulation data via a REST API for the React frontend.
Built with FastAPI.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import time

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
                # Print to console as usual
                engine._print_tick_summary()
                
                if engine.max_ticks and engine.tick_number >= engine.max_ticks:
                    engine.is_running = False
                    break
                    
                time.sleep(engine.tick_delay)
        except Exception as e:
            logger.error(f"Simulation engine crashed: {e}")
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


app = FastAPI(title="Reality Simulator API", lifespan=lifespan)

# Allow React app (which usually runs on 3000 or 5173) to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────

@app.get("/api/world")
def get_world():
    if not engine:
        return {"error": "Engine not ready"}
    return engine.world_state.get_snapshot()

@app.get("/api/agents")
def get_agents():
    if not engine:
        return {"error": "Engine not ready"}
    return engine.agent_manager.get_all_snapshots()

@app.get("/api/events")
def get_events(limit: int = 50):
    if not engine:
        return {"error": "Engine not ready"}
    return {"events": engine.event_bus.get_recent_events(limit)}

@app.get("/api/status")
def get_status():
    if not engine:
        return {"running": False}
    return {
        "running": engine.is_running,
        "tick": engine.tick_number,
    }

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
                logger.error(f"Simulation engine crashed: {e}")
                engine.is_running = False

        run_thread = threading.Thread(target=run_sim, daemon=True)
        run_thread.start()
        
    return {"status": "resumed"}
