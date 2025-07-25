from typing import Dict, TypeAlias, Union

from pydantic import BaseModel, Field

from ..Typehints.basic import Digit

ExpressionUnionType: TypeAlias = Union[str, float, int]


class Calculate(BaseModel):
    expressions: Dict[str, ExpressionUnionType] = Field(
        ...,
        description=(
            "计算表达式字典, 键为变量名, 值为表达式字符串"
            "或直接的数值, 表达式可以包含其他变量名"
            "变量直接用字母组合表示, 例如: {'a': 'b * b - c', 'b': 'a ** 0.5 + 1'}"
            "可用表达式: 加法'+', 减法'-', 乘法'*', 真除'/', 次方'**', 整除'//', 取模'%'"
            "函数调用: 以$开头, 例如: {'c': '$sqrt(a)'}"
        ),
    )
    variables: Dict[str, Digit] = Field(
        default_factory=dict, description="计算中使用的变量及其值"
    )
    returns: Dict[str, str] = Field(
        default_factory=dict,
        description="计算结果返回的变量名, 键为新变量名, 值为表达式变量名",
    )


__all__ = ["Calculate", "ExpressionUnionType"]
