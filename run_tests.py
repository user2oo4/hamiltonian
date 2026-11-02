#!/usr/bin/env python3
"""Simple test runner that does not require pytest.

Usage:
    python3 run_tests.py
"""

import traceback

import tests.test_core as t


def main() -> int:
    fns = [getattr(t, name) for name in dir(t) if name.startswith("test_")]
    passed = failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
