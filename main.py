from src.WorkflowEngine import ExecutorManager, WorkflowManager


def main():
    workflow = WorkflowManager("workflow/SkyFire.json")
    # workflow = WorkflowManager("workflow/test.json")
    exe = ExecutorManager[str](workflow=workflow)
    for result in exe.run():
        print(result)


if __name__ == "__main__":
    main()
