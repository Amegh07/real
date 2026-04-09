"""
Logger Utility
--------------
Centralized logging setup for the entire simulation.
All modules should import get_logger from here — never configure
logging individually per file.
"""

import logging
import sys

# Global format: timestamp + level + module + message
LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
DATE_FORMAT = "%H:%M:%S"

_configured = False


def configure_logging(level: str = "INFO"):
    """
    Call once at startup to configure logging globally.
    """
    global _configured
    if _configured:
        return
    _configured = True

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    root = logging.getLogger()
    root.setLevel(numeric_level)

    # Avoid duplicate handlers if called multiple times in testing
    if not root.handlers:
        root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger. Import and use this everywhere.
    """
    return logging.getLogger(name)
