#!/usr/bin/env python3
"""Run sleeper-gini directly from the repository.

Requires dependencies to be installed:
    pip install httpx click pydantic rich
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from sleeper_gini.cli import main

if __name__ == "__main__":
    main()
