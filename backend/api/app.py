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
import os

from config import SIMULATION_CONFIG
from simulation.engine import GodTierEngine
from utils.logger import get_logger, configure_logging
from ontology.dimensions import FEATURE_SPEC_TEMPLATE, get_master_dimensions_snapshot

logger = get_logger(__name__)

# Global instances
engine = None
run_thread = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, run_thread
    configure_logging(SIMULATION_CONFIG.get("log_level", "INFO"))
    
    logger.info("Initializing GodTierEngine...")
    config = SIMULATION_CONFIG.copy()
    config["use_persistence"] = False  # Disable in server mode to avoid SQLite thread issues
    engine = GodTierEngine(config)
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
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",") if os.environ.get("ALLOWED_ORIGINS") else ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
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
        return round(cumsum / (n * sum(sv)), 4) if n > 0 else 0.0

    top_earner = max(agents, key=lambda a: a.money) if agents else None
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
    snap["dimensions"] = engine.world_state.get_dimensional_snapshot(agents)
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
    limit = min(max(1, limit), 500)  # Cap between 1 and 500
    return {"events": engine.event_bus.get_recent_causal(limit)}


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


@app.get("/api/ontology")
def get_ontology():
    if not engine:
        return {
            "dimensions": get_master_dimensions_snapshot(),
            "feature_template": {
                "required_sections": FEATURE_SPEC_TEMPLATE.required_sections,
                "taxonomy_axes": FEATURE_SPEC_TEMPLATE.taxonomy_axes,
                "constraints": FEATURE_SPEC_TEMPLATE.constraints,
            },
        }

    agents = engine.agent_manager.get_all_agents()
    return {
        "dimensions": get_master_dimensions_snapshot(),
        "feature_template": {
            "required_sections": FEATURE_SPEC_TEMPLATE.required_sections,
            "taxonomy_axes": FEATURE_SPEC_TEMPLATE.taxonomy_axes,
            "constraints": FEATURE_SPEC_TEMPLATE.constraints,
        },
        "world_dimensions": engine.world_state.get_dimensional_snapshot(agents),
    }


@app.get("/api/features")
def get_features():
    if not engine:
        return {"features": []}
    return {"features": engine.feature_registry.list_features()}


@app.get("/api/ontology/all")
def get_all_ontology_features():
    """Get all features from the complete ontology."""
    from ontology import (
        get_feature_count,
        get_cognitive_feature_count,
        get_psychological_feature_count,
        get_social_feature_count,
        get_economic_feature_count,
        get_political_feature_count,
        get_remaining_feature_count,
        get_final_feature_count,
        get_missing_feature_count,
        get_additional_feature_count,
        _EXTENDED_COUNT,
    )
    from ontology.biological_features import get_all_feature_ids as get_bio_ids
    from ontology.cognitive_features import get_all_cognitive_feature_ids
    from ontology.psychological_features import get_all_psychological_feature_ids
    from ontology.social_features import get_all_social_feature_ids
    from ontology.economic_features import get_all_economic_feature_ids
    from ontology.political_features import get_all_political_feature_ids
    from ontology.remaining_features import get_all_remaining_feature_ids
    from ontology.complete_features import FINAL_FEATURES
    from ontology.missing_features import MISSING_FEATURES
    from ontology.additional_missing_features import ADDITIONAL_FEATURES
    from ontology.extended_features import EXTENDED_FEATURES
    
    return {
        "summary": {
            "total_features": (
                get_feature_count() + 
                get_cognitive_feature_count() + 
                get_psychological_feature_count() +
                get_social_feature_count() +
                get_economic_feature_count() +
                get_political_feature_count() +
                get_remaining_feature_count() +
                get_final_feature_count() +
                get_missing_feature_count() +
                get_additional_feature_count() +
                _EXTENDED_COUNT
            ),
            "biological": get_feature_count(),
            "cognitive": get_cognitive_feature_count(),
            "psychological": get_psychological_feature_count(),
            "social": get_social_feature_count(),
            "economic": get_economic_feature_count(),
            "political": get_political_feature_count(),
            "remaining": get_remaining_feature_count(),
            "extended": _EXTENDED_COUNT,
            "complete": get_final_feature_count(),
            "missing": get_missing_feature_count(),
            "additional": get_additional_feature_count(),
        },
        "sections": {
            "A_biological": get_bio_ids()[:100],
            "B_cognitive": get_all_cognitive_feature_ids(),
            "C_psychological": get_all_psychological_feature_ids(),
            "D_social": get_all_social_feature_ids(),
            "E_economic": get_all_economic_feature_ids(),
            "F_political": get_all_political_feature_ids(),
            "G_R_extended": [f.feature_id for f in EXTENDED_FEATURES[:100]],
            "S_AY_remaining": get_all_remaining_feature_ids()[:100],
            "complete": list(FINAL_FEATURES.keys())[:100],
            "missing": list(MISSING_FEATURES.keys())[:100],
            "additional": list(ADDITIONAL_FEATURES.keys())[:100],
        }
    }


