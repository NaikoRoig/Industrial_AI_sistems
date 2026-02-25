import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.verification.test_runner import TestRunner

if __name__ == "__main__":
    runner = TestRunner()
    runner.run_suite()
