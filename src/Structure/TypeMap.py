from typing import Any, Callable, Dict, Optional, Type


class TypeMap:
    type_map: Dict[str, Type[Any]] = {}

    @staticmethod
    def register(key: str) -> Callable[[Type[Any]], Type[Any]]:
        def decorator(value: Type[Any]) -> Type[Any]:
            TypeMap.type_map[key] = value
            return value

        return decorator

    @staticmethod
    def get(key: str) -> Optional[Type[Any]]:
        return TypeMap.type_map.get(key)
