"""
Main Entry Point - God-Tier Engine
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from simulation.engine import GodTierEngine
from utils.logger import configure_logging, get_logger


def parse_args():
    parser = argparse.ArgumentParser(description="Reality Simulator - God-Tier Engine")
    parser.add_argument("--ticks", type=int, default=None, help="Run for N ticks")
    parser.add_argument("--delay", type=float, default=0.8, help="Seconds between ticks")
    parser.add_argument("--agents", type=int, default=50, help="Number of starting agents")
    parser.add_argument("--server", action="store_true", help="Run FastAPI server")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--no-persist", action="store_true", help="Disable persistence")
    return parser.parse_args()


def main():
    args = parse_args()
    
    log_level = "DEBUG" if args.debug else "INFO"
    configure_logging(log_level)
    logger = get_logger(__name__)
    
    # Build config
    config = {
        "max_ticks": args.ticks,
        "tick_delay_seconds": args.delay,
        "initial_agents": args.agents,
        "use_persistence": not args.no_persist and not args.server,  # Disable persistence in server mode
    }
    
    logger.info("=" * 60)
    logger.info("  Reality Simulator - God-Tier Engine")
    logger.info("=" * 60)
    logger.info(f"  Agents: {args.agents}")
    logger.info(f"  Tick delay: {args.delay}s")
    logger.info(f"  Max ticks: {args.ticks or 'infinite'}")
    if args.server:
        logger.info(f"  Persistence: disabled (server mode)")
    else:
        logger.info(f"  Persistence: {'enabled' if not args.no_persist else 'disabled'}")
    logger.info("=" * 60)
    
    if args.server:
        import uvicorn
        logger.info(f"Starting API server on port {args.port}...")
        uvicorn.run("api.app:app", host="0.0.0.0", port=args.port, reload=False)
    else:
        engine = GodTierEngine(config)
        engine.run()


if __name__ == "__main__":
    main()