# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass
from typing import Optional
from drygram.types.base import BaseType

@dataclass(slots=True)
class BusinessConnection(BaseType):
    id: str
    user_id: int
    dc_id: int
    can_reply: bool = True

@dataclass(slots=True)
class BusinessLink(BaseType):
    url: str
    message: str
    title: Optional[str] = None
    views: int = 0

@dataclass(slots=True)
class BusinessGreeting(BaseType):
    message: str
    trigger_hours: Optional[str] = None

@dataclass(slots=True)
class BusinessAway(BaseType):
    message: str
    trigger_offline: bool = True

@dataclass(slots=True)
class BusinessReply(BaseType):
    shortcut: str
    message: str
