from src.WorkflowEngine import ExecutorManager, WorkflowManager


def test():
    workflow = WorkflowManager("workflow/test-r.json")
    for w in workflow:
        print(w)
    exe = ExecutorManager[str](workflow=workflow)
    for result in exe.run():
        print(result)


if __name__ == "__main__":
    test()
