from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .calculate import Calculate
from .globals import Globals
from .input import Input
from .roi import ROI
from .system import System


class Delay(BaseModel):
    pre: int = Field(default=0, ge=0, description="前置延时(ms), 任务执行前等待时间")
    post: int = Field(default=0, ge=0, description="后置延时(ms), 任务执行后等待时间")


class Before(BaseModel):
    tasks: List[str] = Field(
        default_factory=list, description="使用的任务名列表, 任务开始前逐个执行"
    )
    ignore_errors: bool = Field(default=False, description="是否忽略错误")


class After(BaseModel):
    success: List[str] = Field(
        default_factory=list, description="成功时的任务名列表, 任务完成后逐个执行"
    )
    failure: List[str] = Field(
        default_factory=list, description="失败时的任务名列表, 任务完成后逐个执行"
    )
    always: List[str] = Field(
        default_factory=list,
        description="无论成功或失败都执行的任务名列表, 任务完成后逐个执行",
    )
    ignore_errors: bool = Field(default=False, description="是否忽略错误")


class Next(BaseModel):
    success: str = Field(str(), description="成功时的下一个任务名")
    failure: str = Field(str(), description="失败时的下一个任务名")


class Limits(BaseModel):
    maxCount: int = Field(default=-1, ge=-1, description="最大执行次数, 默认不限制")
    maxFailure: int = Field(default=-1, ge=-1, description="最大失败次数, 默认不限制")
    maxSuccess: int = Field(default=-1, ge=-1, description="最大成功次数, 默认不限制")
    exit: str = Field(
        default=str(),
        description="达到最大次数后退出的任务名, 如果为空(null)则退出, 否则切换到指定任务",
    )


class Job(BaseModel):
    # exclude
    name: str = Field(
        "", exclude=True, description="任务名称，仅用于编程记录，不会出现在 schema 中"
    )

    # include
    type: Literal["ROI", "OCR", "Input", "System", "Overload", "Calculate"] = Field(
        ...,
        description="任务类型, 可选: ROI(区域识别), OCR(文字识别), Input(输入操作), System(系统操作), Overload(继承), Calculate(计算)",
    )

    roi: Optional[ROI] = Field(
        default=None, description="ROI任务定义, 仅在type为ROI时有效, 包含图像和区域信息"
    )
    # ocr: TODO
    input: Optional[Input] = Field(
        default=None,
        description="输入操作定义, 仅在type为Input时有效, 包含鼠标/键盘/文本输入",
    )
    system: Optional[System] = Field(
        default=None, description="系统操作定义, 仅在type为System时有效"
    )
    calculate: Optional[Calculate] = Field(
        default=None, description="计算任务定义, 仅在type为Calculate时有效"
    )

    overload: str = Field(
        default=str(),
        description="继承的任务名, 仅在type为Overload时有效, 允许继承其他任务的定义",
    )
    description: str = Field(str(), description="任务描述, 便于理解用途")
    before: Before = Field(
        default_factory=Before,
        description="使用的前置任务名列表, 任务开始前逐个执行",
    )
    after: After = Field(
        default_factory=After, description="使用的任务名列表, 任务完成后逐个执行"
    )
    next: Union[str, Next] = Field(
        default=str(), description="下一个任务名或分支, 支持 success/failure 分支"
    )
    delay: Delay = Field(
        default_factory=Delay, description="延时设置, 控制任务前中后等待时间"
    )
    limits: Limits = Field(
        default_factory=Limits,
        description="任务执行限制, 包含最大执行次数、失败次数等",
    )
    needs: List[str] = Field(
        default_factory=list,
        description="依赖的前置任务名, 只有全部完成后才会执行本任务",
    )
    use: str = Field(
        default=str(),
        description=("指定一个Job, 可使用=该job返回的参数"),
    )


class Workflow(BaseModel):
    begin: str = Field(default=..., description="起始任务名, 必须是 jobs 中的一个 key")
    globals: Globals = Field(
        default_factory=Globals, description="全局配置, 影响所有任务"
    )
    jobs: Dict[str, Job] = Field(
        ..., description="所有任务节点, key为任务名, value为Job定义"
    )


__all__ = [
    "Job",
    "Workflow",
    "Delay",
    "Before",
    "After",
    "Next",
    "Limits",
]
