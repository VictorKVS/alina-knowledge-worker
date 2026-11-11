from __future__ import annotations

import json

from ak01.hidden_case_suite import run_q2_hidden_cases


def main() -> int:
    result = run_q2_hidden_cases()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
