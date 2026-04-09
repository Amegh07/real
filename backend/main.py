"""
Main Entry Point
----------------
Start the Reality Simulator Engine here.

Usage:
    python main.py

Optional flags:
    --ticks N      Run for N ticks then stop
    --delay D      Seconds between ticks (float, default 0.8)
    --agents A     Number of starting agents
    --server       Run as a FastAPI backend server on port 8000
    --debug        Enable debug-level logging
"""

import argparse
import sys
import os

# Allow imports from the backend root
sys.path.insert(0, os.path.dirname(__file__))

from config import SIMULATION_CONFIG
from simulation.engine import SimulationEngine
from utils.logger import configure_logging, get_logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="Reality Simulator Engine — Phase 1"
    )
    parser.add_argument(
        "--ticks", type=int, default=None,
        help="Run for N ticks then stop (default: infinite)"
    )
    parser.add_argument(
        "--delay", type=float, default=None,
        help="Seconds between ticks (default from config)"
    )
    parser.add_argument(
        "--agents", type=int, default=None,
        help="Number of starting agents (default from config)"
    )
    parser.add_argument(
        "--server", action="store_true",
        help="Run the FastAPI server instead of console mode"
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Build runtime config (CLI args override defaults)
    config = SIMULATION_CONFIG.copy()

    if args.ticks is not None:
        config["max_ticks"] = args.ticks
    if args.delay is not None:
        config["tick_delay_seconds"] = args.delay
    if args.agents is not None:
        config["initial_agents"] = args.agents
    if args.debug:
        config["log_level"] = "DEBUG"

    # Boot logging before anything else
    configure_logging(config["log_level"])
    logger = get_logger(__name__)

    logger.info("=" * 60)
    logger.info("  Reality Simulator Engine — Phase 1")
    logger.info("=" * 60)
    logger.info(f"  Agents    : {config['initial_agents']}")
    logger.info(f"  Tick delay: {config['tick_delay_seconds']}s")
    logger.info(f"  Max ticks : {config.get('max_ticks', 'infinite')}")
    logger.info(f"  Groq AI   : {'enabled' if config.get('use_groq') else 'disabled (rule-based)'}")
    logger.info("=" * 60)

    # Start mode
    if args.server:
        import uvicorn
        logger.info("Starting API server on port 8000...")
        # Start uvicorn. Note: host is 0.0.0.0 for external access
        uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=False)
    else:
        # Create and run the engine synchronously
        engine = SimulationEngine(config)
        engine.run()


if __name__ == "__main__":
    main()
