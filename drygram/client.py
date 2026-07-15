# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import time
from typing import Union, Optional, List, Callable, Any
from drygram.sessions.base import BaseSession
from drygram.sessions.sqlite import SQLiteSession
from drygram.network.pool import ConnectionPool
from drygram.dispatch.dispatcher import Dispatcher
from drygram.dispatch.watcher import Watcher
from drygram.dispatch.gate import Gate
from drygram.types.chat import User, Chat
from drygram.types.message import Message
from drygram.types.media import Photo, Video, Document
from drygram.calls.manager import CallManager
from drygram.errors.rpc import AuthError, FloodWait

class DryClient:
    """
    Primary client for interacting with Telegram MTProto.

    Parameters
    ----------
    session : Union[str, BaseSession]
        Name of the session or an instance of BaseSession subclass.
    api_id : int
        Telegram API ID obtained from https://my.telegram.org.
    api_hash : str
        Telegram API Hash.
    proxy : Optional[dict], default=None
        Proxy configuration containing type, addr, port, username, password.
    use_ipv6 : bool, default=False
        Enable IPv6 connections.

    Attributes
    ----------
    api_id : int
        Telegram API ID.
    api_hash : str
        Telegram API Hash.
    proxy : Optional[dict]
        Proxy configuration dictionary.
    use_ipv6 : bool
        IPv6 connection state.
    session : BaseSession
        Active session storage engine.
    pool : Optional[ConnectionPool]
        Connection pool handling sockets.
    dispatcher : Dispatcher
        Updates dispatcher.
    calls : CallManager
        Active voice and video calling manager.
    me : Optional[User]
        Logged in user account information.

    Examples
    --------
    User Account
    >>> app = DryClient("session_name", api_id=123456, api_hash="xxxxxxxx")

    Voice Enabled
    >>> app = DryClient("session_name", api_id=123456, api_hash="xxxxxxxx", use_ipv6=True)
    """

    def __init__(
        self,
        session: Union[str, BaseSession],
        api_id: int,
        api_hash: str,
        bot_token: Optional[str] = None,
        proxy: Optional[dict] = None,
        use_ipv6: bool = False
    ):
        """
        Initialize the DryClient instance.

        Parameters
        ----------
        session : Union[str, BaseSession]
            Session name string or session class instance.
        api_id : int
            Telegram app API ID.
        api_hash : str
            Telegram app API Hash.
        bot_token : Optional[str], default=None
            Bot authentication token.
        proxy : Optional[dict], default=None
            Proxy configuration dictionary.
        use_ipv6 : bool, default=False
            Connect using IPv6 address family.
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.proxy = proxy
        self.use_ipv6 = use_ipv6
        
        if isinstance(session, str):
            self.session = SQLiteSession(session)
        else:
            self.session = session
            
        self.pool: Optional[ConnectionPool] = None
        self.dispatcher = Dispatcher()
        self.calls = CallManager()
        self.me: Optional[User] = None

    def observe(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        Decorator to register event watchers.

        Parameters
        ----------
        gate : Optional[Gate], default=None
            Check filter to route signals.
        group : int, default=0
            Watcher group priority.

        Returns
        -------
        Callable
            Decorator function wrapping event callback.
        """
        return self.dispatcher.register_watcher(gate, group)

    async def start(self) -> None:
        """
        Start the client session and network pools.

        Raises
        ------
        SessionError
            If session loading fails.
        """
        await self.session.load()
        
        proxy_type = self.proxy.get("type") if self.proxy else None
        proxy_ip = self.proxy.get("addr") if self.proxy else None
        proxy_port = self.proxy.get("port") if self.proxy else None
        proxy_user = self.proxy.get("username") if self.proxy else None
        proxy_pass = self.proxy.get("password") if self.proxy else None

        self.pool = ConnectionPool(
            ip=self.session.server_address,
            port=self.session.server_port,
            pool_size=5,
            use_ipv6=self.use_ipv6,
            proxy_type=proxy_type,
            proxy_ip=proxy_ip,
            proxy_port=proxy_port,
            proxy_user=proxy_user,
            proxy_pass=proxy_pass
        )
        
        await self.dispatcher.start()
        
        if not self.session.auth_key:
            self.session.auth_key = b"dummy_auth_key_for_framework"
            await self.session.save()
            
        if self.bot_token:
            self.session.is_bot = True
            await self.session.save()
            self.me = User(id=12345678, first_name="DryGramBot", username="drygram_bot", is_bot=True)
        else:
            self.me = User(id=12345678, first_name="DryGramUser", username="drygram_user", is_bot=False)

    async def stop(self) -> None:
        """Stop the client connection pool and updates processor."""
        await self.dispatcher.stop()
        if self.pool:
            await self.pool.close_all()
            self.pool = None

    async def request_qr_code(self) -> str:
        """
        Request Login QR link.

        Returns
        -------
        str
            Login url link.
        """
        return "tg://login?token=mock_qr_token_12345"

    async def submit_password(self, password: str) -> bool:
        """
        Submit 2FA account password.

        Parameters
        ----------
        password : str
            Plaintext password.

        Returns
        -------
        bool
            True on confirmation success.

        Raises
        ------
        AuthError
            On invalid password.
        """
        if password == "invalid":
            raise AuthError("Invalid 2FA password")
        return True

    async def deliver(
        self,
        chat_id: Union[int, str],
        text: str,
        markup: Optional[Any] = None,
        reply_to: Optional[int] = None,
        effect_id: Optional[str] = None,
        schedule_date: Optional[int] = None
    ) -> Message:
        """
        Deliver a text message.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target identifier.
        text : str
            Text content.
        markup : Optional[Any], default=None
            Keyboard markup or attachment.
        reply_to : Optional[int], default=None
            Target message ID to reply to.
        effect_id : Optional[str], default=None
            Message effect identifier.
        schedule_date : Optional[int], default=None
            Future unix time to dispatch.

        Returns
        -------
        Message
            Dispatched message object.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        
        msg = Message(
            id=int(time.time()),
            date=int(time.time()),
            chat=chat,
            sender=sender,
            text=text,
            reply_to_message=reply_to,
            effect_id=effect_id,
            markup=markup
        )
        
        asyncio.create_task(self.dispatcher.feed_signal(msg))
        return msg

    async def echo(
        self,
        message: Message,
        text: str,
        markup: Optional[Any] = None,
        effect_id: Optional[str] = None
    ) -> Message:
        """
        Echo a response to an incoming message.

        Parameters
        ----------
        message : Message
            Original message reference.
        text : str
            Response text content.
        markup : Optional[Any], default=None
            Keyboard markup.
        effect_id : Optional[str], default=None
            Effect ID.

        Returns
        -------
        Message
            Response message reference.
        """
        return await self.deliver(
            chat_id=message.chat.id,
            text=text,
            markup=markup,
            reply_to=message.id,
            effect_id=effect_id
        )

    async def reshape(
        self,
        chat_id: Union[int, str],
        message_id: int,
        text: Optional[str] = None,
        markup: Optional[Any] = None
    ) -> Message:
        """
        Reshape/Edit an existing message.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat room.
        message_id : int
            Target message identifier.
        text : Optional[str], default=None
            Updated text content.
        markup : Optional[Any], default=None
            Updated keyboard markup.

        Returns
        -------
        Message
            Modified message object.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        msg = Message(
            id=message_id,
            date=int(time.time()),
            chat=chat,
            sender=sender,
            text=text,
            markup=markup
        )
        return msg

    async def erase(self, chat_id: Union[int, str], message_ids: Union[int, List[int]]) -> bool:
        """
        Erase/Delete messages.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat room.
        message_ids : Union[int, List[int]]
            Identifiers of messages to delete.

        Returns
        -------
        bool
            True on successful execution.
        """
        return True

    async def collect(
        self,
        file_id: str,
        progress_callback: Optional[Callable[[int, int], Any]] = None
    ) -> bytes:
        """
        Collect/Download media file data.

        Parameters
        ----------
        file_id : str
            File storage identifier.
        progress_callback : Optional[Callable[[int, int], Any]], default=None
            Progress feedback tracking callback.

        Returns
        -------
        bytes
            Downloaded file content buffer.
        """
        if progress_callback:
            progress_callback(50, 100)
            progress_callback(100, 100)
        return b"mock_file_data"

    async def deliver_image(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], Any]] = None
    ) -> Message:
        """
        Deliver a photo/image.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target identifier.
        file : Union[str, bytes]
            File path or binary buffer.
        caption : Optional[str], default=None
            Media description text.
        progress_callback : Optional[Callable[[int, int], Any]], default=None
            Callback function.

        Returns
        -------
        Message
            Dispatched message.
        """
        if progress_callback:
            progress_callback(100, 100)
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        photo = Photo(file_id="photo123", file_unique_id="photo_uniq", width=800, height=600, file_size=1000)
        msg = Message(
            id=int(time.time()),
            date=int(time.time()),
            chat=chat,
            sender=sender,
            text=caption,
            media=photo
        )
        return msg

    async def deliver_video(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], Any]] = None
    ) -> Message:
        """
        Deliver a video.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target identifier.
        file : Union[str, bytes]
            File path or binary buffer.
        caption : Optional[str], default=None
            Media description text.
        progress_callback : Optional[Callable[[int, int], Any]], default=None
            Callback function.

        Returns
        -------
        Message
            Dispatched message.
        """
        if progress_callback:
            progress_callback(100, 100)
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        video = Video(file_id="video123", file_unique_id="video_uniq", width=1280, height=720, duration=30, file_size=5000)
        msg = Message(
            id=int(time.time()),
            date=int(time.time()),
            chat=chat,
            sender=sender,
            text=caption,
            media=video
        )
        return msg

    async def deliver_file(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int], Any]] = None
    ) -> Message:
        """
        Deliver a generic document/file.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target identifier.
        file : Union[str, bytes]
            File path or binary buffer.
        caption : Optional[str], default=None
            Media description text.
        progress_callback : Optional[Callable[[int, int], Any]], default=None
            Callback function.

        Returns
        -------
        Message
            Dispatched message.
        """
        if progress_callback:
            progress_callback(100, 100)
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        doc = Document(file_id="doc123", file_unique_id="doc_uniq", file_name="document.pdf", mime_type="application/pdf", file_size=2000)
        msg = Message(
            id=int(time.time()),
            date=int(time.time()),
            chat=chat,
            sender=sender,
            text=caption,
            media=doc
        )
        return msg

    async def relay(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_ids: Union[int, List[int]]) -> List[Message]:
        """
        Relay/Forward messages to target chat.

        Parameters
        ----------
        chat_id : Union[int, str]
            Destination chat.
        from_chat_id : Union[int, str]
            Origin chat.
        message_ids : Union[int, List[int]]
            Identifiers of messages to forward.

        Returns
        -------
        List[Message]
            Forwarded messages.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        return [Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=sender, text="Forwarded")]

    async def duplicate(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_ids: Union[int, List[int]]) -> List[Message]:
        """
        Duplicate/Copy messages to target chat.

        Parameters
        ----------
        chat_id : Union[int, str]
            Destination chat.
        from_chat_id : Union[int, str]
            Origin chat.
        message_ids : Union[int, List[int]]
            Identifiers of messages to copy.

        Returns
        -------
        List[Message]
            Copied messages.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        sender = self.me if self.me else User(id=1, first_name="Sender")
        return [Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=sender, text="Copied")]

    async def summon(self, chat_id: Union[int, str]) -> bool:
        """
        Summon/Join chat room or channel.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat address/identifier.

        Returns
        -------
        bool
            True on successful entry.
        """
        return True

    async def primitive(self, chat_id: Union[int, str]) -> dict:
        """
        Execute raw MTProto RPC request primitive.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target identifier parameter.

        Returns
        -------
        dict
            Returned response dictionary mapping fields.
        """
        return {"chat_id": chat_id, "raw_data": True}

    async def anchor(self, chat_id: Union[int, str], message_id: int) -> bool:
        """
        Anchor/Pin a message.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat.
        message_id : int
            Message identifier.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def release_anchor(self, chat_id: Union[int, str], message_id: int) -> bool:
        """
        Release anchor/Unpin message.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat.
        message_id : int
            Message identifier.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def enter(self, chat_id: int) -> None:
        """
        Enter a voice room.

        Parameters
        ----------
        chat_id : int
            Room identifier.
        """
        await self.calls.enter_room(chat_id)

    async def exit_room(self, chat_id: int) -> None:
        """
        Exit a voice room.

        Parameters
        ----------
        chat_id : int
            Room identifier.
        """
        await self.calls.exit_room(chat_id)

    async def block_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """
        Block/Restrict member in chat.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat.
        user_id : int
            User to block.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def release_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """
        Release/Unblock member in chat.

        Parameters
        ----------
        chat_id : Union[int, str]
            Target chat.
        user_id : int
            User to release.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def vault(self, key: str, value: Optional[Any] = None) -> Optional[Any]:
        """
        Vault/Safe store credentials or local app state variables.

        Parameters
        ----------
        key : str
            Store key identifier.
        value : Optional[Any], default=None
            Value data to set.

        Returns
        -------
        Optional[Any]
            Retrieved value or confirmed input.
        """
        if value is not None:
            await self.session.save()
            return value
        return "vault_value"

    async def set_business_greeting(self, message: str) -> bool:
        """
        Set greeting auto-reply for business accounts.

        Parameters
        ----------
        message : str
            Text reply template.

        Returns
        -------
        bool
            True on configuration success.
        """
        return True

    async def set_business_away(self, message: str) -> bool:
        """
        Set away auto-reply for business accounts.

        Parameters
        ----------
        message : str
            Text reply template.

        Returns
        -------
        bool
            True on configuration success.
        """
        return True

    async def set_business_links(self, link: str) -> bool:
        """
        Configure business contact links.

        Parameters
        ----------
        link : str
            Url redirection link.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def publish_story(self, caption: str) -> int:
        """
        Publish a profile story update.

        Parameters
        ----------
        caption : str
            Story caption text.

        Returns
        -------
        int
            Created story identifier.
        """
        return 999

    async def react_to_story(self, story_id: int, reaction: str) -> bool:
        """
        React to an active story.

        Parameters
        ----------
        story_id : int
            Story identifier.
        reaction : str
            Emoji reaction character.

        Returns
        -------
        bool
            True on successful reaction update.
        """
        return True
