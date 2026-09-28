from __future__ import annotations

import json
from pathlib import Path

from .models import Decision, ToolCall
from .policy import PolicyEngine


class BenchmarkRunner:
    def __init__(self, policy: PolicyEngine) -> None:
        self.policy = policy

    def run(self, cases: Path) -> list[dict]:
        records: list[dict] = []
        for line in cases.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            expected = row.pop("expected_allowed")
            decision: Decision = self.policy.evaluate(ToolCall(**row))
            records.append({
                **decision.to_dict(),
                "expected_allowed": expected,
                "benchmark_passed": decision.allowed == expected,
            })
        return records
