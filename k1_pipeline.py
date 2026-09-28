"""Compatibility entry point for the K1 autonomous project.

New development belongs in k1_autoproject.py. This module remains so existing
local commands that call k1_pipeline.py continue to work.
"""
from k1_autoproject import main

if __name__ == "__main__":
    raise SystemExit(main())
