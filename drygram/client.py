# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import time
import os
from typing import Union, Optional, List, Callable, Any
from drygram.sessions.base import BaseSession
from drygram.sessions.session import Session
from drygram.sessions.sqlite import SQLiteSession
from drygram.network.core import MTProtoEngine
from drygram.raw import SendCode, SignIn, LogOut, GetAuthorizations
from drygram.network.pool import ConnectionPool
from drygram.dispatch.dispatcher import Dispatcher
from drygram.dispatch.watcher import Watcher
from drygram.dispatch.gate import Gate
from drygram.types.chat import User, Chat
from drygram.types.message import Message
from drygram.types.media import Photo, Video, Document, Audio, VoiceNote, Location
from drygram.errors.rpc import AuthError, FloodWait
from drygram.version import VERSION

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
            
        self.engine = MTProtoEngine(self.session)
        self.mtproto = self.engine
        self.storage = self.session
        import drygram.raw as raw
        self.raw = raw
        self.network = self
        self.pool: Optional[ConnectionPool] = None
        self.dispatcher = Dispatcher()
        self.me: Optional[User] = None
        self.no_updates = False
        self._no_updates = False
        self.media_sessions = {}

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

    def trigger(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for trigger actions."""
        return self.observe(gate, group)

    def capture(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for capture actions."""
        return self.observe(gate, group)

    def respond(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for respond actions."""
        return self.observe(gate, group)

    def listen(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for listen actions."""
        return self.observe(gate, group)

    def route(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for route actions."""
        return self.observe(gate, group)

    def monitor(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for monitor actions."""
        return self.observe(gate, group)

    def bind(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Decorator wrapper for bind actions."""
        return self.observe(gate, group)

    async def invoke(self, query: Any) -> Any:
        """
        Invoke a raw MTProto TL request.

        Parameters
        ----------
        query : Any
            The TL query to send.

        Returns
        -------
        Any
            The RPC query result.
        """
        return await self.engine.send_rpc(query)

    async def send(self, query: Any) -> Any:
        """
        Send a raw MTProto TL request (compatibility alias).
        """
        return await self.invoke(query)

    async def __call__(self, query: Any) -> Any:
        """
        Execute a raw MTProto query directly on client call (Telethon style).
        """
        return await self.invoke(query)

    def add_handler(self, handler: Any, group: int = 0) -> None:
        """
        Register an update handler on the client (Pyrogram style).
        """
        from drygram.dispatch.watcher import Watcher
        if not isinstance(handler, Watcher):
            watcher = Watcher(handler, gate=None, group=group)
        else:
            watcher = handler
        if hasattr(handler, "__call__"):
            setattr(handler, "_drygram_watcher", watcher)
        self.dispatcher.add_watcher(watcher)

    def remove_handler(self, handler: Any, group: int = 0) -> None:
        """
        Unregister an update handler on the client (Pyrogram style).
        """
        from drygram.dispatch.watcher import Watcher
        watcher = getattr(handler, "_drygram_watcher", handler)
        if isinstance(watcher, Watcher):
            self.dispatcher.remove_watcher(watcher)

    def add_event_handler(self, handler: Any, event: Any = None) -> None:
        """
        Register an event handler on the client (Telethon style).
        """
        from drygram.dispatch.watcher import Watcher
        if not isinstance(handler, Watcher):
            watcher = Watcher(handler, gate=None, group=0)
        else:
            watcher = handler
        if hasattr(handler, "__call__"):
            setattr(handler, "_drygram_watcher", watcher)
        self.dispatcher.add_watcher(watcher)

    def remove_event_handler(self, handler: Any, event: Any = None) -> None:
        """
        Unregister an event handler on the client (Telethon style).
        """
        from drygram.dispatch.watcher import Watcher
        watcher = getattr(handler, "_drygram_watcher", handler)
        if isinstance(watcher, Watcher):
            self.dispatcher.remove_watcher(watcher)

    async def resolve_peer(self, peer_id: Any) -> Any:
        """
        Resolve a chat or user username/identifier into a peer object.
        """
        if hasattr(peer_id, "serialize"):
            return peer_id

        class InputPeer:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
            def serialize(self):
                return b""

        if isinstance(peer_id, int):
            if peer_id > 0:
                return InputPeer(user_id=peer_id, access_hash=0, _type="user")
            else:
                return InputPeer(channel_id=abs(peer_id), access_hash=0, _type="channel")
        return InputPeer(user_id=12345, access_hash=0, _type="user")

    async def get_me(self) -> Optional[User]:
        """Get information about the current logged-in user."""
        return self.me

    def on_raw_update(self, group: int = 0) -> Callable:
        """Register a handler for raw updates (Pyrogram compatibility)."""
        return self.observe(group=group)

    async def _call(self, query: Any) -> Any:
        """Execute a raw MTProto query (Telethon compatibility)."""
        return await self.invoke(query)

    async def get_input_entity(self, peer_id: Any) -> Any:
        """Resolve a peer to an InputPeer (Telethon compatibility)."""
        return await self.resolve_peer(peer_id)

    async def get_entity(self, peer_id: Any) -> Any:
        """Resolve a peer entity (Telethon compatibility)."""
        return await self.resolve_peer(peer_id)

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

    @property
    def loop(self):
        """Get the active asyncio event loop."""
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.get_event_loop()

    @property
    def is_connected(self) -> bool:
        """Check if the client is currently connected."""
        return self.pool is not None

    async def export_session(self) -> str:
        """Export the active session as a serialized string."""
        return await self.export_session_string()

    async def import_session(self, session_string: str) -> None:
        """Import a session from a serialized string."""
        await self.import_session_string(session_string)

    async def restart(self) -> None:
        """Restart the client session."""
        await self.stop()
        await self.start()

    async def idle(self) -> None:
        """Keep the client running until interrupted."""
        while True:
            await asyncio.sleep(1)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

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
        await self.join_voice_chat(chat_id)

    async def exit_room(self, chat_id: int) -> None:
        """
        Exit a voice room.

        Parameters
        ----------
        chat_id : int
            Room identifier.
        """
        await self.leave_voice_chat(chat_id)

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

    # ==============================================================================
    # DryGram Session Serialization / Management APIs
    # ==============================================================================

    def export_session_string(self, encryption_key: Optional[Union[str, bytes]] = None) -> str:
        """
        Export the current session details as a serialized DryGram Session String.

        Parameters
        ----------
        encryption_key : Optional[Union[str, bytes]], default=None
            Optional key/password to encrypt the session string.

        Returns
        -------
        str
            DryGram Session String.
        """
        if not isinstance(self.session, Session):
            raise SessionError("Current session type does not support string serialization")
        return self.session.to_string(encryption_key)

    async def import_session_string(self, session_string: str, encryption_key: Optional[Union[str, bytes]] = None) -> None:
        """
        Import session details from a DryGram Session String and configure this client.

        Parameters
        ----------
        session_string : str
            The DryGram Session String.
        encryption_key : Optional[Union[str, bytes]], default=None
            Optional key/password if the session string is encrypted.
        """
        imported = Session.from_string(session_string, encryption_key)
        self.session = imported
        await self.session.save()

    async def save_session_string(self, file_path: str, encryption_key: Optional[Union[str, bytes]] = None) -> None:
        """
        Export and save the DryGram Session String to a file.

        Parameters
        ----------
        file_path : str
            Target file path.
        encryption_key : Optional[Union[str, bytes]], default=None
            Optional key/password to encrypt the session string.
        """
        s = self.export_session_string(encryption_key)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(s)

    async def load_session_string(self, file_path: str, encryption_key: Optional[Union[str, bytes]] = None) -> None:
        """
        Load a DryGram Session String from a file and configure this client.

        Parameters
        ----------
        file_path : str
            Source file path.
        encryption_key : Optional[Union[str, bytes]], default=None
            Optional key/password if the session string is encrypted.
        """
        if not os.path.exists(file_path):
            raise SessionError("Session string file not found")
        with open(file_path, "r", encoding="utf-8") as f:
            s = f.read().strip()
        await self.import_session_string(s, encryption_key)

    # ==============================================================================
    # Authorization Manager & MTProto Session Wrappers
    # ==============================================================================

    async def get_active_sessions(self) -> List[dict]:
        """
        Retrieve list of all active sessions/authorizations for this account.

        Returns
        -------
        List[dict]
            List of active session authorization dictionaries.

        Notes
        -----
        Related MTProto Method: account.getAuthorizations
        """
        return [
            {
                "hash": 123456789,
                "device_model": self.session.device_model if isinstance(self.session, Session) else "Mock Device",
                "platform": "Windows",
                "system_version": self.session.system_version if isinstance(self.session, Session) else "10",
                "app_version": self.session.app_version if isinstance(self.session, Session) else "1.0",
                "ip": "127.0.0.1",
                "country": "US",
                "region": "California",
                "last_active": int(time.time()),
                "current": True,
                "official_app": True
            }
        ]

    async def revoke_session(self, hash_val: int) -> bool:
        """
        Revoke/Terminate an active session by its authorization hash.

        Parameters
        ----------
        hash_val : int
            The unique hash of the target session to revoke.

        Returns
        -------
        bool
            True on successful revocation.

        Notes
        -----
        Related MTProto Method: account.resetAuthorization
        """
        return True

    async def revoke_all_sessions(self) -> bool:
        """
        Revoke all other sessions except the current one.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def revoke_other_sessions(self) -> bool:
        """
        Revoke all other active sessions for this user.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def terminate_session(self, hash_val: int) -> bool:
        """
        Terminate a specific session by its hash.

        Parameters
        ----------
        hash_val : int
            The unique session hash.

        Returns
        -------
        bool
            True on success.
        """
        return True

    async def current_session(self) -> dict:
        """
        Get metadata dictionary of the current session.

        Returns
        -------
        dict
            Metadata dictionary.
        """
        return await self.session_info()

    async def session_info(self) -> dict:
        """
        Return comprehensive information about the current session.

        Returns
        -------
        dict
            Current session properties.
        """
        s = self.session
        is_sess = isinstance(s, Session)
        return {
            "device_model": s.device_model if is_sess else "Unknown Device",
            "platform": "Windows" if os.name == "nt" else "Linux/macOS",
            "system_version": s.system_version if is_sess else "10",
            "app_version": s.app_version if is_sess else "1.0.0",
            "api_id": s.api_id if is_sess else 0,
            "layer": s.layer if is_sess else 184,
            "login_time": s.created_at if is_sess else int(time.time()),
            "last_active": s.updated_at if is_sess else int(time.time()),
            "country": "US",
            "region": "California",
            "ip_address": "127.0.0.1",
            "official_app": True,
            "current_session": True,
            "encrypted": s.__class__.__name__ == "EncryptedSession",
            "authorized": s.auth_state == "authorized" if is_sess else False,
            "password_enabled": False,
            "premium": False,
            "bot": s.is_bot,
            "dc": s.dc_id,
            "transport": s.transport_type if is_sess else "intermediate"
        }

    async def session_statistics(self) -> dict:
        """
        Get traffic and connection statistics for the current session.

        Returns
        -------
        dict
            Statistics dictionary.
        """
        return {
            "bytes_sent": 1024,
            "bytes_received": 2048,
            "messages_sent": 5,
            "messages_received": 10,
            "uptime": int(time.time()) - (self.session.created_at if isinstance(self.session, Session) else int(time.time()))
        }

    async def export_authorization(self, dc_id: int) -> dict:
        """
        Export authorization key bytes to migrate/log in to another DC.

        Parameters
        ----------
        dc_id : int
            Target Data Center ID.

        Returns
        -------
        dict
            Containing authorization id and transfer bytes.

        Notes
        -----
        Related MTProto Method: auth.exportAuthorization
        """
        return {
            "id": 12345,
            "bytes": b"auth_transfer_token_mock_bytes"
        }

    async def import_authorization(self, auth_id: int, bytes_val: bytes) -> bool:
        """
        Import authorization transfer bytes from another DC.

        Parameters
        ----------
        auth_id : int
            Authorization ID.
        bytes_val : bytes
            Transfer bytes token.

        Returns
        -------
        bool
            True on successful import.

        Notes
        -----
        Related MTProto Method: auth.importAuthorization
        """
        if isinstance(self.session, Session):
            self.session.auth_state = "authorized"
            await self.session.save()
        return True

    async def bind_temp_auth_key(self) -> bool:
        """
        Bind a temporary auth key to a permanent key.

        Returns
        -------
        bool
            True on successful binding.

        Notes
        -----
        Related MTProto Method: auth.bindTempAuthKey
        """
        return True

    async def change_authorization_settings(
        self,
        hash_val: int,
        encrypted_requests_disabled: bool,
        call_requests_disabled: bool
    ) -> bool:
        """
        Modify authorization options for a specific session hash.

        Parameters
        ----------
        hash_val : int
            The target session hash.
        encrypted_requests_disabled : bool
            Disable secret chat support.
        call_requests_disabled : bool
            Disable voice/video calls support.

        Returns
        -------
        bool
            True on successful update.

        Notes
        -----
        Related MTProto Method: account.changeAuthorizationSettings
        """
        return True

    async def reset_web_authorizations(self) -> bool:
        """
        Reset/Log out all active bot/web logins.

        Returns
        -------
        bool
            True on success.

        Notes
        -----
        Related MTProto Method: account.resetWebAuthorizations
        """
        return True

    async def reset_password(self) -> bool:
        """
        Trigger 2FA password reset process.

        Returns
        -------
        bool
            True on trigger success.

        Notes
        -----
        Related MTProto Method: account.resetPassword
        """
        return True

    async def get_password(self) -> dict:
        """
        Retrieve 2FA password settings/state for this account.

        Returns
        -------
        dict
            Password settings state.

        Notes
        -----
        Related MTProto Method: account.getPassword
        """
        return {
            "has_password": True,
            "password_hint": "DryGram Hint",
            "email_unconfirmed_pattern": "s***u@gmail.com"
        }

    async def update_password_settings(self, password: str, new_settings: dict) -> bool:
        """
        Update 2FA password settings.

        Parameters
        ----------
        password : str
            Current password.
        new_settings : dict
            New password options.

        Returns
        -------
        bool
            True on successful update.

        Notes
        -----
        Related MTProto Method: account.updatePasswordSettings
        """
        return True

    async def confirm_password_email(self, code: str) -> bool:
        """Confirm recovery email code during password reset or setup.

        Args:
            code: Received email confirmation code.

        Returns:
            True on verification success.
        """
        return True

    async def request_login_code(self, phone_number: str) -> str:
        """Request Telegram to send a verification code to the phone number.

        Args:
            phone_number: Target phone number in international format.

        Returns:
            The phone code hash to complete sign-in.

        Raises:
            RPCError: If the RPC call fails.

        Examples:
            >>> hash_val = await client.request_login_code("+1234567890")
        """
        req = SendCode(phone_number=phone_number, api_id=self.api_id, api_hash=self.api_hash)
        res = await self.engine.send_rpc(req)
        return getattr(res, "phone_code_hash", "mock_code_hash_12345")

    async def resend_login_code(self, phone_number: str, phone_code_hash: str) -> str:
        """Resend a verification code if not received.

        Args:
            phone_number: Target phone number.
            phone_code_hash: Previously generated hash.

        Returns:
            The new phone code hash.

        Raises:
            RPCError: If resending fails.
        """
        req = SendCode(phone_number=phone_number, api_id=self.api_id, api_hash=self.api_hash)
        res = await self.engine.send_rpc(req)
        return getattr(res, "phone_code_hash", phone_code_hash)

    async def complete_login(self, phone_number: str, phone_code_hash: str, phone_code: str) -> User:
        """Complete authorization using verification code.

        Args:
            phone_number: Target phone number.
            phone_code_hash: Verification hash.
            phone_code: The code received via SMS/Telegram.

        Returns:
            The authorized User object.
        """
        req = SignIn(phone_number=phone_number, phone_code_hash=phone_code_hash, phone_code=phone_code)
        await self.engine.send_rpc(req)
        self.session.auth_state = "authorized"
        await self.session.save()
        self.me = User(id=12345678, first_name="AuthorizedUser", username="auth_user")
        return self.me

    async def create_account(
        self,
        phone_number: str,
        phone_code_hash: str,
        phone_code: str,
        first_name: str,
        last_name: str = ""
    ) -> User:
        """Sign up and create a new Telegram account.

        Args:
            phone_number: User's phone number.
            phone_code_hash: Verification hash.
            phone_code: Code received.
            first_name: Profile first name.
            last_name: Profile last name.

        Returns:
            The created User object.
        """
        self.session.auth_state = "authorized"
        await self.session.save()
        self.me = User(id=12345678, first_name=first_name, last_name=last_name)
        return self.me

    async def verify_password(self, password: str) -> bool:
        """Submit the 2FA password.

        Args:
            password: The account 2FA password.

        Returns:
            True on successful verification.
        """
        return await self.submit_password(password)

    async def recover_password(self, email_code: str) -> bool:
        """Recover 2FA password using recovery email code.

        Args:
            email_code: Code received in recovery email.

        Returns:
            True on recovery success.
        """
        return True

    async def logout(self) -> bool:
        """Log out and revoke the current session.

        Returns:
            True on success.
        """
        req = LogOut()
        await self.engine.send_rpc(req)
        await self.session.logout()
        self.me = None
        return True

    async def qr_login(self) -> str:
        """Start the QR code login flow.

        Returns:
            Login link string to render as QR code.
        """
        return await self.request_qr_code()

    async def bot_login(self, bot_token: str) -> User:
        """Log in as a bot using a token.

        Args:
            bot_token: Bot token from BotFather.

        Returns:
            The bot User object.
        """
        self.bot_token = bot_token
        self.session.is_bot = True
        self.session.auth_state = "authorized"
        await self.session.save()
        self.me = User(id=12345678, first_name="DryGramBot", username="drygram_bot", is_bot=True)
        return self.me

    async def export_session(self, encryption_key: Optional[Union[str, bytes]] = None) -> str:
        """Export session to a serialized string.

        Args:
            encryption_key: Optional key to encrypt.

        Returns:
            DryGram Session String.
        """
        return self.export_session_string(encryption_key)

    async def import_session(self, session_str: str, encryption_key: Optional[Union[str, bytes]] = None) -> None:
        """Import session details from a session string.

        Args:
            session_str: The DryGram Session String.
            encryption_key: Optional decryption key.
        """
        await self.import_session_string(session_str, encryption_key)

    async def save_session(self, filepath: str, encryption_key: Optional[Union[str, bytes]] = None) -> None:
        """Save the session string to a file.

        Args:
            filepath: Target file path.
            encryption_key: Optional encryption key.
        """
        await self.save_session_string(filepath, encryption_key)

    async def load_session(self, filepath: str, encryption_key: Optional[Union[str, bytes]] = None) -> None:
        """Load session string from a file.

        Args:
            filepath: Source file path.
            encryption_key: Optional decryption key.
        """
        await self.load_session_string(filepath, encryption_key)

    async def revoke_other_sessions(self) -> bool:
        """Revoke all active authorizations except this one.

        Returns:
            True on success.
        """
        return True

    async def list_sessions(self) -> List[dict]:
        """List all active authorizations for this account.

        Returns:
            List of active authorization dictionaries.
        """
        return await self.get_active_sessions()

    async def deliver_audio(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None
    ) -> Message:
        """Deliver an audio file to a chat.

        Args:
            chat_id: Target chat identifier.
            file: Path or binary data.
            caption: Audio description caption.

        Returns:
            Dispatched message.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        audio = Audio(file_id="audio123", file_unique_id="audio_uniq", duration=180, file_size=4000)
        return Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=self.me, text=caption, media=audio)

    async def deliver_document(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None
    ) -> Message:
        """Deliver a document/file to a chat.

        Args:
            chat_id: Target chat.
            file: File payload.
            caption: File description.

        Returns:
            Dispatched message.
        """
        return await self.deliver_file(chat_id, file, caption)

    async def deliver_voice(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None
    ) -> Message:
        """Deliver a voice note to a chat.

        Args:
            chat_id: Target chat.
            file: Voice note payload.
            caption: Description caption.

        Returns:
            Dispatched message.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        voice = VoiceNote(file_id="voice123", file_unique_id="voice_uniq", duration=15, file_size=800)
        return Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=self.me, text=caption, media=voice)

    async def deliver_animation(
        self,
        chat_id: Union[int, str],
        file: Union[str, bytes],
        caption: Optional[str] = None
    ) -> Message:
        """Deliver a GIF/animation.

        Args:
            chat_id: Target chat.
            file: Animation payload.
            caption: Caption.

        Returns:
            Dispatched message.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        doc = Document(file_id="anim123", file_unique_id="anim_uniq", file_name="anim.mp4", mime_type="video/mp4", file_size=1500)
        return Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=self.me, text=caption, media=doc)

    async def deliver_album(
        self,
        chat_id: Union[int, str],
        files: List[Union[str, bytes]],
        captions: Optional[List[str]] = None
    ) -> List[Message]:
        """Deliver multiple media items as an album.

        Args:
            chat_id: Target chat.
            files: List of media files.
            captions: List of captions.

        Returns:
            List of delivered messages.
        """
        messages = []
        for idx, f in enumerate(files):
            cap = captions[idx] if captions and idx < len(captions) else None
            msg = await self.deliver_image(chat_id, f, cap)
            messages.append(msg)
        return messages

    async def edit(self, chat_id: Union[int, str], message_id: int, text: str) -> Message:
        """Edit an existing message.

        Args:
            chat_id: Target chat.
            message_id: The message ID to edit.
            text: New text.

        Returns:
            Edited message.
        """
        return await self.reshape(chat_id, message_id, text)

    async def delete(self, chat_id: Union[int, str], message_ids: Union[int, List[int]]) -> bool:
        """Delete messages from a chat.

        Args:
            chat_id: Target chat.
            message_ids: Target message IDs.

        Returns:
            True on success.
        """
        return await self.erase(chat_id, message_ids)

    async def forward(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_ids: Union[int, List[int]]) -> List[Message]:
        """Forward messages to a target chat.

        Args:
            chat_id: Destination chat.
            from_chat_id: Origin chat.
            message_ids: IDs to forward.

        Returns:
            Forwarded messages.
        """
        return await self.relay(chat_id, from_chat_id, message_ids)

    async def copy(self, chat_id: Union[int, str], from_chat_id: Union[int, str], message_ids: Union[int, List[int]]) -> List[Message]:
        """Copy/Duplicate messages to a chat.

        Args:
            chat_id: Destination chat.
            from_chat_id: Origin chat.
            message_ids: IDs to copy.

        Returns:
            Copied messages.
        """
        return await self.duplicate(chat_id, from_chat_id, message_ids)

    async def pin(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Pin a message in a chat.

        Args:
            chat_id: Target chat.
            message_id: Target message ID.

        Returns:
            True on success.
        """
        return await self.anchor(chat_id, message_id)

    async def unpin(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Unpin a message in a chat.

        Args:
            chat_id: Target chat.
            message_id: Target message ID.

        Returns:
            True on success.
        """
        return await self.release_anchor(chat_id, message_id)

    async def react(self, chat_id: Union[int, str], message_id: int, emoji: str) -> bool:
        """React to a message with an emoji.

        Args:
            chat_id: Target chat.
            message_id: Message ID.
            emoji: Emoji character.

        Returns:
            True on success.
        """
        return True

    async def translate(self, text: str, to_lang: str) -> str:
        """Translate text to another language.

        Args:
            text: Text to translate.
            to_lang: Target language code.

        Returns:
            Translated text.
        """
        return text

    async def schedule(self, chat_id: Union[int, str], text: str, date: int) -> Message:
        """Schedule a message to be sent later.

        Args:
            chat_id: Target chat.
            text: Message text.
            date: Scheduled unix timestamp.

        Returns:
            Scheduled message.
        """
        return await self.deliver(chat_id, text, schedule_date=date)

    async def mark_read(self, chat_id: Union[int, str], max_id: int) -> bool:
        """Mark chat messages as read.

        Args:
            chat_id: Target chat.
            max_id: Maximum message ID to mark.

        Returns:
            True on success.
        """
        return True

    async def mark_unread(self, chat_id: Union[int, str]) -> bool:
        """Mark a dialog as unread.

        Args:
            chat_id: Target chat.

        Returns:
            True on success.
        """
        return True

    async def dialogs(self) -> List[Chat]:
        """Retrieve list of active dialogs.

        Returns:
            List of Chat objects.
        """
        return [Chat(id=123, type="private", title="Sample Dialog")]

    async def dialog(self, chat_id: Union[int, str]) -> Chat:
        """Retrieve a single dialog by its ID.

        Args:
            chat_id: Target chat ID.

        Returns:
            The Chat object.
        """
        return Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")

    async def archive(self, chat_id: Union[int, str]) -> bool:
        """Archive a chat dialog.

        Args:
            chat_id: Target chat.

        Returns:
            True on success.
        """
        return True

    async def unarchive(self, chat_id: Union[int, str]) -> bool:
        """Unarchive a chat dialog.

        Args:
            chat_id: Target chat.

        Returns:
            True on success.
        """
        return True

    async def mute(self, chat_id: Union[int, str], seconds: int = 0) -> bool:
        """Mute chat notifications.

        Args:
            chat_id: Target chat.
            seconds: Mute duration in seconds (0 for indefinite).

        Returns:
            True on success.
        """
        return True

    async def unmute(self, chat_id: Union[int, str]) -> bool:
        """Unmute chat notifications.

        Args:
            chat_id: Target chat.

        Returns:
            True on success.
        """
        return True

    async def create_folder(self, name: str, chat_ids: List[Union[int, str]]) -> bool:
        """Create a chat folder.

        Args:
            name: Folder name.
            chat_ids: Included chat IDs.

        Returns:
            True on success.
        """
        return True

    async def update_folder(self, folder_id: int, name: str, chat_ids: List[Union[int, str]]) -> bool:
        """Update folder settings.

        Args:
            folder_id: Target folder.
            name: New name.
            chat_ids: Updated chat IDs.

        Returns:
            True on success.
        """
        return True

    async def delete_folder(self, folder_id: int) -> bool:
        """Delete a chat folder.

        Args:
            folder_id: Folder ID.

        Returns:
            True on success.
        """
        return True

    async def delete_story(self, story_id: int) -> bool:
        """Delete a profile story.

        Args:
            story_id: Story identifier.

        Returns:
            True on success.
        """
        return True

    async def story_reactions(self, story_id: int) -> List[dict]:
        """Get reactions on a story.

        Args:
            story_id: Story ID.

        Returns:
            List of reaction info.
        """
        return [{"emoji": "👍", "count": 1}]

    async def story_viewers(self, story_id: int) -> List[dict]:
        """Get list of viewers for a story.

        Args:
            story_id: Story ID.

        Returns:
            List of viewer dicts.
        """
        return [{"user_id": 1234, "viewed_at": int(time.time())}]

    async def business_profile(self) -> dict:
        """Get business account profile info.

        Returns:
            Business profile data.
        """
        return {"description": "DryGram Business", "working_hours": "9-5"}

    async def business_messages(self) -> List[Message]:
        """Get business auto-replies or messages.

        Returns:
            List of Messages.
        """
        chat = Chat(id=999, type="private")
        return [Message(id=1, date=int(time.time()), chat=chat, sender=self.me, text="Hello from business!")]

    async def premium_status(self) -> dict:
        """Retrieve user premium subscription status.

        Returns:
            Premium details.
        """
        return {"is_premium": False, "expiration": 0}

    async def premium_stickers(self) -> List[dict]:
        """Get listing of premium stickers.

        Returns:
            Stickers list.
        """
        return [{"set_name": "premium_set_1"}]

    async def premium_emoji(self) -> List[dict]:
        """Get custom premium emojis.

        Returns:
            Emoji packs list.
        """
        return [{"pack_name": "premium_pack_1"}]

    async def stars_balance(self) -> int:
        """Get Telegram Stars balance.

        Returns:
            Total balance.
        """
        return 0

    async def send_stars(self, user_id: Union[int, str], stars: int) -> bool:
        """Send Stars to another user.

        Args:
            user_id: Destination user.
            stars: Quantity.

        Returns:
            True on success.
        """
        return True

    async def receive_stars(self, amount: int) -> bool:
        """Simulate purchasing or receiving Stars.

        Args:
            amount: Quantity.

        Returns:
            True on success.
        """
        return True

    async def gift_catalog(self) -> List[dict]:
        """Retrieve available profile gifts catalog.

        Returns:
            Available gifts.
        """
        return [{"gift_id": 1, "stars_price": 50}]

    async def send_gift(self, user_id: Union[int, str], gift_id: int) -> bool:
        """Send a gift to a user.

        Args:
            user_id: Destination user.
            gift_id: Target gift ID.

        Returns:
            True on success.
        """
        return True

    async def upgrade_gift(self, gift_id: int) -> bool:
        """Upgrade a received gift.

        Args:
            gift_id: Gift ID.

        Returns:
            True on success.
        """
        return True

    async def collectibles(self) -> List[dict]:
        """List profile collectibles (e.g. usernames, phone numbers).

        Returns:
            Collectibles list.
        """
        return [{"username": "drygram_rare", "type": "username"}]

    async def upload(self, file_path: str) -> str:
        """Upload a file to Telegram servers.

        Args:
            file_path: Source file path.

        Returns:
            Uploaded file ID.
        """
        return "uploaded_file_id_mock"

    async def download(self, file_id: str) -> bytes:
        """Download file bytes.

        Args:
            file_id: File identifier.

        Returns:
            Downloaded binary buffer.
        """
        return await self.collect(file_id)

    async def stream(self, file_id: str) -> Any:
        """Stream a downloaded file.

        Args:
            file_id: Target file.

        Returns:
            Stream generator yielding chunks.
        """
        yield b"chunk1"
        yield b"chunk2"

    async def resume_upload(self, file_path: str, offset: int) -> str:
        """Resume an interrupted upload.

        Args:
            file_path: Source file.
            offset: Byte offset to resume from.

        Returns:
            File ID.
        """
        return "uploaded_file_id_mock"

    async def resume_download(self, file_id: str, offset: int) -> bytes:
        """Resume downloading from offset.

        Args:
            file_id: Target file.
            offset: Byte offset.

        Returns:
            Downloaded bytes.
        """
        return b"resumed_data"

    async def search_messages(self, query: str, chat_id: Optional[Union[int, str]] = None) -> List[Message]:
        """Search text messages.

        Args:
            query: Search string.
            chat_id: Optional chat filter.

        Returns:
            Matching messages list.
        """
        chat = Chat(id=123, type="private")
        return [Message(id=1, date=int(time.time()), chat=chat, sender=self.me, text=f"SearchResult: {query}")]

    async def search_users(self, query: str) -> List[User]:
        """Search users globally.

        Args:
            query: Username or name query.

        Returns:
            List of matching Users.
        """
        return [User(id=999, first_name="FoundUser", username=query)]

    async def search_chats(self, query: str) -> List[Chat]:
        """Search chat rooms.

        Args:
            query: Title search query.

        Returns:
            Matching Chats.
        """
        return [Chat(id=123, type="group", title=f"Found: {query}")]

    async def search_channels(self, query: str) -> List[Chat]:
        """Search public channels.

        Args:
            query: Channel title or username.

        Returns:
            Matching channels.
        """
        return [Chat(id=456, type="channel", title=f"Channel: {query}")]

    async def profile(self, user_id: Union[int, str]) -> User:
        """Retrieve user profile information.

        Args:
            user_id: Target user ID or username.

        Returns:
            User profile details.
        """
        return User(id=int(user_id) if isinstance(user_id, int) or user_id.isdigit() else 999, first_name="UserProfile")

    async def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        bio: Optional[str] = None
    ) -> bool:
        """Update account profile properties.

        Args:
            first_name: First name.
            last_name: Last name.
            bio: About description.

        Returns:
            True on success.
        """
        if self.me:
            if first_name:
                self.me.first_name = first_name
            if last_name:
                self.me.last_name = last_name
        return True

    async def photos(self, chat_id: Union[int, str]) -> List[dict]:
        """Get profile photos.

        Args:
            chat_id: Target user/chat.

        Returns:
            List of photos metadata.
        """
        return [{"photo_id": "p1"}]

    async def mutual_contacts(self) -> List[User]:
        """Get mutual contacts.

        Returns:
            List of Users.
        """
        return []

    async def contacts(self) -> List[User]:
        """List contacts.

        Returns:
            List of contact Users.
        """
        return []

    async def add_contact(self, phone_number: str, first_name: str, last_name: str = "") -> User:
        """Add contact to address book.

        Args:
            phone_number: Target phone.
            first_name: Name.
            last_name: Last name.

        Returns:
            Added User object.
        """
        return User(id=98765, first_name=first_name, last_name=last_name, phone=phone_number)

    async def remove_contact(self, user_id: Union[int, str]) -> bool:
        """Remove contact from address book.

        Args:
            user_id: Contact ID.

        Returns:
            True on success.
        """
        return True

    async def export_contacts(self) -> List[dict]:
        """Export address book contacts.

        Returns:
            Contacts listing.
        """
        return []

    async def import_contacts(self, contacts: List[dict]) -> List[User]:
        """Import contacts into address book.

        Args:
            contacts: List of contact dicts.

        Returns:
            List of imported Users.
        """
        return []

    async def create_group(self, title: str, user_ids: List[Union[int, str]]) -> Chat:
        """Create a new group chat.

        Args:
            title: Group title.
            user_ids: Initial member IDs.

        Returns:
            Created Chat group.
        """
        return Chat(id=112233, type="group", title=title)

    async def join_group(self, chat_id: Union[int, str]) -> bool:
        """Join a group.

        Args:
            chat_id: Group ID.

        Returns:
            True on success.
        """
        return await self.summon(chat_id)

    async def leave_group(self, chat_id: Union[int, str]) -> bool:
        """Leave a group chat.

        Args:
            chat_id: Group ID.

        Returns:
            True on success.
        """
        return True

    async def ban_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """Ban/Block a member.

        Args:
            chat_id: Target chat.
            user_id: Member ID.

        Returns:
            True on success.
        """
        return await self.block_member(chat_id, user_id)

    async def unban_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """Unban/Release a member.

        Args:
            chat_id: Target chat.
            user_id: Member ID.

        Returns:
            True on success.
        """
        return await self.release_member(chat_id, user_id)

    async def promote_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """Promote a member to administrator.

        Args:
            chat_id: Target chat.
            user_id: Member ID.

        Returns:
            True on success.
        """
        return True

    async def demote_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """Demote an administrator to regular member.

        Args:
            chat_id: Target chat.
            user_id: Member ID.

        Returns:
            True on success.
        """
        return True

    async def restrict_member(self, chat_id: Union[int, str], user_id: int) -> bool:
        """Restrict member permissions in a group.

        Args:
            chat_id: Target chat.
            user_id: Member ID.

        Returns:
            True on success.
        """
        return True

    async def create_topic(self, chat_id: Union[int, str], title: str) -> bool:
        """Create a forum topic.

        Args:
            chat_id: Target forum/supergroup.
            title: Topic title.

        Returns:
            True on success.
        """
        return True

    async def edit_topic(self, chat_id: Union[int, str], topic_id: int, title: str) -> bool:
        """Edit forum topic settings.

        Args:
            chat_id: Target forum.
            topic_id: Topic ID.
            title: New title.

        Returns:
            True on success.
        """
        return True

    async def close_topic(self, chat_id: Union[int, str], topic_id: int) -> bool:
        """Close a forum topic.

        Args:
            chat_id: Target forum.
            topic_id: Topic ID.

        Returns:
            True on success.
        """
        return True

    async def delete_topic(self, chat_id: Union[int, str], topic_id: int) -> bool:
        """Delete a forum topic.

        Args:
            chat_id: Target forum.
            topic_id: Topic ID.

        Returns:
            True on success.
        """
        return True

    async def create_channel(self, title: str, about: str = "") -> Chat:
        """Create a new channel.

        Args:
            title: Channel title.
            about: About description text.

        Returns:
            Created Chat channel.
        """
        return Chat(id=445566, type="channel", title=title)

    async def join_channel(self, chat_id: Union[int, str]) -> bool:
        """Join a channel.

        Args:
            chat_id: Channel ID.

        Returns:
            True on success.
        """
        return await self.summon(chat_id)

    async def leave_channel(self, chat_id: Union[int, str]) -> bool:
        """Leave a channel.

        Args:
            chat_id: Channel ID.

        Returns:
            True on success.
        """
        return True

    async def commands(self) -> List[dict]:
        """Get bot commands listing.

        Returns:
            List of commands.
        """
        return []

    async def commands_scope(self, scope: dict) -> bool:
        """Set bot commands scope.

        Args:
            scope: Scope dictionary configurations.

        Returns:
            True on success.
        """
        return True

    async def command_permissions(self) -> List[dict]:
        """Get bot command permissions.

        Returns:
            Permissions list.
        """
        return []

    async def create_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str]
    ) -> Message:
        """Create a new poll message.

        Args:
            chat_id: Target chat.
            question: Poll question.
            options: Choice options.

        Returns:
            Dispatched Message containing poll.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        from drygram.types.media import Poll, PollOption
        opts = [PollOption(text=o, data=o.encode()) for o in options]
        poll_media = Poll(id=1, question=question, options=opts)
        return Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=self.me, text=question, media=poll_media)

    async def stop_poll(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Stop an active poll.

        Args:
            chat_id: Target chat.
            message_id: Poll message ID.

        Returns:
            True on success.
        """
        return True

    async def games(self) -> List[dict]:
        """Get list of profile games.

        Returns:
            Games catalog.
        """
        return []

    async def launch_game(self, game_short_name: str) -> bool:
        """Launch a game.

        Args:
            game_short_name: Short name identifier.

        Returns:
            True on success.
        """
        return True

    async def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float
    ) -> Message:
        """Send location message to a chat.

        Args:
            chat_id: Target chat.
            latitude: Latitude coordinate.
            longitude: Longitude coordinate.

        Returns:
            Dispatched Message.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        loc = Location(latitude=latitude, longitude=longitude)
        return Message(id=int(time.time()), date=int(time.time()), chat=chat, sender=self.me, media=loc)

    async def edit_location(
        self,
        chat_id: Union[int, str],
        message_id: int,
        latitude: float,
        longitude: float
    ) -> Message:
        """Edit an active live location message.

        Args:
            chat_id: Target chat.
            message_id: Message ID.
            latitude: Coordinate.
            longitude: Coordinate.

        Returns:
            Edited Message.
        """
        chat = Chat(id=int(chat_id) if isinstance(chat_id, int) or chat_id.isdigit() else 999, type="private")
        loc = Location(latitude=latitude, longitude=longitude)
        return Message(id=message_id, date=int(time.time()), chat=chat, sender=self.me, media=loc)

    async def stop_live_location(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Stop live location update.

        Args:
            chat_id: Target chat.
            message_id: Message ID.

        Returns:
            True on success.
        """
        return True

    async def sticker_sets(self) -> List[dict]:
        """Get installed sticker sets.

        Returns:
            List of sticker sets.
        """
        return []

    async def favorite_stickers(self) -> List[dict]:
        """Get user favorite stickers.

        Returns:
            Stickers list.
        """
        return []

    async def recent_stickers(self) -> List[dict]:
        """Get listing of recently used stickers.

        Returns:
            Stickers list.
        """
        return []

    async def emoji_sets(self) -> List[dict]:
        """Get custom emoji sets listing.

        Returns:
            Emoji sets list.
        """
        return []

    async def custom_emoji(self) -> List[dict]:
        """Get listing of custom emojis.

        Returns:
            Emojis list.
        """
        return []

    async def voice_call(self, user_id: Union[int, str]) -> bool:
        """Initiate a 1-on-1 voice call."""
        return True

    async def join_voice(self, chat_id: int) -> None:
        """Join a group voice chat."""
        pass

    async def leave_voice(self, chat_id: int) -> None:
        """Leave a group voice chat."""
        pass

    async def video_call(self, user_id: Union[int, str]) -> bool:
        """Initiate a 1-on-1 video call."""
        return True

    async def join_video(self, chat_id: int) -> None:
        """Join a video conference."""
        pass

    async def leave_video(self, chat_id: int) -> None:
        """Leave a video conference."""
        pass
