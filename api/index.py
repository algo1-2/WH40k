import sys
import os

# Discover root and subpackages
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
engine_dir = os.path.join(root_dir, "engine")
subengines_dir = os.path.join(engine_dir, "subengines")

for p in [root_dir, engine_dir, subengines_dir]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from engine.main import app
