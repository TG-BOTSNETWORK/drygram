# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import re
from typing import Callable, Any, Union, Dict

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
        self._cache: Dict[int, bool] = {}

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
        event_id = id(event)
        if event_id in self._cache:
            return self._cache[event_id]
        try:
            res = self.check(event)
        except Exception:
            res = False
        self._cache[event_id] = res
        return res

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

    def __xor__(self, other: "Gate") -> "Gate":
        """
        Exclusive OR combination.

        Parameters
        ----------
        other : Gate
            Additional Gate to combine.

        Returns
        -------
        Gate
            XOR Gate.
        """
        return Gate(lambda event: self(event) ^ other(event))

# TEXT GATES
class TextGate(Gate):
    def __init__(self, text: str):
        super().__init__(lambda event: hasattr(event, "text") and event.text == text)

class CaptionGate(Gate):
    def __init__(self, caption: str):
        super().__init__(lambda event: hasattr(event, "caption") and event.caption == caption)

class RegexGate(Gate):
    def __init__(self, pattern: str):
        compiled = re.compile(pattern)
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and bool(compiled.search(event.text)))

class MarkdownGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") in ("bold", "italic") for e in event.entities))

class HtmlGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") in ("bold", "italic") for e in event.entities))

class StartsWithGate(Gate):
    def __init__(self, prefix: str):
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and event.text.startswith(prefix))

class EndsWithGate(Gate):
    def __init__(self, suffix: str):
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and event.text.endswith(suffix))

class ContainsGate(Gate):
    def __init__(self, value: str):
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and value in event.text)

class LengthGate(Gate):
    def __init__(self, min_len: int, max_len: int):
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and min_len <= len(event.text) <= max_len)

class LanguageGate(Gate):
    def __init__(self, lang: str):
        super().__init__(lambda event: hasattr(event, "sender") and getattr(event.sender, "language_code", "") == lang)

class EmojiGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and len(event.text) == 1)

class PremiumEmojiGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "custom_emoji" for e in event.entities))

class HashtagGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "hashtag" for e in event.entities))

class MentionGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "mention" for e in event.entities))

class URLGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "url" for e in event.entities))

class EmailGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "email" for e in event.entities))

class NumberGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "text") and event.text is not None and event.text.isdigit())

class CodeBlockGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "pre" for e in event.entities))

class QuoteGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "blockquote" for e in event.entities))

class SpoilerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "entities") and any(e.get("type") == "spoiler" for e in event.entities))

# MEDIA GATES
class MediaGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and event.media is not None)

class ImageGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("photo"))

class PhotoGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("photo"))

class VideoGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("video"))

class AnimationGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("animation"))

class GifGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("gif"))

class DocumentGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("doc"))

class ArchiveGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_name", "").endswith(".zip"))

class VoiceGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("voice"))

class AudioGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("audio"))

class MusicGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("audio"))

class VideoNoteGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("videonote"))

class StickerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("sticker"))

class PremiumStickerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("sticker"))

class AnimatedStickerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("sticker"))

class VectorStickerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "file_unique_id", "").startswith("sticker"))

class AlbumGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "media") and getattr(event.media, "id", None) is not None)

# CHAT GATES
class PrivateGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") == "private")

class GroupGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") in ("group", "supergroup"))

class SuperGroupGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") == "supergroup")

class BroadcastGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") == "channel")

class ForumGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "chat") and event.chat is not None and getattr(event.chat, "type", "") == "supergroup")

class TopicGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "topic") and event.topic is not None)

class BusinessGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "is_business", False))

class SecretGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# USER GATES
class BotGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "is_bot", False))

class HumanGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and not getattr(event.sender, "is_bot", False))

class OwnerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "id", 0) == 12345678)

class AdminGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "id", 0) == 12345678)

class PremiumGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "is_premium", False))

class VerifiedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "id", 0) == 12345678)

class ScamGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class FakeGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class SupportGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class DeveloperGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "id", 0) == 12345678)

# SERVICE GATES
class JoinGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class LeaveGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class PromoteGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class DemoteGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class TitleGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class PhotoChangedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class PinnedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class MigrationGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# CALL GATES
class VoiceCallGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class VideoCallGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class ParticipantGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class SpeakerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class MutedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class ScreenShareGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# BUSINESS GATES
class GreetingGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class AwayGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class QuickReplyGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class BusinessLinkGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class BusinessMessageGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class BusinessStoryGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# PREMIUM GATES
class PremiumFeatureGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class BoostGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class StarGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class GiftGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class CollectibleGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class EffectGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class StoryGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class StoryReplyGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class StoryReactionGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class StoryArchiveGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# REACTIONS GATES
class ReactionGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class CustomReactionGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class EmojiReactionGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# EVENTS GATES
class ScheduledGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class EditedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class DeletedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class ForwardedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "forward_from") and event.forward_from is not None)

class ReplyGate(Gate):
    def __init__(self):
        super().__init__(lambda event: hasattr(event, "reply_to_message") and event.reply_to_message is not None)

class PinnedMessageGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class MentionedGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class AutoDeleteGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

# SYSTEM GATES
class FloodWaitGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class ConnectionGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class ReconnectGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class UpdateGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class SchedulerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class WorkerGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class PluginGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class MiddlewareGate(Gate):
    def __init__(self):
        super().__init__(lambda event: False)

class Gates:
    """
    Standard filters factory helper class.
    """

    @staticmethod
    def all_signals() -> Gate:
        return Gate(lambda event: True)

    @staticmethod
    def text(pattern: str) -> Gate:
        return Gate(lambda event: hasattr(event, "text") and event.text == pattern)

    @staticmethod
    def regex(pattern: str) -> Gate:
        compiled = re.compile(pattern)
        return Gate(lambda event: hasattr(event, "text") and event.text is not None and bool(compiled.search(event.text)))

    @staticmethod
    def private() -> Gate:
        return PrivateGate()

    @staticmethod
    def group() -> Gate:
        return GroupGate()

    @staticmethod
    def channel() -> Gate:
        return BroadcastGate()

    @staticmethod
    def sender(user_id: int) -> Gate:
        return Gate(lambda event: hasattr(event, "sender") and event.sender is not None and getattr(event.sender, "id", None) == user_id)

    @staticmethod
    def premium() -> Gate:
        return PremiumGate()

    @staticmethod
    def business() -> Gate:
        return BusinessGate()
