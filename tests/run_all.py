"""Run the catalog tests: python -I tests/run_all.py"""
import sys
import unittest
from pathlib import Path

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(here), pattern="test_*.py", top_level_dir=str(here))
    sys.exit(0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1)
