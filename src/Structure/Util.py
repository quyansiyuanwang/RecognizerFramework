from typing import Any


def repr_indent(obj: Any, cls_name: str, indent: int = 0) -> str:
    string = f"<{cls_name}(\n"
    for key, value in obj.__dict__.items():
        if value is None or key.startswith("_"):
            continue
        is_indentable: bool = not isinstance(
            value, (str, int, float, bool, dict, set, list, tuple)
        )
        representation: str = (
            value.__repr__(indent + 4) if is_indentable else f"{value}"
        )
        string += f"{' ' * (indent + 4)}{key}={representation},\n"
    string = string.rstrip(",\n") + "\n" + " " * indent + ")>"
    return string
