# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass, field
from typing import Optional, List
from drygram.types.base import BaseType

@dataclass(slots=True)
class Photo(BaseType):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int

@dataclass(slots=True)
class Video(BaseType):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    file_size: int

@dataclass(slots=True)
class Document(BaseType):
    file_id: str
    file_unique_id: str
    file_name: str
    mime_type: str
    file_size: int

@dataclass(slots=True)
class Audio(BaseType):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_size: Optional[int] = None

@dataclass(slots=True)
class VoiceNote(BaseType):
    file_id: str
    file_unique_id: str
    duration: int
    waveform: Optional[bytes] = None
    file_size: Optional[int] = None

@dataclass(slots=True)
class VideoNote(BaseType):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    file_size: Optional[int] = None

@dataclass(slots=True)
class Location(BaseType):
    latitude: float
    longitude: float

@dataclass(slots=True)
class LiveLocation(BaseType):
    latitude: float
    longitude: float
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None

@dataclass(slots=True)
class WebApp(BaseType):
    url: str
    title: str

@dataclass(slots=True)
class MiniApp(BaseType):
    url: str
    title: str

@dataclass(slots=True)
class PollOption(BaseType):
    text: str
    voter_count: int = 0

@dataclass(slots=True)
class Poll(BaseType):
    id: str
    question: str
    options: List[PollOption] = field(default_factory=list)
    total_voter_count: int = 0
    is_closed: bool = False

@dataclass(slots=True)
class Quiz(BaseType):
    id: str
    question: str
    options: List[PollOption] = field(default_factory=list)
    correct_option_id: int = 0
    total_voter_count: int = 0

@dataclass(slots=True)
class MediaGroup(BaseType):
    id: str
    media_list: List[BaseType] = field(default_factory=list)
