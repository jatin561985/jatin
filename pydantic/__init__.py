from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, get_type_hints


class FieldInfo:
    def __init__(self, default: Any = None, default_factory: Callable[[], Any] | None = None) -> None:
        self.default = default
        self.default_factory = default_factory


def Field(default: Any = None, default_factory: Callable[[], Any] | None = None) -> FieldInfo:
    return FieldInfo(default=default, default_factory=default_factory)


def validator(field_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        setattr(func, "_validator_fields", (field_name,))
        return func

    return decorator


class BaseModelMeta(type):
    def __new__(mcls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]):
        validators: Dict[str, List[Callable[..., Any]]] = {}
        fields: Dict[str, FieldInfo] = {}
        annotations = namespace.get("__annotations__", {})
        for base in bases:
            validators.update(getattr(base, "__validators__", {}))
            fields.update(getattr(base, "__field_defs__", {}))
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, FieldInfo):
                fields[attr_name] = attr_value
            if callable(attr_value) and hasattr(attr_value, "_validator_fields"):
                field = getattr(attr_value, "_validator_fields")[0]
                validators.setdefault(field, []).append(attr_value)
        namespace["__validators__"] = validators
        namespace["__field_defs__"] = fields
        cls = super().__new__(mcls, name, bases, namespace)
        cls.__annotations__ = get_type_hints(cls)
        return cls


class BaseModel(metaclass=BaseModelMeta):
    __validators__: Dict[str, List[Callable[..., Any]]]
    __field_defs__: Dict[str, FieldInfo]

    def __init__(self, **data: Any) -> None:
        for name, annotation in self.__annotations__.items():
            value = data.get(name, self._get_default(name))
            value = self._coerce_field(annotation, value)
            setattr(self, name, value)
        self._run_validators(data)

    @classmethod
    def parse_obj(cls: Type["BaseModel"], data: Dict[str, Any]) -> "BaseModel":
        return cls(**data)

    def dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()

    def _get_default(self, name: str) -> Any:
        if name in self.__field_defs__:
            info = self.__field_defs__[name]
            if info.default_factory is not None:
                return info.default_factory()
            return info.default
        return getattr(type(self), name, None)

    def _coerce_field(self, annotation: Any, value: Any) -> Any:
        origin = getattr(annotation, "__origin__", None)
        if isinstance(value, dict) and isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return annotation.parse_obj(value)
        if annotation is time and isinstance(value, str):
            return datetime.strptime(value, "%H:%M").time()
        if origin in {dict, Dict}:
            return dict(value) if value is not None else {}
        return value

    def _run_validators(self, values: Dict[str, Any]) -> None:
        state = self.__dict__.copy()
        for field, funcs in self.__validators__.items():
            for func in funcs:
                new_value = func(type(self), getattr(self, field), state)
                if new_value is not None:
                    setattr(self, field, new_value)


__all__ = ["BaseModel", "Field", "validator"]
