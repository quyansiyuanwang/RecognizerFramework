from typing import Any, Callable, Mapping, Optional, Tuple, TypeVar

_DF_K = TypeVar("_DF_K")
_DF_V = TypeVar("_DF_V")


def dict_filter(
    d: Mapping[_DF_K, _DF_V],
    lam: Callable[[Tuple[_DF_K, _DF_V]], bool],
) -> Mapping[_DF_K, _DF_V]:
    return {k: v for k, v in d.items() if lam((k, v))}


def dict_filter_keys(
    d: Mapping[_DF_K, _DF_V],
    k: _DF_K,
    reverse: bool = False,
) -> Mapping[_DF_K, _DF_V]:
    return dict_filter(
        d,
        lambda item: (item[0] == k if not reverse else item[0] != k),
    )


def dict_filter_values(
    d: Mapping[_DF_K, _DF_V],
    v: _DF_V,
    reverse: bool = False,
) -> Mapping[_DF_K, _DF_V]:
    return dict_filter(
        d,
        lambda item: (item[1] == v if not reverse else item[1] != v),
    )


def convert_float(value: Any) -> Optional[float]:
    if isinstance(value, (float, int)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            pass
    return None
