"""Eval entrypoint: python -m evals.run [--deterministic | --judge]

Deterministic checks run offline and always. The LLM-as-judge suite runs the real
turn loop and needs APP_API_KEY (+ optional APP_PROVIDER / APP_MODEL). Both use a
temp DB + workspace so nothing touches ~/.assistant.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path


def _load_cases() -> list[dict]:
    d = Path(__file__).parent / "cases"
    cases: list[dict] = []
    for f in sorted(d.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                cases.append(json.loads(line))
    return cases


def main() -> None:
    ap = argparse.ArgumentParser(description="Agent evals")
    ap.add_argument("--deterministic", action="store_true", help="offline checks only")
    ap.add_argument("--judge", action="store_true", help="LLM-as-judge (needs APP_API_KEY)")
    args = ap.parse_args()
    run_all = not (args.deterministic or args.judge)

    tmp = Path(tempfile.mkdtemp(prefix="evals-"))
    os.environ.setdefault("APP_DB_PATH", str(tmp / "state.db"))
    os.environ.setdefault("APP_FILE_ROOT", str(tmp / "workspace"))
    os.environ["APP_FILE_UNRESTRICTED"] = "0"
    from app.config import get_settings
    get_settings.cache_clear()

    code = 0

    if args.deterministic or run_all:
        from evals.deterministic import run_deterministic
        r = run_deterministic()
        for name, ok in r["results"]:
            print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        print(f"deterministic: {r['passed']}/{r['total']} passed")
        if r["passed"] != r["total"]:
            code = 1

    if args.judge or run_all:
        provider = os.getenv("APP_PROVIDER", "openai")
        model = os.getenv("APP_MODEL") or None
        key = os.getenv("APP_API_KEY", "")
        if not key:
            print("judge: skipped (set APP_API_KEY to run LLM-as-judge evals)")
        else:
            from evals.judge import run_judge
            res = asyncio.run(run_judge(_load_cases(), provider, model, key))
            for r in res:
                print(f"  {r['id']}: tool_ok={r['tool_ok']} helpful={r['helpful']} "
                      f"hallucinated={r['hallucinated']}")
            fails = sum(1 for r in res if not r["tool_ok"] or r.get("hallucinated"))
            print(f"judge: {len(res) - fails}/{len(res)} ok")
            if fails:
                code = 1

    sys.exit(code)


if __name__ == "__main__":
    main()
