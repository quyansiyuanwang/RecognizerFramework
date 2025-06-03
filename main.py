from typing import List

from src.WorkflowEngine import ExecutorManager, WorkflowManager


def main() -> None:
    manager = WorkflowManager("workflow/example.json")
    # for name, job in manager.items():
    #     print(f"{name}: {job}")

    exe = ExecutorManager(workflow=manager)
    results: List[str] = exe.run()
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
