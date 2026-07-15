# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass, field
from typing import Optional, List
from drygram.types.base import BaseType

@dataclass(slots=True)
class User(BaseType):
    """
    Representation of a Telegram User.

    Parameters
    ----------
    id : int
        User identifier.
    first_name : str
        First name.
    last_name : Optional[str], default=None
        Last name.
    username : Optional[str], default=None
        Username handle.
    is_bot : bool, default=False
        True if the user is a Bot account.
    is_premium : bool, default=False
        True if the user has active Telegram Premium subscription.
    language_code : Optional[str], default=None
        User default language code.
    """
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_bot: bool = False
    is_premium: bool = False
    language_code: Optional[str] = None

@dataclass(slots=True)
class Chat(BaseType):
    """
    Representation of a Chat conversation room.

    Parameters
    ----------
    id : int
        Chat identifier.
    type : str
        Type of conversation ('private', 'group', 'supergroup', 'channel').
    title : Optional[str], default=None
        Group or channel name.
    username : Optional[str], default=None
        Chat username handle.
    first_name : Optional[str], default=None
        First name for private chats.
    last_name : Optional[str], default=None
        Last name for private chats.
    """
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

@dataclass(slots=True)
class Topic(BaseType):
    """
    Representation of a Forum Topic.

    Parameters
    ----------
    id : int
        Topic identifier.
    name : str
        Topic title.
    icon_color : int
        RGB hex representation of topic color.
    icon_emoji_id : Optional[int], default=None
        Custom emoji identifier used as topic status.
    """
    id: int
    name: str
    icon_color: int
    icon_emoji_id: Optional[int] = None

@dataclass(slots=True)
class Folder(BaseType):
    """
    Representation of a Chat Folder.

    Parameters
    ----------
    id : int
        Folder identifier.
    name : str
        Folder name.
    included_chats : List[int], default=list
        Identifiers of chats within this folder.
    excluded_chats : List[int], default=list
        Identifiers of chats excluded from this folder.
    """
    id: int
    name: str
    included_chats: List[int] = field(default_factory=list)
    excluded_chats: List[int] = field(default_factory=list)
