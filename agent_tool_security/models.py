from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolSpec:
    name: str
    schema: dict[str, Any]
    risk: str = "low"


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    tool: str
    arguments: dict[str, Any]
    user_text: str = ""
    confirmed: bool = False


@dataclass
class Decision:
    call_id: str
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    normalized_arguments: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
