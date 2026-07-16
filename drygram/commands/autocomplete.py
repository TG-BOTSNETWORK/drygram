# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import List, Union, Callable, Any

class Autocompleter:
    """
    Computes matching option suggestions for arguments in command prompts.
    """
    def __init__(self, choices: Union[List[str], Callable[[str], List[str]]]):
        self.choices = choices

    def get_suggestions(self, query: str) -> List[str]:
        """Filter choices based on the search query."""
        options = self.choices(query) if callable(self.choices) else self.choices
        query_lower = query.lower()
        return [opt for opt in options if query_lower in opt.lower()]

    @staticmethod
    def suggest(query: str, choices: List[str]) -> List[str]:
        """Static helper to filter a direct list of choices."""
        query_lower = query.lower()
        return [opt for opt in choices if query_lower in opt.lower()]

CommandAutocomplete = Autocompleter
