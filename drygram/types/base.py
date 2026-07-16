# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass, asdict

@dataclass(slots=True)
class BaseType:
    def to_dict(self) -> dict:
        return asdict(self)
