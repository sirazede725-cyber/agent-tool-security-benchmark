from __future__ import annotations

from typing import Any


TYPE_MAP = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list}


def validate(schema: dict[str, Any], arguments: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    properties = schema.get("properties", {})
    for name in schema.get("required", []):
        if name not in arguments:
            errors.append(f"missing_required:{name}")
    if schema.get("additionalProperties") is False:
        for name in arguments:
            if name not in properties:
                errors.append(f"unexpected_argument:{name}")
    for name, value in arguments.items():
        rule = properties.get(name)
        if not rule:
            continue
        expected = TYPE_MAP.get(rule.get("type"))
        if expected and (isinstance(value, bool) if rule.get("type") in ("integer", "number") else False):
            errors.append(f"invalid_type:{name}")
        elif expected and not isinstance(value, expected):
            errors.append(f"invalid_type:{name}")
        if isinstance(value, str) and "enum" in rule and value not in rule["enum"]:
            errors.append(f"invalid_enum:{name}")
        if isinstance(value, str) and len(value) > rule.get("maxLength", 10_000):
            errors.append(f"too_long:{name}")
    return errors
