import sys
import os

api_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(api_dir)

# Add all relevant paths
for d in [
    api_dir,
    os.path.join(api_dir, 'engine'),
    os.path.join(api_dir, 'engine', 'subengines'),
    root_dir,
    os.path.join(root_dir, 'engine'),
    os.path.join(root_dir, 'engine', 'subengines')
]:
    if os.path.exists(d) and d not in sys.path:
        sys.path.insert(0, d)

# Import app from main
try:
    from engine.main import app
except Exception:
    from main import app
