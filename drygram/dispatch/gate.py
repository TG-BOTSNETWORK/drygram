# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import re
from typing import Callable, Any, Union

class Gate:
    """
    Check condition router gate for filtering updates.

    Parameters
    ----------
    check : Callable[[Any], bool]
        Conditional verification function.

    Attributes
    ----------
    check : Callable[[Any], bool]
        Filter condition logic.
    """

    def __init__(self, check: Callable[[Any], bool]):
        """
        Initialize the Gate.

        Parameters
        ----------
        check : Callable[[Any], bool]
            Verification logic callback.
        """
        self.check = check

    def __call__(self, event: Any) -> bool:
        """
        Check if event matches criteria.

        Parameters
        ----------
        event : Any
            The event message object.

        Returns
        -------
        bool
            True if validation matches successfully.
        """
        try:
            return self.check(event)
        except Exception:
            return False

    def __and__(self, other: "Gate") -> "Gate":
        """
        Intersect multiple Gate objects.

        Parameters
        ----------
        other : Gate
            Additional Gate to check.

        Returns
        -------
        Gate
            Combined Gate.
        """
        return Gate(lambda event: self(event) and other(event))

    def __or__(self, other: "Gate") -> "Gate":
        """
        Union multiple Gate objects.

        Parameters
        ----------
        other : Gate
            Additional Gate to check.

        Returns
        -------
        Gate
            Combined Gate.
        """
        return Gate(lambda event: self(event) or other(event))

    def __invert__(self) -> "Gate":
        """
        Negate/Invert current Gate condition.

        Returns
        -------
        Gate
            Inverted condition Gate.
        """
        return Gate(lambda event: not self(event))

class Gates:
    """
    Standard filters factory helper class.
    """

    @staticmethod
    def all_signals() -> Gate:
        """
        Match all signals.

        Returns
        -------
        Gate
            All events Gate.
        """
        return Gate(lambda event: True)

    @staticmethod
    def text(pattern: str) -> Gate:
        """
        Match strict message text content.

        Parameters
        ----------
        pattern : str
            Plaintext to match.

        Returns
        -------
        Gate
            Filter Gate.
        """
        return Gate(lambda event: hasattr(event, "text") and event.text == pattern)

    @staticmethod
    def regex(pattern: str) -> Gate:
        """
        Match text using regular expressions.

        Parameters
        ----------
        pattern : str
            Regular expression string.

        Returns
        -------
        Gate
            Regex matching Gate.
        """
        compiled = re.compile(pattern)
        return Gate(lambda event: hasattr(event, "text") and event.text is not None and bool(compiled.search(event.text)))

    @staticmethod
    def private() -> Gate:
        """
        Match private 1-on-1 chats.

        Returns
        -------
        Gate
            Private chat Gate.
        """
        return Gate(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") == "private")

    @staticmethod
    def group() -> Gate:
        """
        Match group and supergroup rooms.

        Returns
        -------
        Gate
            Group Gate.
        """
        return Gate(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") in ("group", "supergroup"))

    @staticmethod
    def channel() -> Gate:
        """
        Match channel rooms.

        Returns
        -------
        Gate
            Channel Gate.
        """
        return Gate(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") == "channel")

    @staticmethod
    def sender(user_id: int) -> Gate:
        """
        Match sender identifier.

        Parameters
        ----------
        user_id : int
            Sender user ID.

        Returns
        -------
        Gate
            Sender ID filter Gate.
        """
        return Gate(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "id", None) == user_id)

    @staticmethod
    def premium() -> Gate:
        """
        Match users holding Premium accounts.

        Returns
        -------
        Gate
            Premium filter Gate.
        """
        return Gate(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "is_premium", False))

    @staticmethod
    def business() -> Gate:
        """
        Match Business interaction events.

        Returns
        -------
        Gate
            Business filter Gate.
        """
        return Gate(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "is_business", False))
