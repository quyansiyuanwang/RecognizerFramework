import argparse
import sys
from typing import Dict

from ..main import run


def default_choice_map(default: bool) -> Dict[str, bool]:
    return {
        "y": True,
        "n": False,
        "yes": True,
        "no": False,
        "": default,
    }


def switch_choice(msg: str, choice_map: Dict[str, bool]) -> bool:
    user_input = input(msg).strip().lower()
    while user_input not in choice_map:
        print("Invalid input. Please enter 'y' or 'n'.")
        user_input = input(msg).strip().lower()
    return choice_map.get(user_input, False)


def until_not_empty(prompt: str) -> str:
    user_input = input(prompt).strip()
    while not user_input:
        print("Input cannot be empty. Please try again.")
        user_input = input(prompt).strip()
    return user_input


def input_args() -> argparse.Namespace:
    args = argparse.Namespace()
    args.path = until_not_empty("Enter the path to the input JSON file: ")

    msg = "Await for all tasks to complete? (y/N): "
    args.await_all = switch_choice(msg, default_choice_map(False))

    args.verbose = switch_choice(
        "Enable verbose output? (Y/n): ", default_choice_map(True)
    )
    return args


def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recognizer Framework CLI")
    parser.add_argument(
        "path",
        type=str,
        help="Path to the input JSON file containing the workflow definition",
    )
    parser.add_argument(
        "-a",
        "--await_all",
        action="store_true",
        default=False,
        help="Await for all tasks to complete before printing results (default: False)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_false",
        default=True,
        help="Enable verbose output (default: True)",
    )

    args = parser.parse_args(sys.argv[1:])
    return args


def cli():
    if len(sys.argv) > 1:
        args = args_parse()
    else:
        args = input_args()
    run(args.path, await_all=args.await_all, verbose=args.verbose)
