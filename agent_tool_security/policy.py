from __future__ import annotations

import re
from pathlib import Path

from .models import Decision, ToolCall, ToolSpec
from .schema import validate


INJECTION = re.compile(r"忽略.{0,12}(规则|指令|限制)|system prompt|developer message|绕过.{0,8}(权限|确认)", re.I)


class PolicyEngine:
    def __init__(self, tools: list[ToolSpec], sandbox: Path) -> None:
        self.tools = {tool.name: tool for tool in tools}
        self.sandbox = sandbox.resolve()

    def evaluate(self, call: ToolCall) -> Decision:
        reasons: list[str] = []
        spec = self.tools.get(call.tool)
        if spec is None:
            return Decision(call.call_id, False, ["tool_not_allowed"])
        reasons.extend(validate(spec.schema, call.arguments))
        if INJECTION.search(call.user_text):
            reasons.append("prompt_injection_detected")
        if spec.risk == "high" and not call.confirmed:
            reasons.append("confirmation_required")
        path = call.arguments.get("path")
        if isinstance(path, str):
            candidate = (self.sandbox / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
            try:
                candidate.relative_to(self.sandbox)
            except ValueError:
                reasons.append("sandbox_escape")
        return Decision(call.call_id, not reasons, reasons, dict(call.arguments))
