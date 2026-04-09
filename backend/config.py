"""
Configuration — Phase 2 Update
--------------------------------
Added: economy settings, treasury income, inflation, job slots.
"""

SIMULATION_CONFIG = {
    # ── Simulation ──────────────────────────────────────────
    "tick_delay_seconds": 0.8,
    "max_ticks": None,
    "ticks_per_day": 10,

    # ── Agents ──────────────────────────────────────────────
    "initial_agents": 8,

    # ── Economy ─────────────────────────────────────────────
    "starting_treasury": 15_000.0,
    "base_wage": 20.0,
    "food_cost": 12.0,
    "tax_rate": 0.01,

    # Treasury refill per tick (simulates external trade/taxes)
    "treasury_income_per_tick": 40.0,

    # Price inflation: how much the multiplier grows each tick
    "inflation_growth": 0.0005,

    # ── Groq AI (Phase 4+) ──────────────────────────────────
    "use_groq": True,
    "groq_max_tokens": 200,
    "groq_model": "llama3-8b-8192",

    # ── Logging ─────────────────────────────────────────────
    "log_level": "INFO",
}
