# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Any, Optional, Type

class Argument:
    """
    Represents a positional or flag argument specification for a command.
    """
    def __init__(
        self,
        name: str,
        type: Type = str,
        default: Any = None,
        required: bool = True,
        description: str = ""
    ):
        self.name = name
        self.type = type
        self.default = default
        self.required = required
        self.description = description

class IntArg(Argument):
    def __init__(self, name: str, required: bool = True, description: str = ""):
        super().__init__(name, type=int, required=required, description=description)

class EnumArg(Argument):
    def __init__(self, name: str, enum_cls: Any, required: bool = True, description: str = ""):
        super().__init__(name, type=enum_cls, required=required, description=description)
