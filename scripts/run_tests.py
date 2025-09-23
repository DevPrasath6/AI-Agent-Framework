import importlib
import sys

MODULES = ["tests.test_core_agent_workflow"]


def run():
    failures = 0
    for mod in MODULES:
        try:
            m = importlib.import_module(mod)
            print(f"Imported {mod}")
        except Exception as e:
            print(f"Failed to import {mod}: {e}")
            failures += 1
    if failures:
        print("Some tests failed to import")
        sys.exit(2)
    print("Basic import checks passed")


if __name__ == "__main__":
    run()
