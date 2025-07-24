import argparse
import json
import os
import subprocess
from typing import Dict, List, Optional, Tuple

from .util import Color

scripts: Dict[str, str] = {}
workflows: Dict[str, List[str]] = {}


def load_workflows():
    global workflows
    with open("script/workflows.json", "r", encoding="utf-8") as f:
        json_workflows = json.load(f)
        for name, workflow in json_workflows.items():
            workflows[name] = workflow


def load_scripts():
    global scripts
    current_dir: str = os.path.dirname(os.path.abspath(__file__))

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
        scripts[name] = file_path


def run_script(script_name: str, extra_args: Optional[List[str]] = None):
    global scripts
    if script_name not in scripts:
        print(f"{Color.RED}[ERR]Script '{script_name}' not found.{Color.RESET}")
        return
    if extra_args is None:
        extra_args = []
    script_path: str = scripts[script_name]
    print(f"{Color.YELLOW}[WRN]Running {script_name}...{Color.RESET}")
    subprocess.run(["python", script_path, *extra_args], check=True)
    print(f"{Color.GREEN}[INF]Finished running {script_name}.{Color.RESET}")


def run_workflow(workflow_name: str, extra_args: Optional[List[str]] = None):
    global workflows
    if workflow_name not in workflows:
        print(f"Workflow '{workflow_name}' not found.")
        return
    if extra_args is None:
        extra_args = []
    workflow = workflows[workflow_name]
    for script_name in workflow:
        if script_name not in scripts:
            print(f"Script '{script_name}' not found.")
            continue
        run_script(script_name, extra_args=extra_args)


def display_help():
    print(f"{Color.CYAN}Available commands:")
    print(
        "\t<name> - Run a specific script or workflow.\n"
        "\t\tNOTE: This is case-sensitive and will prioritize workflows if names overlap."
    )
    print("\tscript:<script_name> - Run a specific script.")
    print("\tworkflow:<workflow_name> - Run a specific workflow.")
    print(
        f"{Color.YELLOW}Note: Use 'script:' or 'workflow:' prefix to specify the type explicitly.{Color.RESET}"
    )


def arg_parser() -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(
        description="Run scripts or workflows from the script directory."
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Name of the script or workflow to run. Use 'script:<name>' or 'workflow:<name>' for explicit selection.",
        default=None,
    )
    return parser.parse_known_args()


def display_found_items():
    print(end=f"{Color.CYAN}")
    print("--" * 20)
    print(f"Scripts found:{Color.WHITE}")
    for name, path in scripts.items():
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
        f"{Color.YELLOW}Enter the workflow or script name to run: {Color.RESET}"
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
    elif name.startswith("script:"):
        run_script(name.split("script:")[1].strip())
        return

    if name in workflows:
        run_workflow(name, extra_args=unknown)
    elif name in scripts:
        run_script(name, extra_args=unknown)
    else:
        print(
            f"{Color.RED}[ERR]'{name}' is neither a script nor a workflow.{Color.RESET}"
        )


if __name__ == "__main__":
    load_scripts()
    load_workflows()
    main()
