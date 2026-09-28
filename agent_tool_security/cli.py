from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import ToolSpec
from .policy import PolicyEngine
from .runner import BenchmarkRunner


DEFAULT_TOOLS = [
    ToolSpec("search_docs", {"type": "object", "required": ["query"], "properties": {"query": {"type": "string", "maxLength": 500}}, "additionalProperties": False}),
    ToolSpec("read_file", {"type": "object", "required": ["path"], "properties": {"path": {"type": "string", "maxLength": 300}}, "additionalProperties": False}),
    ToolSpec("delete_file", {"type": "object", "required": ["path"], "properties": {"path": {"type": "string", "maxLength": 300}}, "additionalProperties": False}, risk="high"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate agent tool calls against security policy")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--cases", type=Path, required=True)
    run.add_argument("--output", type=Path, default=Path("outputs/result.json"))
    run.add_argument("--sandbox", type=Path, default=Path("sandbox"))
    args = parser.parse_args()
    records = BenchmarkRunner(PolicyEngine(DEFAULT_TOOLS, args.sandbox)).run(args.cases)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    passed = sum(row["benchmark_passed"] for row in records)
    print(f"cases={len(records)} passed={passed} output={args.output}")


if __name__ == "__main__":
    main()
