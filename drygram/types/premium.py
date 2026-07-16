# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from dataclasses import dataclass
from typing import Optional
from drygram.types.base import BaseType

@dataclass(slots=True)
class StarPayment(BaseType):
    transaction_id: str
    amount: int
    date: int
    source: str

@dataclass(slots=True)
class Gift(BaseType):
    id: str
    name: str
    emoji: str
    cost_stars: int
    is_upgraded: bool = False

@dataclass(slots=True)
class GiftUpgrade(BaseType):
    id: str
    gift_id: str
    new_emoji: str
    upgrade_cost_stars: int

@dataclass(slots=True)
class Collectible(BaseType):
    id: str
    title: str
    type: str
    address: str

@dataclass(slots=True)
class PremiumEmojiStatus(BaseType):
    emoji_id: str
    document_id: Optional[str] = None
    expiration_date: Optional[int] = None
