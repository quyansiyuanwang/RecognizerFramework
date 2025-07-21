from typing import Dict, List, Literal, NotRequired, TypedDict

LogLevelLiteral = Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LogDict(TypedDict):
    message: str
    levels: List[LogLevelLiteral]

    returns: NotRequired[Dict[str, Literal["type", "message", "levels"]]]


class CommandDict(TypedDict):
    command: str
    args: NotRequired[List[str]]
    env: NotRequired[Dict[str, str]]
    shell: NotRequired[bool]
    cwd: NotRequired[str]
    wait: NotRequired[bool]
    ignore: NotRequired[bool]

    returns: NotRequired[
        Dict[
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
        ]
    ]


class SystemDict(TypedDict):
    # Required fields
    type: Literal["Delay", "Log", "Paste", "Command"]

    # Optional fields
    duration: NotRequired[int]

    log: NotRequired[LogDict]
    command: NotRequired[CommandDict]

    returns: NotRequired[Dict[str, Literal["type", "duration", "content"]]]
