import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

if "pytest" not in sys.modules:
    from .hooks import init_hooks

    init_hooks()
