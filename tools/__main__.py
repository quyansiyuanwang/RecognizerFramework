import argparse
import json
import os
import subprocess
from typing import Dict, List, Optional, Tuple

from .util import Color

tools: Dict[str, str] = {}
workflows: Dict[str, List[str]] = {}


def load_workflows():
    global workflows
    with open("tools/SingleScripts/workflows.json", "r", encoding="utf-8") as f:
        json_workflows = json.load(f)
        for name, workflow in json_workflows.items():
            workflows[name] = workflow


def load_tools():
    global tools
    current_dir: str = os.path.dirname(os.path.abspath(__file__)) + "/SingleScripts"

    python_files: List[str] = [
        f
        for f in os.listdir(current_dir)
        if f.endswith(".py")
        and f != os.path.basename(__file__)
        and not f.startswith("_")
    ]

    for py_file in python_files:
        file_path: str = os.path.join(current_dir, py_file)
        name: str = os.path.splitext(py_file)[0]
        tools[name] = file_path


def run_tool(tool_name: str, extra_args: Optional[List[str]] = None):
    global tools
    if tool_name not in tools:
        raise ValueError(f"{Color.RED}[ERR]Tool '{tool_name}' not found.{Color.RESET}")
    if extra_args is None:
        extra_args = []
    tool_path: str = tools[tool_name]
    print(f"{Color.YELLOW}[WRN]Running {tool_name}...{Color.RESET}")
    subprocess.run(["python", tool_path, *extra_args], check=True)
    print(f"{Color.GREEN}[INF]Finished running {tool_name}.{Color.RESET}")


def run_workflow(workflow_name: str, extra_args: Optional[List[str]] = None):
    global workflows
    if workflow_name not in workflows:
        raise ValueError(f"Workflow '{workflow_name}' not found.")
    if extra_args is None:
        extra_args = []
    workflow = workflows[workflow_name]
    for tool_name in workflow:
        if tool_name not in tools:
            print(f"Tool '{tool_name}' not found.")
            raise ValueError(
                f"Tool '{tool_name}' not found in workflow '{workflow_name}'."
            )
        run_tool(tool_name, extra_args=extra_args)


def display_help():
    print(f"{Color.CYAN}Available commands:")
    print(
        "\t<name> - Run a specific tool or workflow.\n"
        "\t\tNOTE: This is case-sensitive and will prioritize workflows if names overlap."
    )
    print("\ttool:<tool_name> - Run a specific tool.")
    print("\tworkflow:<workflow_name> - Run a specific workflow.")
    print(
        f"{Color.YELLOW}Note: Use 'tool:' or 'workflow:' prefix to specify the type explicitly.{Color.RESET}"
    )


def arg_parser() -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(
        description="Run tools or workflows from the tool directory."
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Name of the tool or workflow to run. Use 'tool:<name>' or 'workflow:<name>' for explicit selection.",
        default=None,
    )
    return parser.parse_known_args()


def display_found_items():
    print(end=f"{Color.CYAN}")
    print("--" * 20)
    print(f"Tools found:{Color.WHITE}")
    for name, path in tools.items():
        print(f"{Color.MAGENTA}{name}{Color.RESET}: {Color.GREEN}{path}{Color.RESET}")

    print(end=f"{Color.CYAN}")
    print("--" * 20)
    print(f"Workflows found:{Color.WHITE}")
    for name, workflow in workflows.items():
        print(
            f"{Color.MAGENTA}{name}{Color.RESET}: {Color.GREEN}{f'{Color.RESET} -> {Color.GREEN}'.join(workflow)}{Color.RESET}"
        )

    print(end=f"{Color.CYAN}")
    print(f"--" * 20, end=f"{Color.RESET}\n")


def operate() -> str:
    display_help()
    display_found_items()

    name = input(
        f"{Color.YELLOW}Enter the workflow or tool name to run: {Color.RESET}"
    ).strip()
    return name


def main():
    args, unknown = arg_parser()
    name: str = args.name
    if not name:
        name = operate()

    if not name:
        print(f"{Color.YELLOW}[WRN]Exiting...{Color.RESET}")
        return
    if name.startswith("workflow:"):
        run_workflow(name.split("workflow:")[1].strip())
        return
    elif name.startswith("tool:"):
        run_tool(name.split("tool:")[1].strip())
        return

    if name in workflows:
        run_workflow(name, extra_args=unknown)
    elif name in tools:
        run_tool(name, extra_args=unknown)
    else:
        raise ValueError(
            f"{Color.RED}[ERR]'{name}' is neither a tool nor a workflow.{Color.RESET}"
        )


if __name__ == "__main__":
    load_tools()
    load_workflows()
    main()
