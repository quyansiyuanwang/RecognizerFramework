from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .input import Input
from .roi import ROI
from .system import System


class Delay(BaseModel):
    pre: Optional[int] = Field(0, ge=0, description="前置延时(ms), 任务执行前等待时间")
    post: Optional[int] = Field(0, ge=0, description="后置延时(ms), 任务执行后等待时间")


class After(BaseModel):
    success: List[str] = Field(
        list(), description="成功时的任务名列表, 任务完成后逐个执行"
    )
    failure: List[str] = Field(
        list(), description="失败时的任务名列表, 任务完成后逐个执行"
    )
    always: List[str] = Field(
        list(), description="无论成功或失败都执行的任务名列表, 任务完成后逐个执行"
    )
    ignore_errors: bool = Field(False, description="是否忽略错误")


class Next(BaseModel):
    success: Optional[str] = Field(str(), description="成功时的下一个任务名")
    failure: Optional[str] = Field(str(), description="失败时的下一个任务名")


class Limits(BaseModel):
    maxCount: Optional[int] = Field(-1, ge=1, description="最大执行次数, 默认不限制")
    maxFailure: Optional[int] = Field(-1, ge=0, description="最大失败次数, 默认不限制")
    maxSuccess: Optional[int] = Field(-1, ge=0, description="最大成功次数, 默认不限制")
    exit: Optional[str] = Field(
        None,
        description="达到最大次数后退出的任务名, 如果为空(null)则退出, 否则切换到指定任务",
    )


class Job(BaseModel):
    type: Literal["ROI", "OCR", "Input", "System", "Overload"] = Field(
        ...,
        description="任务类型, 可选: ROI(区域识别), OCR(文字识别), Input(输入操作), System(系统操作), Overload(继承)",
    )

    roi: Optional[ROI] = Field(
        None, description="ROI任务定义, 仅在type为ROI时有效, 包含图像和区域信息"
    )
    # ocr: TODO
    input: Optional[Input] = Field(
        None, description="输入操作定义, 仅在type为Input时有效, 包含鼠标/键盘/文本输入"
    )
    system: Optional[System] = Field(
        None, description="系统操作定义, 仅在type为System时有效"
    )

    overload: Optional[str] = Field(
        None,
        description="继承的任务名, 仅在type为Overload时有效, 允许继承其他任务的定义",
    )
    description: Optional[str] = Field(str(), description="任务描述, 便于理解用途")
    after: Optional[After] = Field(
        None, description="使用的任务名列表, 任务完成后逐个执行"
    )
    next: Optional[Union[str, Next]] = Field(
        None, description="下一个任务名或分支, 支持 success/failure 分支"
    )
    delay: Optional[Delay] = Field(None, description="延时设置, 控制任务前中后等待时间")
    limits: Optional[Limits] = Field(
        None, description="任务执行限制, 包含最大执行次数、失败次数等"
    )
    needs: Optional[List[str]] = Field(
        list(), description="依赖的前置任务名, 只有全部完成后才会执行本任务"
    )


class LogConfig(BaseModel):
    level: Optional[Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]] = (
        Field(
            None,
            description="日志级别, 可选: LOG, DEBUG, INFO, WARNING, ERROR, CRITICAL",
        )
    )
    file: Optional[str] = Field(
        str(), description="日志文件路径, 如果为None则不写入文件"
    )
    format: Optional[str] = Field(
        "%(levelname)s - %(asctime)s - %(message)s",
        description="日志格式化字符串",
    )
    datefmt: Optional[str] = Field(
        "%Y-%m-%d %H:%M:%S.%f", description="日期时间格式化字符串"
    )
    clear: Optional[bool] = Field(False, description="是否清空日志")


class IdentifiedGlobals(BaseModel):
    debug: Optional[bool] = Field(False, description="调试模式, 开启后输出详细日志")
    colorful: Optional[bool] = Field(True, description="彩色日志输出")
    ignore: Optional[bool] = Field(False, description="忽略错误")
    logConfig: Optional[LogConfig] = Field(None, description="日志配置")


Globals = Union[IdentifiedGlobals, Dict[str, Any]]


class Workflow(BaseModel):
    begin: str = Field(..., description="起始任务名, 必须是 jobs 中的一个 key")
    globals: Optional[Globals] = Field(None, description="全局配置, 影响所有任务")
    jobs: Dict[str, Job] = Field(
        ..., description="所有任务节点, key为任务名, value为Job定义"
    )