@app.get("/api/causal")
def get_causal(limit: int = 50):
    if not engine:
        return {"records": []}
    limit = min(max(1, limit), 500)
    return {"records": engine.event_bus.get_recent_causal(limit)}


@app.get("/api/health")
def get_health():
    if not engine:
        return {"summary": {}, "cases": []}
    agents = engine.agent_manager.get_all_agents()
    cases = [
        {
            "id": agent.id,
            "name": agent.name,
            "disease": agent.disease_name,
            "severity": round(agent.illness_severity, 1),
            "energy": round(agent.energy, 1),
            "happiness": round(agent.happiness, 1),
        }
        for agent in agents
        if agent.is_sick
    ]
    active_cases = len(cases)
    avg_severity = round(sum(case["severity"] for case in cases) / active_cases, 2) if active_cases > 0 else 0.0
    worst = max(cases, key=lambda case: case["severity"]) if cases else None
    summary = {
        "active_cases": active_cases,
        "average_severity": avg_severity,
        "worst_case": worst["name"] if worst else None,
    }
    return {"summary": summary, "cases": cases}


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
    if not engine:
        return {"status": "error", "message": "Engine not ready"}
    
    # If already running or thread is alive, don't create another
    if engine.is_running and run_thread and run_thread.is_alive():
        return {"status": "already_running"}
    
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
        finally:
            engine.is_running = False

    # Join any existing thread first
    if run_thread and run_thread.is_alive():
        run_thread.join(timeout=1.0)
    
    run_thread = threading.Thread(target=run_sim, daemon=False)
    run_thread.start()

    return {"status": "resumed"}


@app.post("/api/control/speed")
def set_speed(tps: float = 1.0):
    """Set the tick delay. tps = ticks per second. Range: 0.1-10."""
    if engine:
        engine.tick_delay = round(max(0.1, min(10.0, 1.0 / tps)), 3)
    return {"tick_delay": engine.tick_delay if engine else None}


# ─────────────────────────────────────────────────────────
# Financial System (E1-E3)
# ─────────────────────────────────────────────────────────

@app.get("/api/financial/summary")
def get_financial_summary():
    if not engine:
        return {"error": "Engine not ready"}
    fs = engine.financial_system
    m = fs.market
    b = fs.banking
    return {
        "market": {
            "bid_ask_spread": round(m.bid_ask_spread, 4),
            "volatility": round(m.volatility, 4),
            "momentum": round(m.momentum, 4),
            "order_book_imbalance": round(m.order_book_imbalance, 2),
            "vwap": round(m.vwap, 2),
        },
        "banking": {
            "reserve_ratio": round(b.reserve_ratio, 4),
            "money_multiplier": round(b.money_multiplier, 2),
            "net_interest_margin": round(b.net_interest_margin, 4),
            "non_performing_loans": round(b.non_performing_loans, 4),
            "repo_haircut": round(b.repo_haircut, 4),
            "yield_curve_inverted": b.is_inverted(),
            "term_spread": round(b.get_term_spread(), 4),
            "zombie_firms": b.zombie_firms,
        },
        "inflation_rate": round(fs.inflation_rate, 4),
        "treasury_holdings": round(fs.treasury_holdings, 2),
    }


