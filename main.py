import sys
import os

# Root directory path resolution
root_dir = os.path.dirname(os.path.abspath(__file__))
for p in [
    root_dir,
    os.path.join(root_dir, "engine"),
    os.path.join(root_dir, "engine", "subengines"),
    os.path.join(root_dir, "api")
]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from engine.main import app
