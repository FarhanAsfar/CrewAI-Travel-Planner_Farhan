"""
logger.py

Centralised logging for the Travel Planner package.
"""

import logging
import os
from datetime import datetime

# Resolve project root (src/travel_planner/logger.py → ../../.. = project root)
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

_LOG_DIR = os.path.join(_PROJECT_ROOT, "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

_LOG_FILE = os.path.join(
    _LOG_DIR,
    f"travel_planner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
)

_FORMATTER = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _init_root_logger() -> logging.Logger:
    """Initialise the root logger once; subsequent imports reuse it."""
    root = logging.getLogger("travel_planner")
    if root.handlers:
        return root  

    root.setLevel(logging.DEBUG)

    # Console — INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(_FORMATTER)
    root.addHandler(ch)

    # File — DEBUG
    fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_FORMATTER)
    root.addHandler(fh)

    root.info(f"Logging initialised → {_LOG_FILE}")
    return root


_init_root_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger under the 'travel_planner' namespace.

    Usage:
        from travel_planner.logger import get_logger
        log = get_logger(__name__)
    """
    return logging.getLogger(f"travel_planner.{name}")