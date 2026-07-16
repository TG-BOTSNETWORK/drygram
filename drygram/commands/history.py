# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import time
from typing import List, Optional

class CommandHistoryRecord:
    """Represents a single command execution log record."""
    def __init__(
        self,
        command_name: str,
        user_id: Optional[int],
        chat_id: Optional[int],
        timestamp: float,
        success: bool,
        error: Optional[str] = None
    ):
        self.command_name = command_name
        self.user_id = user_id
        self.chat_id = chat_id
        self.timestamp = timestamp
        self.success = success
        self.error = error

class CommandHistory:
    """
    Keeps an in-memory audit log of all command calls.
    """
    def __init__(self):
        self.records: List[CommandHistoryRecord] = []

    def log_call(
        self,
        command_name: str,
        user_id: Optional[int],
        chat_id: Optional[int],
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """Add a new execution record to history."""
        self.records.append(
            CommandHistoryRecord(command_name, user_id, chat_id, time.time(), success, error)
        )

_global_history = CommandHistory()

def get_history() -> list:
    """Retrieve the global history list of records."""
    return _global_history.records
