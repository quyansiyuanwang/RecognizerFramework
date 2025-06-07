from src.WorkflowEngine import ExecutorManager, WorkflowManager


def test():
    workflow = WorkflowManager("workflow/QQ_Sent_Msg.json")
    exe = ExecutorManager[str](workflow=workflow)
    for result in exe.run():
        print(result)


if __name__ == "__main__":
    test()
