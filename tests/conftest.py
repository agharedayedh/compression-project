from __future__ import annotations

import sys
from pathlib import Path

# Make "src/" importable so plain "pytest" can find the compression package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