@app.get("/api/financial/portfolio/{agent_id}")
def get_portfolio(agent_id: int):
    if not engine:
        return {"error": "Engine not ready"}
    fs = engine.financial_system
    if agent_id not in fs.portfolios:
        return {"error": "Agent not found"}
    p = fs.portfolios[agent_id]
    return {
        "liquidity": round(p.liquidity, 2),
        "total_value": round(p.calculate_total(), 2),
        "asset_count": sum(len(assets) for assets in p.assets.values()),
        "instrument_count": len(p.instruments),
    }


# ─────────────────────────────────────────────────────────
# Political System (F1-F3)
# ─────────────────────────────────────────────────────────

@app.get("/api/political/summary")
def get_political_summary():
    if not engine:
        return {"error": "Engine not ready"}
    ps = engine.political_system
    return {
        "state_formation": {
            "monopoly_on_violence": ps.state.monopoly_on_violence,
            "territorial_control": round(ps.state.territorial_control, 2),
            "tax_extraction_efficiency": round(ps.state.tax_extraction_efficiency, 2),
            "bureaucratic_quality": round(ps.state.bureaucratic_quality, 2),
            "rule_of_law": round(ps.state.rule_of_law, 2),
            "corruption_perceptions": round(ps.state.corruption_perceptions, 2),
            "political_stability": ps.state.political_stability.value,
            "legitimacy_source": ps.state.legitimacy_source.value,
            "performance_legitimacy": round(ps.state.performance_legitimacy, 2),
            "revolutionary_potential": round(ps.state.revolutionary_potential, 2),
            "stability_score": round(ps.state.get_stability_score(), 2),
        },
        "democratic_mechanics": {
            "electoral_system": ps.democracy.electoral_system.value,
            "gerrymandering_level": round(ps.democracy.gerrymandering_level, 2),
            "voter_suppression": ps.democracy.voter_suppression,
            "polarization_index": round(ps.democracy.polarization_index, 2),
            "populist_appeal": round(ps.democracy.populist_appeal, 2),
            "authoritarian_backsliding_risk": round(ps.democracy.authoritarian_backsliding_risk, 2),
            "civic_education": round(ps.democracy.civic_education, 2),
            "democracy_score": round(ps.democracy.get_democracy_score(), 2),
        },
        "international_relations": {
            "balance_of_power_score": round(ps.international.balance_of_power_score, 2),
            "hegemon_present": ps.international.hegemon_present,
            "security_dilemma_active": ps.international.security_dilemma_active,
            "deterrence_credibility": round(ps.international.deterrence_credibility, 2),
            "alliance_count": len(ps.international.alliance_obligations),
            "free_rider_level": round(ps.international.free_rider_level, 2),
            "asylum_backlog": ps.international.asylum_backlog,
            "alliance_strength": round(ps.international.get_alliance_strength(), 2),
        },
        "public_goods": {k: round(v, 2) for k, v in ps.public_goods.items()},
        "governance_score": round(ps.get_governance_score(), 2),
        "treasury": round(ps.treasury, 2),
    }


@app.post("/api/political/policy")
def apply_policy(policy_type: str, intensity: float = 0.5):
    if not engine:
        return {"error": "Engine not ready"}
    result = engine.political_system.apply_policy(policy_type, intensity)
    return result


# ─────────────────────────────────────────────────────────
# Information Physics API
# ─────────────────────────────────────────────────────────

@app.get("/api/information/state")
def get_information_state():
    """Get information physics state for all agents."""
    if not engine:
        return {"knowledge": {}}
    ip = engine.info_physics
    knowledge = {}
    for agent_id, state in ip.agent_states.items():
        knowledge[agent_id] = {
            "known_agents": len(state.known_agents),
            "information_received": state.information_received,
            "trusted_sources": list(state.trusted_sources)[:5],
        }
    return {"knowledge": knowledge, "packets": ip.total_packets}


