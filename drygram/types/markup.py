# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass, field
from typing import Optional, List, Union
from drygram.types.base import BaseType

@dataclass(slots=True)
class KeyboardButton(BaseType):
    """
    Representation of a Reply Keyboard button.

    Parameters
    ----------
    text : str
        Button label text.
    request_contact : bool, default=False
        True to request contact phone sharing.
    request_location : bool, default=False
        True to request location sharing.
    request_poll : bool, default=False
        True to request poll builder modal.
    request_user : bool, default=False
        True to request user picker modal.
    request_chat : bool, default=False
        True to request chat/channel picker modal.
    """
    text: str
    request_contact: bool = False
    request_location: bool = False
    request_poll: bool = False
    request_user: bool = False
    request_chat: bool = False

@dataclass(slots=True)
class InlineKeyboardButton(BaseType):
    """
    Representation of an Inline Keyboard button.

    Parameters
    ----------
    text : str
        Button label text.
    callback_data : Optional[str], default=None
        Associated query callback data.
    url : Optional[str], default=None
        Hyperlink URL.
    switch_inline_query : Optional[str], default=None
        Auto switch inline query prefix string.
    web_app_url : Optional[str], default=None
        Web App URL.
    business_chat_link : Optional[str], default=None
        Telegram Business link.
    login_url : Optional[str], default=None
        Redirect authentication URL.
    copy_text : Optional[str], default=None
        Text clipboard string.
    premium_gift_code : Optional[str], default=None
        Telegram Premium code.
    """
    text: str
    callback_data: Optional[str] = None
    url: Optional[str] = None
    switch_inline_query: Optional[str] = None
    web_app_url: Optional[str] = None
    business_chat_link: Optional[str] = None
    login_url: Optional[str] = None
    copy_text: Optional[str] = None
    premium_gift_code: Optional[str] = None

@dataclass(slots=True)
class ReplyKeyboardMarkup(BaseType):
    """
    Reply Keyboard Layout.

    Parameters
    ----------
    keyboard : List[List[KeyboardButton]], default=list
        Grid list of buttons.
    resize_keyboard : bool, default=True
        True to automatically downscale keyboard height.
    one_time_keyboard : bool, default=False
        True to auto-hide keyboard after single click.
    selective : bool, default=False
        True to only render to targeted users.
    """
    keyboard: List[List[KeyboardButton]] = field(default_factory=list)
    resize_keyboard: bool = True
    one_time_keyboard: bool = False
    selective: bool = False

@dataclass(slots=True)
class InlineKeyboardMarkup(BaseType):
    """
    Inline Keyboard Layout.

    Parameters
    ----------
    inline_keyboard : List[List[InlineKeyboardButton]], default=list
        Grid list of inline buttons.
    """
    inline_keyboard: List[List[InlineKeyboardButton]] = field(default_factory=list)
