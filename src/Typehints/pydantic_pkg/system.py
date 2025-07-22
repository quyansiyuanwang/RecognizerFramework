from typing import Dict, List, Literal, Optional, TypeAlias

from pydantic import BaseModel, Field

LogLevelLiteral: TypeAlias = Literal[
    "LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
]


class System_Log(BaseModel):
    message: str = Field(..., description="日志消息, 必须提供")
    levels: List[LogLevelLiteral] = Field(
        ..., description="日志级别, 可选: LOG, DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    returns: Dict[str, Literal["type", "message", "levels"]] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['type', 'message', 'levels'], 以键为变量, 值指定返回参数"
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )


class System_Command(BaseModel):
    command: str = Field(..., description="要执行的命令, 必须提供")
    args: List[str] = Field([], description="命令参数列表, 可选")
    shell: bool = Field(True, description="是否在shell中执行命令, 可选")
    wait: bool = Field(True, description="是否等待命令执行完成, 可选")
    cwd: str = Field(str(), description="命令执行时的工作目录, 可选")
    env: Dict[str, str] = Field(
        default_factory=dict,
        description="环境变量字典, 可选, 用于设置命令执行时的环境变量",
    )
    ignore: bool = Field(
        False,
        description="是否忽略命令执行错误, 可选, 默认为False表示不忽略",
    )
    returns: Dict[
        str,
        Literal[
            "command",
            "args",
            "env",
            "shell",
            "cwd",
            "wait",
            "full_command",
            "type",
        ],
    ] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['command', 'args', 'env', 'shell', 'cwd', 'wait', 'full_command', 'type'], "
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )


class System(BaseModel):
    type: Literal["Delay", "Paste", "Log", "Command"] = Field(
        ...,
        description="系统操作类型, 可选: Delay(延时), Paste(粘贴), Log(日志记录), Command(命令执行)",
    )
    duration: int = Field(0, description="延时操作定义, 仅在type为Delay时有效")
    log: Optional[System_Log] = Field(
        None,
        description="日志记录定义, 仅在type为Log时有效, 包含消息和级别等",
    )
    command: Optional[System_Command] = Field(
        None,
        description="命令执行定义, 仅在type为Command时有效, 包含命令、参数、环境变量等",
    )
    returns: Dict[str, Literal["type", "duration", "content"]] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['type', 'duration', 'content'], 以键为变量, 值指定返回参数"
            "可在其他Job中使用use指定该job返回的参数"
        ),
    )
