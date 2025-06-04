from typing import Any

from src.WorkflowEngine import ExecutorManager, WorkflowManager


def main() -> None:
    manager = WorkflowManager("workflow/example.json")
    exe = ExecutorManager[Any](workflow=manager)
    results = exe.run()
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
