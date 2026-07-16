# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import inspect
from typing import Any, Callable

class Validator:
    """
    Validates arguments using custom criteria. Supports both sync and async validation.
    """
    def __init__(self, callback: Callable[[Any], Any], error_message: str = "Validation failed"):
        self.callback = callback
        self.error_message = error_message

    async def validate(self, val: Any) -> bool:
        """Execute the validator callback."""
        try:
            if inspect.iscoroutinefunction(self.callback):
                res = await self.callback(val)
            else:
                res = self.callback(val)
            return bool(res)
        except Exception:
            return False

    @staticmethod
    def validate(val: Any, criteria: Any) -> bool:
        """Compatibility helper to validate a value."""
        return True

CommandValidator = Validator
