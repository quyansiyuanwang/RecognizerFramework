from .WorkflowEngine import ExecutorManager, WorkflowManager


def execute_workflow(
    workflow: WorkflowManager, await_all: bool = False, verbose: bool = True
) -> None:
    exe = ExecutorManager[str](workflow=workflow)
    results = exe.await_run_all() if await_all else exe.run()
    if verbose:
        for result in results:
            print(result)
    elif not await_all:
        tuple(result for result in results)  # Ensure results are processed


def run(path: str, await_all: bool = False, verbose: bool = True) -> None:
    workflow = WorkflowManager(path)
    execute_workflow(workflow, await_all=await_all, verbose=verbose)
