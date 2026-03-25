from __future__ import annotations

import sys
from pathlib import Path

"""
This file makes sure that the "src/" folder is added to Python's import path.

This is needed so that when we run tests (for example using pytest),
Python can find and import the "compression" package correctly.

Without this, pytest might not recognize the project structure.
"""

# Get the root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Path to the "src" folder where the main code is located
SRC_DIR = PROJECT_ROOT / "src"

# Add "src" to Python path if it is not already there
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
