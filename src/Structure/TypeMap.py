from typing import Any, Callable, Dict, Optional, Type, TypeVar

T = TypeVar("T", bound=type)


class TypeMap:
    type_map: Dict[str, Type[Any]] = {}

    @staticmethod
    def register(key: str) -> Callable[[T], T]:

        def decorator(cls: T) -> T:
            TypeMap.type_map[key] = cls
            return cls

        return decorator

    @staticmethod
    def get(key: str) -> Optional[Type[Any]]:
        return TypeMap.type_map.get(key)
