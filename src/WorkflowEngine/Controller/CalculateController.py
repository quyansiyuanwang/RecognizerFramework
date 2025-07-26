import enum
import math
import string
from typing import Any, Callable, Dict, List, LiteralString, Optional, Tuple, Union

from src.WorkflowEngine.Util.util import convert_float

from ...Models.calculate import ExpressionUnionType
from ...Typehints.basic import Digit


class _ExpressionType(enum.Enum):
    VARIABLE = "variable"
    OPERATION = "operation"
    FUNCTION = "function"
    QUOTE = "quote"
    DIGIT = "digit"


class CalculateController:
    _SUPPORTED_FUNCTIONS: Dict[str, Callable[..., float]] = {
        "sqrt": math.sqrt,
        "pow": math.pow,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "fabs": math.fabs,
        "ceil": math.ceil,
        "floor": math.floor,
        "lg": math.log10,
    }

    _SPACE: LiteralString = " "
    _COMMA: LiteralString = ","
    _VAR_LETTERS: LiteralString = string.ascii_letters + "_"
    _DIGITS: LiteralString = string.digits
    _OPERATORS: LiteralString = "+-*/%**//"
    _FUNCTION_START: LiteralString = "$"
    _QUOTE_START: LiteralString = "("
    _QUOTE_END: LiteralString = ")"

    _MODE_END_MAP: Dict[str, Tuple[str, Tuple[int, int], _ExpressionType]] = {
        _VAR_LETTERS: (
            _SPACE + _DIGITS + _OPERATORS + _FUNCTION_START + _QUOTE_START + _QUOTE_END,
            (0, 0),
            _ExpressionType.VARIABLE,
        ),
        _DIGITS: (
            _SPACE + _OPERATORS + _FUNCTION_START + _QUOTE_START + _QUOTE_END,
            (0, 0),
            _ExpressionType.DIGIT,
        ),
        _OPERATORS: (
            _SPACE + _DIGITS + _FUNCTION_START + _QUOTE_START + _QUOTE_END,
            (0, 0),
            _ExpressionType.OPERATION,
        ),
        _FUNCTION_START: (_QUOTE_END, (0, 1), _ExpressionType.FUNCTION),
        _QUOTE_START: (_QUOTE_END, (0, 1), _ExpressionType.QUOTE),
        _QUOTE_END: (
            _SPACE + _DIGITS + _VAR_LETTERS + _FUNCTION_START,
            (0, 0),
            _ExpressionType.QUOTE,
        ),
    }

    @classmethod
    def _read_expression(
        cls, sentence: str, begin: int = 0
    ) -> Tuple[str, int, _ExpressionType]:
        """it return the expression and the beyond index"""
        end = begin
        first_char = sentence[begin]
        for chars, e in cls._MODE_END_MAP.items():
            if first_char in chars:
                end_letters, (l, r), m = e
                break
        else:
            raise ValueError(f"Invalid character '{first_char}' at position {begin}")
        end += 1
        while end < len(sentence):
            cur_char = sentence[end]
            if cur_char in end_letters:
                break
            end += 1
        return (sentence[begin + l : end + r], end + r, m)

    @classmethod
    def _parse_function_call(cls, sentence: str) -> Tuple[str, List[str]]:
        """Parse a function call like $sqrt(a) or $pow(b, 2)

        return e.g. ('sqrt', 'a') or ('pow', 2) if no argument is given, return empty string
        """
        if not sentence.startswith(cls._FUNCTION_START):
            raise ValueError(f"Invalid function call '{sentence}'")
        end = 1
        while end < len(sentence) and sentence[end] != cls._QUOTE_START:
            end += 1
        func_name = sentence[1:end]
        args_str = sentence[end + 1 : -1].strip()
        args: List[str] = (
            list(map(str.strip, args_str.split(cls._COMMA))) if args_str else []
        )
        return func_name, args

    @classmethod
    def _get_expression(
        cls,
        sentence: str,
        known: Dict[str, Digit],
        expressions: Dict[str, ExpressionUnionType],
    ) -> Optional[ExpressionUnionType]:
        if sentence in known:
            return known[sentence]
        exp_res = expressions.get(sentence)
        if isinstance(exp_res, (float, int)) or (
            exp_res is not None and convert_float(exp_res) is not None
        ):
            return float(exp_res)
        return exp_res

    @classmethod
    def _calculate_expression(
        cls,
        sentence: str,
        known: Dict[str, Digit],
        expressions: Dict[str, ExpressionUnionType],
    ) -> float:
        # e.g. 'b ** $pow(aa, 2) - 1 + c - (1 - 2)'
        idx = 0
        length = len(sentence)

        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "//": 2,
            "%": 2,
            "**": 3,
            "(": 0,
        }

        operator_stack: List[str] = []
        postfix: List[Union[str, float]] = []
        while idx < length:
            if sentence[idx] == cls._SPACE:
                idx += 1
                continue
            expression, idx, mode = cls._read_expression(sentence, idx)
            if mode == _ExpressionType.VARIABLE:
                real = cls._get_expression(expression, known, expressions)
                if real is None:
                    raise ValueError(f"Unknown variable '{expression}'")
                if isinstance(real, str):
                    real = cls._calculate_expression(real, known, expressions)
                known[expression] = real
                postfix.append(real)

            elif mode == _ExpressionType.DIGIT:
                postfix.append(float(expression))

            elif mode == _ExpressionType.OPERATION:
                while (
                    operator_stack
                    and precedence[operator_stack[-1]] >= precedence[expression]
                ):
                    postfix.append(operator_stack.pop())
                operator_stack.append(expression)

            elif mode == _ExpressionType.FUNCTION:
                func_name, args = cls._parse_function_call(expression)
                if func_name in cls._SUPPORTED_FUNCTIONS:
                    parsed_args: List[Digit] = []
                    for arg in args:
                        v = cls._get_expression(
                            sentence=arg, known=known, expressions=expressions
                        )
                        if v is None:
                            raise ValueError(
                                f"Unknown variable '{arg}' in function call '{func_name}'"
                            )
                        if isinstance(v, str):
                            v = cls._calculate_expression(v, known, expressions)

                        parsed_args.append(v)

                    postfix.append(cls._SUPPORTED_FUNCTIONS[func_name](*parsed_args))
                else:
                    raise ValueError(f"Unknown function '{func_name}'")
            elif mode == _ExpressionType.QUOTE:
                postfix.append(
                    cls._calculate_expression(expression[1:-1], known, expressions)
                )
            else:
                raise ValueError(f"Unknown mode '{mode}' for expression '{expression}'")

        while operator_stack:
            postfix.append(operator_stack.pop())
        # Now we have a postfix expression, we can evaluate it
        stack: List[float] = []
        for token in postfix:
            if isinstance(token, (int, float)):
                stack.append(token)
                continue
            b: float = stack.pop()
            a: float = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
            elif token == "//":
                stack.append(a // b)
            elif token == "%":
                stack.append(a % b)
            elif token == "**":
                stack.append(a**b)
            else:
                raise ValueError(f"Unknown operator '{token}'")
        if len(stack) != 1:
            raise ValueError(f"Invalid postfix expression, stack: {stack}")
        return stack[0]

    @classmethod
    def calculate(
        cls, expressions: Dict[str, ExpressionUnionType], variables: Dict[str, Any]
    ) -> Dict[str, float]:
        calculated_values: Dict[str, float] = {}
        calculated_values.update(variables)
        for key, expression in expressions.items():
            if isinstance(expression, (float, int)):
                calculated_values[key] = float(expression)
                continue
            calculated_values[key] = cls._calculate_expression(
                expression, calculated_values, expressions
            )
        return calculated_values
