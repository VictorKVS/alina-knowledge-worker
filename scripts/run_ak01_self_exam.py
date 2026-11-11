from __future__ import annotations

import json

from ak01.self_diagnostic import run_ak01_self_diagnostic


def main() -> int:
    result = run_ak01_self_diagnostic()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
