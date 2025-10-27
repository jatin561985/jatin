from __future__ import annotations

from typing import Any, Dict, List, Tuple


def safe_load(stream: str) -> Dict[str, Any]:
    if hasattr(stream, "read"):
        text = stream.read()
    else:
        text = str(stream)
    lines = [line.rstrip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    root: Dict[str, Any] = {}
    stack: List[Tuple[Dict[str, Any], int]] = [(root, -1)]
    for line in lines:
        indent = len(line) - len(line.lstrip(" "))
        while stack and indent <= stack[-1][1] and len(stack) > 1:
            stack.pop()
        current = stack[-1][0]
        key, value = _parse_line(line.strip())
        if isinstance(value, dict):
            current[key] = value
            stack.append((value, indent))
        else:
            current[key] = value
    return root


def _parse_line(line: str) -> Tuple[str, Any]:
    if ":" not in line:
        raise ValueError(f"Invalid line: {line}")
    key, raw = line.split(":", 1)
    key = key.strip()
    raw = raw.strip()
    if not raw:
        return key, {}
    return key, _parse_scalar(raw)


def _parse_scalar(value: str) -> Any:
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() == "null":
        return None
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
