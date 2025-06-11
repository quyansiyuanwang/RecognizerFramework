from ..Structure import Job


class ExecutionError(Exception):
    def __init__(self, job: Job, message: str):
        super().__init__(f"Execution error in job '{job}': \n{message}")
        self.job: Job = job
        self.message: str = message


class JobTypeError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Job type error: " + message)
        self.job: Job = job
        self.message: str = message


class JobNotFoundError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Job not found: " + message)
        self.job: Job = job


class ROIError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "ROI error occurred: " + message)
        self.job: Job = job


class TemplateError(ROIError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Template error occurred: " + message)
        self.job: Job = job


class MatchingError(ROIError):
    def __init__(self, job: Job, message: str):
        super().__init__(job=job, message="Matching error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class ActionError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Action error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class ArgumentError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "(Keyword)Argument error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class LogLevelError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Log level error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class OverloadError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Overload error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class RecursiveError(OverloadError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Recursive overload error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class NeededError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Needed error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class RetryError(ExecutionError):
    def __init__(self, job: Job, message: str):
        super().__init__(job, "Retry error occurred: " + message)
        self.job: Job = job
        self.message: str = message


class WorkflowError(Exception):
    def __init__(self, job: Job, message: str):
        super().__init__(f"Workflow error in job '{job}': {message}")
        self.job: Job = job
        self.message: str = message
