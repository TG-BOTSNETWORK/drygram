# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass, field
from typing import Optional, List, Any
from drygram.types.base import BaseType

@dataclass(slots=True)
class StoryReaction(BaseType):
    emoji: str
    count: int = 1

@dataclass(slots=True)
class StoryPrivacy(BaseType):
    privacy_type: str
    allowed_users: List[int] = field(default_factory=list)
    denied_users: List[int] = field(default_factory=list)

@dataclass(slots=True)
class Story(BaseType):
    id: int
    sender_id: int
    media: Any
    caption: Optional[str] = None
    date: int = 0
    privacy: Optional[StoryPrivacy] = None
    reactions: List[StoryReaction] = field(default_factory=list)

@dataclass(slots=True)
class StoryArchive(BaseType):
    stories: List[Story] = field(default_factory=list)
