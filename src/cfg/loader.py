from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from .models import ConfigBundle, StrategyConfig


class ConfigError(Exception):
    """Raised when configuration files are invalid."""


def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Config file {path} not found")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def _resolve_inheritance(raw: Dict[str, Any], config_dir: Path) -> Dict[str, Any]:
    extends = raw.get("extends")
    if not extends:
        return raw
    base_path = config_dir / f"{extends}.yaml"
    base_data = load_yaml(base_path)
    merged = _merge_dicts(base_data, {k: v for k, v in raw.items() if k != "extends"})
    return _resolve_inheritance(merged, config_dir)


def load_config(path: str | Path) -> ConfigBundle:
    config_path = Path(path)
    config_dir = config_path.parent
    data = load_yaml(config_path)
    resolved = _resolve_inheritance(data, config_dir)
    config = StrategyConfig.parse_obj(resolved)
    return ConfigBundle(config=config, source_path=str(config_path.resolve()))


__all__ = ["ConfigBundle", "ConfigError", "load_config"]
