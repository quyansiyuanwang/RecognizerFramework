from typing import Any, Dict

from ...Models.calculate import Calculate
from ...Models.globals import Globals
from ...Typehints.structure import TaskReturnsDict
from ..Controller import CalculateController, LogLevel, global_log_manager
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("Calculate")
class CalculateExecutor(Executor):
    def __init__(self, job: Job, globals: Globals) -> None:
        self.job: Job = job
        self.globals: Globals = globals
        self.use_vars: Dict[str, Any] = {}

    def calculate_expression(self, calculate: Calculate) -> Dict[str, float]:
        expressions = calculate.expressions
        cv: Dict[str, float] = CalculateController.calculate(expressions, self.use_vars)
        global_log_manager.log(
            msg=f"Calculated values: {cv}",
            levels=[LogLevel.INFO, LogLevel.DEBUG],
            debug=self.globals.debug,
            log_config=self.globals.logConfig,
        )

        return cv

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[str]:
        self.use_vars.update(kwargs)
        calculate = self.job.calculate
        if calculate is None:
            raise ValueError("Calculate job must have a 'calculate' field defined")
        cv = self.calculate_expression(calculate=calculate)

        return TaskReturnsDict(
            result=f"Calculate executed successfully, vars: {cv}",
            returns=calculate.returns,
            variables=cv,
        )
