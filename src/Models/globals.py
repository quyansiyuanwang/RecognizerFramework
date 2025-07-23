from pydantic import BaseModel, Field

from .system import LogLevelLiteral as _LogLevelLiteral


class LogConfig(BaseModel):
    level: _LogLevelLiteral = Field(
        default="LOG",
        description="日志级别, 可选: LOG, DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )
    file: str = Field(default=str(), description="日志文件路径, 如果为None则不写入文件")
    format: str = Field(
        default="%(levelname)s - %(asctime)s - %(message)s",
        description="日志格式化字符串",
    )
    datefmt: str = Field(
        default="%Y-%m-%d %H:%M:%S.%f", description="日期时间格式化字符串"
    )
    clear: bool = Field(default=False, description="是否清空日志")


class Globals(BaseModel):
    debug: bool = Field(default=False, description="调试模式, 开启后输出详细日志")
    colorful: bool = Field(default=True, description="彩色日志输出")
    ignore: bool = Field(default=False, description="忽略错误")
    logConfig: LogConfig = Field(default_factory=LogConfig, description="日志配置")

    class Config:
        extra = "allow"  # 允许未知字段


__all__ = [
    "Globals",
    "LogConfig",
]
