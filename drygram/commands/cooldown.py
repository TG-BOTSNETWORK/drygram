# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import time
from typing import Dict, List, Tuple, Union

class CooldownManager:
    """
    Tracks and restricts rate-limited calls per user or per chat.
    """
    def __init__(self, rate: int = 1, per: float = 5.0):
        self.rate = rate
        self.per = per
        self.history: Dict[Union[int, str], List[float]] = {}

    def check_cooldown(self, key: Union[int, str]) -> Tuple[bool, float]:
        """
        Check if the key is under cooldown limitation.
        Returns:
            (is_limited, time_remaining)
        """
        now = time.time()
        if key not in self.history:
            self.history[key] = []
            
        # Clean timestamps older than cooldown window
        self.history[key] = [t for t in self.history[key] if now - t < self.per]
        
        if len(self.history[key]) >= self.rate:
            oldest = self.history[key][0]
            remaining = self.per - (now - oldest)
            return True, max(0.0, remaining)
            
        return False, 0.0

    def update_cooldown(self, key: Union[int, str]) -> None:
        """Record an execution timestamp for the key."""
        now = time.time()
        if key not in self.history:
            self.history[key] = []
        self.history[key].append(now)
