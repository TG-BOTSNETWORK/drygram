# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass, field
from typing import Optional, List, Union, Any
from drygram.types.base import BaseType
from drygram.types.chat import User, Chat

@dataclass(slots=True)
class MessageEffect(BaseType):
    """
    Representation of a message effect.

    Parameters
    ----------
    id : str
        Effect identifier.
    name : str
        Human readable name.
    emoji : str
        Emoji associated with the effect.
    """
    id: str
    name: str
    emoji: str

@dataclass(slots=True)
class CloudDraft(BaseType):
    """
    Representation of a message cloud draft.

    Parameters
    ----------
    text : str
        Draft text.
    entities : List[dict], default=list
        Parsed styling entity tags.
    date : int, default=0
        Draft save date unix timestamp.
    """
    text: str
    entities: List[dict] = field(default_factory=list)
    date: int = 0

@dataclass(slots=True)
class Message(BaseType):
    """
    Representation of a chat room message.

    Parameters
    ----------
    id : int
        Message identifier.
    date : int
        Unix time of sending.
    chat : Chat
        Chat room reference.
    sender : Union[User, Chat]
        Sender profile.
    text : Optional[str], default=None
        Message body text.
    entities : List[dict], default=list
        Formatting entities list.
    reply_to_message : Optional[Any], default=None
        Reply reference.
    forward_from : Optional[Union[User, Chat]], default=None
        Original forward sender.
    edit_date : Optional[int], default=None
        Unix time of edit.
    effect_id : Optional[str], default=None
        Active message effect ID.
    media : Optional[Any], default=None
        Media attachment reference.
    markup : Optional[Any], default=None
        Keyboard markup payload.
    """
    id: int
    date: int
    chat: Chat
    sender: Union[User, Chat]
    text: Optional[str] = None
    entities: List[dict] = field(default_factory=list)
    reply_to_message: Optional[Any] = None
    forward_from: Optional[Union[User, Chat]] = None
    edit_date: Optional[int] = None
    effect_id: Optional[str] = None
    media: Optional[Any] = None
    markup: Optional[Any] = None
