from typing import List, Literal, Optional

from pydantic import BaseModel, Field

LogLevelLiteral = Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class System_Log(BaseModel):
    message: str = Field(..., description="日志消息, 必须提供")
    levels: List[LogLevelLiteral] = Field(
        ..., description="日志级别, 可选: LOG, DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )


class System(BaseModel):
    type: Literal["Delay", "Paste", "Log"] = Field(
        ...,
        description="系统操作类型, 可选: Delay(延时), Paste(粘贴), Log(日志记录)",
    )
    duration: Optional[int] = Field(
        0, description="延时操作定义, 仅在type为Delay时有效"
    )
    log: Optional[System_Log] = Field(
        None,
        description="日志记录定义, 仅在type为Log时有效, 包含消息和级别等",
    )
