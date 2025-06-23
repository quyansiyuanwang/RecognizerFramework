import argparse
import sys

from src.WorkflowEngine import ExecutorManager, WorkflowManager


def args_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some json workflows.")
    parser.add_argument(
        "input",
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

    args = parser.parse_args(sys.argv[1:])
    return args


def execute_workflow(workflow: WorkflowManager, await_all: bool = False) -> None:
    exe = ExecutorManager[str](workflow=workflow)
    if await_all:
        await_results = exe.await_run_all()
        for await_result in await_results:
            print(await_result)
    else:
        flow_results = exe.run()
        for flow_result in flow_results:
            print(flow_result)


def main():
    args = args_parse()

    workflow = WorkflowManager(args.input)
    execute_workflow(workflow, args.await_all)


if __name__ == "__main__":
    main()
