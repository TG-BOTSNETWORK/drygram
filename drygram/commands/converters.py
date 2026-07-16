# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import enum
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse
from typing import Any, List, Tuple, Type, Union

class Converter:
    """
    Standard converters to translate raw command string tokens into typed parameters.
    """
    @staticmethod
    def to_bool(val: str) -> bool:
        return val.lower() in ("true", "1", "yes", "on", "y", "enable")

    @staticmethod
    def to_int(val: str) -> int:
        return int(val)

    @staticmethod
    def to_float(val: str) -> float:
        return float(val)

    @staticmethod
    def to_decimal(val: str) -> Decimal:
        return Decimal(val)

    @staticmethod
    def to_path(val: str) -> Path:
        return Path(val)

    @staticmethod
    def to_url(val: str) -> str:
        parsed = urlparse(val)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError(f"Invalid URL schema: {val}")
        return val

    @staticmethod
    def to_list(val: str, item_type: Type = str, sep: str = ",") -> List[Any]:
        return [Converter.convert(item.strip(), item_type) for item in val.split(sep) if item.strip()]

    @staticmethod
    def to_tuple(val: str, item_type: Type = str, sep: str = ",") -> Tuple[Any, ...]:
        return tuple(Converter.to_list(val, item_type, sep))

    @staticmethod
    def to_enum(val: str, enum_cls: Type[enum.Enum]) -> enum.Enum:
        try:
            return enum_cls[val]
        except KeyError:
            for member in enum_cls:
                if member.value == val or str(member.value).lower() == val.lower():
                    return member
            raise ValueError(f"'{val}' is not a valid {enum_cls.__name__}")

    @staticmethod
    def convert(val: str, target_type: Type) -> Any:
        if target_type == str:
            return val
        if target_type == bool:
            return Converter.to_bool(val)
        if target_type == int:
            return Converter.to_int(val)
        if target_type == float:
            return Converter.to_float(val)
        if target_type == Decimal:
            return Converter.to_decimal(val)
        if target_type == Path:
            return Converter.to_path(val)
        if isinstance(target_type, type) and issubclass(target_type, enum.Enum):
            return Converter.to_enum(val, target_type)
        return target_type(val)