@app.get("/api/information/trace")
def trace_information(agent_id: str = None):
    """Trace information flow for an agent."""
    if not engine:
        return {"trace": []}
    ip = engine.info_physics
    if agent_id and agent_id in ip.agent_states:
        state = ip.agent_states[agent_id]
        return {
            "agent": agent_id,
            "received": state.information_received,
            "beliefs": list(ip.all_information.items())[:20],
        }
    return {"trace": []}


# ─────────────────────────────────────────────────────────
# Relationships API
# ─────────────────────────────────────────────────────────

@app.get("/api/relationships")
def get_relationships():
    """Get full relationship graph."""
    if not engine:
        return {"relationships": [], "stats": {}}
    rg = engine.agent_manager.rel_graph
    all_rels = []
    for source_id, targets in rg._graph.items():
        for target_id, rel in targets.items():
            all_rels.append({
                "source": source_id,
                "target": target_id,
                "bond": rel.bond,
                "type": rel.relationship_type.value if hasattr(rel.relationship_type, 'value') else str(rel.relationship_type),
            })
    stats = {
        "total_relationships": len(all_rels),
        "friends": sum(1 for r in all_rels if r["type"] == "friend"),
        "rivals": sum(1 for r in all_rels if r["type"] == "rival"),
    }
    return {"relationships": all_rels, "stats": stats}


# ─────────────────────────────────────────────────────────
# Persistence API
# ─────────────────────────────────────────────────────────

@app.get("/api/snapshots")
def list_snapshots():
    """List available snapshots."""
    if not engine or not engine.persistence:
        return {"snapshots": [], "count": 0}
    # Return basic snapshot info
    return {"snapshots": [], "count": engine.stats.get("snapshots_stored", 0)}


@app.post("/api/snapshots/save")
def save_snapshot(name: str = "manual"):
    """Save a snapshot."""
    if not engine or not engine.persistence:
        return {"error": "Persistence not enabled"}
    engine._create_snapshot()
    return {"saved": name, "tick": engine.tick_number}


@app.get("/api/snapshots/load")
def load_snapshot(tick: int = None):
    """Load a snapshot."""
    if not engine or not engine.persistence:
        return {"error": "Persistence not enabled"}
    # This would load from DB - placeholder for now
    return {"loaded": tick, "status": "not_implemented"}


# ─────────────────────────────────────────────────────────
# Full Agent State API (includes physiology)
# ─────────────────────────────────────────────────────────

@app.get("/api/agents/{agent_id}/full")
def get_agent_full(agent_id: str):
    """Get full agent state including physiology."""
    if not engine:
        return {"error": "Engine not ready"}
    agent = engine.agent_manager.get_agent(agent_id)
    if not agent:
        return {"error": "Agent not found"}
    return {
        "id": agent.id,
        "name": agent.name,
        "personality": agent.personality,
        "traits": agent.traits,
        "big_five": agent.big_five,
        "physiology": agent.physiology.get_snapshot() if hasattr(agent, 'physiology') else {},
        "affect": {
            "valence": agent.affect_valence,
            "arousal": agent.affect_arousal,
            "dominance": agent.affect_dominance,
        },
        "dark_traits": {
            "machiavellianism": agent.machiavellianism,
            "narcissism_grandiose": agent.narcissism_grandiose,
            "psychopathy_primary": agent.psychopathy_primary,
        },
        "dimensions": agent.dimension_state,
    }


# ─────────────────────────────────────────────────────────
# Market API
# ─────────────────────────────────────────────────────────

@app.get("/api/market/state")
def get_market_state():
    """Get double auction market state."""
    if not engine or not engine.market:
        return {"error": "Market not available"}
    m = engine.market
    return {
        "symbol": m.symbol,
        "price": m.price,
        "volume": m.volume,
        "spread": m.books.get("GOLD", type('obj', (object,), {'get_spread': lambda s: 0.0})()).get_spread() if "GOLD" in m.books else 0.0,
        "buy_orders": len(m.buy_orders),
        "sell_orders": len(m.sell_orders),
    }
