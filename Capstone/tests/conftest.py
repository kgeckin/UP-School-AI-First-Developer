"""Include the Streamlit source folder in imports for the test suite."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
