# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import List

class CompletionResult:
    """
    Holds structured suggestion details returned by autocomplete providers.
    """
    def __init__(self, query: str, matches: List[str]):
        self.query = query
        self.matches = matches

    @staticmethod
    def get_completions(cmd: str) -> List[str]:
        """Compatibility helper to return completions list."""
        return [cmd]

CommandCompletion = CompletionResult
