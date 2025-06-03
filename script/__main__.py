import json
import os
import subprocess
from typing import Dict, List

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
        if f.endswith(".py") and f != os.path.basename(__file__)
    ]

    for py_file in python_files:
        file_path = os.path.join(current_dir, py_file)
        name = os.path.splitext(py_file)[0]
        scripts[name] = file_path


def run_script(script_name: str):
    global scripts
    if script_name not in scripts:
        print(f"Script '{script_name}' not found.")
        return

    script_path = scripts[script_name]
    print(f"Running {script_name}...")
    subprocess.run(["python", script_path], check=True)
    print(f"Finished running {script_name}.")


def run_workflow(workflow_name: str):
    global workflows
    if workflow_name not in workflows:
        print(f"Workflow '{workflow_name}' not found.")
        return

    workflow = workflows[workflow_name]
    for script_name in workflow:
        if script_name not in scripts:
            print(f"Script '{script_name}' not found.")
            continue
        run_script(script_name)


def display_help():
    print("Available commands:")
    print(
        "\t<name> - Run a specific script or workflow.\n"
        "\t\tNOTE: This is case-sensitive and will prioritize workflows if names overlap."
    )
    print("\tscript:<script_name> - Run a specific script.")
    print("\tworkflow:<workflow_name> - Run a specific workflow.")
    print()


def main():
    display_help()
    load_scripts()
    load_workflows()

    print("--" * 20)
    print("Scripts found:")
    for name, path in scripts.items():
        print(f"{name}: {path}")

    print("--" * 20)
    print("Workflows found:")
    for name, workflow in workflows.items():
        print(f"{name}: {workflow}")

    print("--" * 20)

    name = input("Enter the workflow or script name to run: ").strip()
    if not name:
        print("Exiting...")
        return
    if name.startswith("workflow:"):
        run_workflow(name.split("workflow:")[1].strip())
        return
    elif name.startswith("script:"):
        run_script(name.split("script:")[1].strip())
        return

    if name in workflows:
        run_workflow(name)
    elif name in scripts:
        run_script(name)
    else:
        print(f"'{name}' is neither a script nor a workflow.")


if __name__ == "__main__":
    main()
