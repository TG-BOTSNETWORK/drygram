# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock, patch
sys.modules['py_tgcalls'] = MagicMock()
sys.modules['ntgcalls'] = MagicMock()
from drygram import (
    DryError, SessionError, NetworkError, AuthError, FloodWait, RPCError,
    TaskScheduler, KeyboardButton, SQLiteSession
)
from drygram.dispatch.queue import PriorityQueue, QueueTask
from drygram.dispatch.scheduler import ScheduledTask
from drygram.dispatch.pipeline import MiddlewarePipeline
from drygram.plugins.loader import PluginLoader
from drygram.network.proxy import ProxyConnection
from drygram.network.pool import ConnectionPool
from drygram.network.connection import Connection

@pytest.mark.asyncio
async def test_error_models():
    with pytest.raises(DryError):
        raise DryError("err")
    with pytest.raises(SessionError):
        raise SessionError("err")
    with pytest.raises(NetworkError):
        raise NetworkError("err")
    with pytest.raises(AuthError):
        raise AuthError("err")
        
    fw = FloodWait(45)
    assert fw.seconds == 45
    assert fw.code == 420
    assert "FLOOD_WAIT_45" in str(fw)

def test_queue_models():
    qt = QueueTask(1, lambda: None)
    assert qt.priority == 1

@pytest.mark.asyncio
async def test_queue_exception_and_sync_job():
    q = PriorityQueue(num_workers=1)
    await q.start()
    
    run_vals = []
    def sync_job(val):
        run_vals.append(val)
        
    def sync_error_job():
        raise ValueError("error")
        
    await q.push(1, sync_job, "hello")
    await q.push(2, sync_error_job)
    
    await asyncio.sleep(0.2)
    assert "hello" in run_vals
    await q.stop()

@pytest.mark.asyncio
async def test_scheduler_cancel_and_interval():
    sched = TaskScheduler()
    await sched.start()
    
    run_vals = []
    def job():
        run_vals.append(1)
        
    task = await sched.schedule(job, delay=0.01, interval=0.05)
    await asyncio.sleep(0.25)
    assert len(run_vals) >= 2
    
    await sched.cancel(task)
    len_before = len(run_vals)
    await asyncio.sleep(0.15)
    assert len(run_vals) == len_before
    
    def error_job():
        raise ValueError()
    await sched.schedule(error_job, delay=0.01)
    await asyncio.sleep(0.05)
    
    await sched.stop()

@pytest.mark.asyncio
async def test_pipeline_multiple_next_and_sync():
    pipe = MiddlewarePipeline()
    
    def sync_mid(event, next_call):
        return next_call()
        
    async def bad_mid(event, next_call):
        await next_call()
        return await next_call()
        
    pipe.use(sync_mid)
    pipe.use(bad_mid)
    
    async def handler(event):
        return "ok"
        
    with pytest.raises(RuntimeError):
        await pipe.execute("ev", handler)

def test_loader_missing_directories():
    disp = MagicMock()
    loader = PluginLoader(disp)
    loader.discover("non_existent_folder_abc")
    loader.unload_plugin("non_existent_plugin_abc")
    loader.reload_plugin("non_existent_plugin_abc")
    assert len(loader.loaded_plugins) == 0

@pytest.mark.asyncio
async def test_proxy_handshake_extra_branches():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [
        b"\x05\x02",
        b"\x01\x00",
        b"\x05\x00\x00\x01",
        b"\x7f\x00\x00\x01",
        b"\x00\x50"
    ]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080, username="u", password="p")
        await conn.connect()
        await conn.close()

@pytest.mark.asyncio
async def test_proxy_auth_failures():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [
        b"\x05\x02",
        b"\x01\x01"
    ]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080, username="u", password="p")
        with pytest.raises(NetworkError):
            await conn.connect()

@pytest.mark.asyncio
async def test_proxy_unsupported_type():
    conn = ProxyConnection("127.0.0.1", 80, "invalid_proxy", "127.0.0.1", 1080)
    mock_reader = AsyncMock()
    mock_writer = MagicMock()
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        with pytest.raises(NetworkError):
            await conn.connect()

@pytest.mark.asyncio
async def test_call_manager_methods():
    from drygram import DryClient
    client = DryClient("test_compat_methods", api_id=123, api_hash="abc")
    await client.start()
    
    with patch.object(client.engine, "send_rpc", new_callable=AsyncMock) as mock_send_rpc:
        mock_send_rpc.return_value = "ok"
        res1 = await client.invoke("query1")
        res2 = await client.send("query2")
        res3 = await client("query3")
        assert res1 == "ok"
        assert res2 == "ok"
        assert res3 == "ok"
        assert mock_send_rpc.call_count == 3
        
    handler = lambda x: x
    client.add_handler(handler)
    assert any(w.callback is handler for w in client.dispatcher.watchers.get(0, []))
    client.remove_handler(handler)
    assert not any(w.callback is handler for w in client.dispatcher.watchers.get(0, []))
    
    client.add_event_handler(handler)
    assert any(w.callback is handler for w in client.dispatcher.watchers.get(0, []))
    client.remove_event_handler(handler)
    assert not any(w.callback is handler for w in client.dispatcher.watchers.get(0, []))
    
    await client.stop()

def test_base_type_dict():
    btn = KeyboardButton("text")
    d = btn.to_dict()
    assert d["text"] == "text"

@pytest.mark.asyncio
async def test_connection_pool_timeout():
    mock_reader = AsyncMock()
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        pool = ConnectionPool("127.0.0.1", 80, pool_size=1)
        conn = await pool.acquire()
        assert conn is not None
        with pytest.raises(asyncio.TimeoutError):
            await pool.acquire()
        await pool.release(conn)
        await pool.close_all()

@pytest.mark.asyncio
async def test_pipeline_sync_non_awaitable():
    pipe = MiddlewarePipeline()
    def sync_mid(event, next_call):
        return "sync_val"
    pipe.use(sync_mid)
    res = await pipe.execute("ev", lambda e: "handler_val")
    assert res == "sync_val"

@pytest.mark.asyncio
async def test_dispatcher_callback_errors():
    from drygram.dispatch.dispatcher import Dispatcher
    from drygram.dispatch.watcher import Watcher
    from drygram import Message, Chat, User
    
    disp = Dispatcher()
    await disp.start()
    
    def bad_watcher_cb(event):
        raise ValueError("watcher error")
        
    watcher = Watcher(bad_watcher_cb)
    disp.add_watcher(watcher)
    
    chat = Chat(id=1, type="private")
    sender = User(id=12, first_name="u")
    msg = Message(id=100, date=0, chat=chat, sender=sender, text="hi")
    
    await disp.feed_signal(msg)
    await disp.stop()

def test_watcher_sync():
    from drygram.dispatch.watcher import Watcher
    res = []
    w = Watcher(lambda event: res.append(event))
    asyncio.run(w.execute("val"))
    assert res == ["val"]

@pytest.mark.asyncio
async def test_connection_errors():
    conn = Connection("127.0.0.1", 80)
    with pytest.raises(NetworkError):
        await conn.write(b"")
    with pytest.raises(NetworkError):
        await conn.read(4)
        
    with patch("asyncio.open_connection", side_effect=ValueError("connection failed")):
        with pytest.raises(NetworkError):
            await conn.connect()

@pytest.mark.asyncio
async def test_connection_write_read_failures():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = ValueError("read error")
    mock_writer = MagicMock()
    mock_writer.write.side_effect = ValueError("write error")
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = Connection("127.0.0.1", 80)
        await conn.connect()
        with pytest.raises(NetworkError):
            await conn.write(b"test")
        with pytest.raises(NetworkError):
            await conn.read(4)
        await conn.close()

@pytest.mark.asyncio
async def test_socks5_different_addresses():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [
        b"\x05\x00",
        b"\x05\x00\x00\x03",
        b"\x0b",
        b"example.com",
        b"\x00\x50"
    ]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("example.com", 80, "socks5", "127.0.0.1", 1080)
        await conn.connect()
        await conn.close()
        
    mock_reader_ipv6 = AsyncMock()
    mock_reader_ipv6.readexactly.side_effect = [
        b"\x05\x00",
        b"\x05\x00\x00\x04",
        b"\x00"*16,
        b"\x00\x50"
    ]
    with patch("asyncio.open_connection", return_value=(mock_reader_ipv6, mock_writer)):
        conn = ProxyConnection("::1", 80, "socks5", "127.0.0.1", 1080)
        await conn.connect()
        await conn.close()

@pytest.mark.asyncio
async def test_socks5_handshake_exceptions():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [b"\x04\x00"]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080)
        with pytest.raises(NetworkError):
            await conn.connect()
            
    mock_reader2 = AsyncMock()
    mock_reader2.readexactly.side_effect = [b"\x05\xff"]
    with patch("asyncio.open_connection", return_value=(mock_reader2, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080)
        with pytest.raises(NetworkError):
            await conn.connect()

    mock_reader3 = AsyncMock()
    mock_reader3.readexactly.side_effect = [b"\x05\x02"]
    with patch("asyncio.open_connection", return_value=(mock_reader3, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080)
        with pytest.raises(NetworkError):
            await conn.connect()

    mock_reader4 = AsyncMock()
    mock_reader4.readexactly.side_effect = [
        b"\x05\x00",
        b"\x04\x00\x00\x01"
    ]
    with patch("asyncio.open_connection", return_value=(mock_reader4, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080)
        with pytest.raises(NetworkError):
            await conn.connect()

    mock_reader5 = AsyncMock()
    mock_reader5.readexactly.side_effect = [
        b"\x05\x00",
        b"\x05\x01\x00\x01"
    ]
    with patch("asyncio.open_connection", return_value=(mock_reader5, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080)
        with pytest.raises(NetworkError):
            await conn.connect()

@pytest.mark.asyncio
async def test_http_proxy_exceptions():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [
        b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
    ]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "http", "127.0.0.1", 8080)
        with pytest.raises(NetworkError):
            await conn.connect()

    mock_reader2 = AsyncMock()
    mock_reader2.readexactly.return_value = b"x"
    with patch("asyncio.open_connection", return_value=(mock_reader2, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "http", "127.0.0.1", 8080)
        with pytest.raises(NetworkError):
            await conn.connect()

    mock_reader3 = AsyncMock()
    mock_reader3.readexactly.side_effect = [
        b"HTTP/1.1 200 OK\r\n\r\n"
    ]
    with patch("asyncio.open_connection", return_value=(mock_reader3, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "http", "127.0.0.1", 8080, username="u", password="p")
        await conn.connect()
        await conn.close()

@pytest.mark.asyncio
async def test_base_session_defaults():
    from drygram.sessions.base import BaseSession
    bs = BaseSession("default")
    await bs.load()
    await bs.save()
    await bs.delete()
    assert bs.dc_id == 1

@pytest.mark.asyncio
async def test_spec_extensions_coverage():
    from drygram import DryClient
    client = DryClient("test_spec_cov", api_id=123, api_hash="abc")
    await client.start()
    
    peer = await client.resolve_peer(12345)
    assert peer.user_id == 12345
    assert peer._type == "user"
    
    peer_ch = await client.resolve_peer(-10012345)
    assert peer_ch.channel_id == 10012345
    assert peer_ch._type == "channel"
    
    await client.stop()
    
    from drygram.parsers.markdown import MarkdownParser
    text_md = "**bold** *italic* __underline__ ~~strikethrough~~ ||spoiler|| `code` ```pre``` [link](http://url) [emoji](tg://emoji?id=99) @user > quote"
    t_md, ents_md = MarkdownParser.parse(text_md)
    assert len(ents_md) > 0
    
    from drygram.parsers.html import HTMLParser
    text_html = "<b>b</b> <strong>strong</strong> <i>i</i> <em>em</em> <u>u</u> <s>s</s> <strike>strike</strike> <del>del</del> <tg-spoiler>spoiler</tg-spoiler> <code>code</code> <pre>pre</pre> <blockquote>quote</blockquote> <a href='url'>link</a> <tg-emoji emoji-id='99'>emoji</tg-emoji> @user"
    # Replace single quotes with double quotes to match HTML regex
    text_html_clean = text_html.replace("'", '"')
    t_html, ents_html = HTMLParser.parse(text_html_clean)
    assert len(ents_html) > 0

@pytest.mark.asyncio
async def test_compat_coverage():
    from drygram.compat import (
        SessionManager, MediaUploader, MediaDownloader, BusinessManager,
        StoryManager, PremiumManager, StickerManager, EmojiManager,
        GiftManager, StarsManager, VoiceCallManager, VideoCallManager,
        Router, Signal, Channel, Group, KeyboardBuilder, Button,
        InlineKeyboard, ReplyKeyboard, CallbackButton, Logger, Cache, Storage
    )
    
    sm = SessionManager("my_session")
    assert sm.resolve().session_id == "my_session"
    
    sm2 = SessionManager(SQLiteSession("sess"))
    assert sm2.resolve().session_id == "sess"
    
    mu = MediaUploader(None)
    assert await mu.upload("path") == "uploaded_file_id"
    
    md = MediaDownloader(None)
    assert await md.download("id") == b"file_data"
    
    bm = BusinessManager(None)
    stm = StoryManager(None)
    pm = PremiumManager(None)
    stkm = StickerManager(None)
    emm = EmojiManager(None)
    gm = GiftManager(None)
    smgr = StarsManager(None)
    
    vcm = VoiceCallManager()
    vidm = VideoCallManager()
    rtr = Router()
    
    kb = KeyboardBuilder()
    kb.add("Hello")
    rep = kb.build_reply()
    assert len(rep.keyboard) == 1
    
    logger = Logger()
    logger.log_info("test")
    
    cache = Cache()
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("b") is None
    
    stor = Storage("test")
    assert stor.session_id == "test"

@pytest.mark.asyncio
async def test_bot_token_login():
    from drygram import DryClient
    client = DryClient("bot_sess", api_id=123, api_hash="abc", bot_token="123456:dummy_token")
    await client.start()
    assert client.session.is_bot is True
    assert client.me.is_bot is True
    assert client.me.username == "drygram_bot"
    await client.stop()

@pytest.mark.asyncio
async def test_command_and_gates_and_version():
    from drygram import version as v
    assert isinstance(v.version(), str)
    assert isinstance(v.version_tuple(), tuple)
    assert isinstance(v.full_version(), str)
    assert isinstance(v.build_info(), dict)
    assert isinstance(v.python_info(), dict)
    assert isinstance(v.platform_info(), dict)
    assert isinstance(v.architecture(), str)
    assert isinstance(v.framework_info(), dict)
    assert isinstance(v.telegram_layer(), int)
    assert isinstance(v.telegram_version(), str)
    assert isinstance(v.license_info(), str)
    assert isinstance(v.support_links(), dict)
    assert isinstance(v.banner(), str)
    assert isinstance(v.ascii_logo(), str)
    assert isinstance(v.installation_banner(), str)
    assert isinstance(v.startup_banner(), str)
    assert isinstance(v.runtime_report(), dict)
    assert isinstance(v.environment_report(), str)
    assert isinstance(v.dependency_report(), dict)
    assert v.check_python() in (True, False)
    assert v.check_dependencies() in (True, False)
    assert v.check_platform() in (True, False)
    assert isinstance(v.runtime_info(), dict)
    assert isinstance(v.__title__, str)
    assert isinstance(v.__version__, str)
    assert isinstance(v.__version_info__, tuple)
    assert isinstance(v.__release_date__, str)
    assert isinstance(v.__api_layer__, int)
    assert isinstance(v.__telegram_api_version__, str)
    assert isinstance(v.__author__, str)
    assert isinstance(v.__email__, str)
    assert isinstance(v.__license__, str)
    assert isinstance(v.__homepage__, str)
    assert isinstance(v.__repository__, str)
    assert isinstance(v.__documentation__, str)
    assert isinstance(v.__support_chat__, str)
    assert isinstance(v.__updates_channel__, str)
    assert isinstance(v.__python_requires__, str)
    
    # Test client decorators
    from drygram import DryClient
    client = DryClient("sess_dec", api_id=123, api_hash="abc")
    
    @client.trigger()
    async def h1(event):
        pass
        
    @client.capture()
    async def h2(event):
        pass
        
    @client.respond()
    async def h3(event):
        pass
        
    @client.listen()
    async def h4(event):
        pass
        
    @client.route()
    async def h5(event):
        pass
        
    @client.monitor()
    async def h6(event):
        pass
        
    @client.bind()
    async def h7(event):
        pass

    # Test Gate Logic
    from drygram.dispatch.gate import (
        TextGate, RegexGate, CaptionGate, PrivateGate, BotGate, OwnerGate, MediaGate
    )
    g1 = TextGate("hello")
    g2 = TextGate("world")
    
    and_gate = g1 & g2
    or_gate = g1 | g2
    not_gate = ~g1
    xor_gate = g1 ^ g2
    
    mock_msg = MagicMock()
    mock_msg.text = "hello"
    mock_msg.sender = MagicMock()
    mock_msg.sender.id = 12345678
    mock_msg.sender.is_bot = False
    mock_msg.chat = MagicMock()
    mock_msg.chat.type = "private"
    mock_msg.media = None
    
    assert and_gate(mock_msg) is False
    assert or_gate(mock_msg) is True
    assert not_gate(mock_msg) is False
    assert xor_gate(mock_msg) is True
    
    # Test text gates
    rg = RegexGate("^he")
    assert rg(mock_msg) is True
    
    # Test media gates
    mg = MediaGate()
    assert mg(mock_msg) is False
    
    # Test command system
    from drygram.commands.registry import CommandRegistry
    from drygram.commands.router import CommandRouter
    from drygram.commands.arguments import IntArg, EnumArg
    
    registry = CommandRegistry()
    
    called_vals = []
    async def my_cmd_cb(ctx, amount):
        called_vals.append(amount)
        
    registry.register(
        name="send",
        callback=my_cmd_cb,
        args=[IntArg("amount", required=True)],
        permissions=["owner"],
        cooldown=1.0,
        category="Admin",
        description="Send coins"
    )
    
    # Verify helper generator
    from drygram.commands.help import CommandHelpGenerator
    help_text = CommandHelpGenerator.generate("send", registry.get("send"))
    assert "send" in help_text
    
    router = CommandRouter(registry)
    
    # Set mock client helper
    async def mock_echo(msg, text):
        pass
    client.echo = mock_echo
    
    # Try routing command
    mock_msg.text = "/send 50"
    routed = await router.route(client, mock_msg)
    assert routed is True
    assert called_vals == [50]

@pytest.mark.asyncio
async def test_command_and_gates_full_coverage():
    from drygram.commands.aliases import CommandAliases
    from drygram.commands.autocomplete import CommandAutocomplete
    from drygram.commands.completion import CommandCompletion
    from drygram.commands.executor import CommandExecutor
    from drygram.commands.matcher import CommandMatcher
    from drygram.commands.validator import CommandValidator
    from drygram.commands.history import get_history
    from drygram.commands.analytics import get_statistics
    
    aliases = CommandAliases()
    aliases.add_alias("x", "y")
    assert aliases.aliases_map["x"] == "y"
    
    assert CommandAutocomplete.suggest("q", ["query"]) == ["query"]
    assert CommandCompletion.get_completions("cmd") == ["cmd"]
    assert await CommandExecutor.run(lambda: 123) == 123
    assert CommandMatcher.is_match("/cmd", "cmd") is True
    assert CommandValidator.validate(1, {}) is True
    
    assert isinstance(get_history(), list)
    assert isinstance(get_statistics(), dict)
    
    # Test all gates
    from drygram.dispatch.gate import (
        CaptionGate, MarkdownGate, HtmlGate, StartsWithGate, EndsWithGate,
        ContainsGate, LengthGate, LanguageGate, EmojiGate, PremiumEmojiGate,
        HashtagGate, MentionGate, URLGate, EmailGate, NumberGate, CodeBlockGate,
        QuoteGate, SpoilerGate, ImageGate, VideoGate, AnimationGate, GifGate,
        DocumentGate, ArchiveGate, VoiceGate, AudioGate, MusicGate, VideoNoteGate,
        StickerGate, PremiumStickerGate, AnimatedStickerGate, VectorStickerGate,
        AlbumGate, GroupGate, SuperGroupGate, BroadcastGate, ForumGate, TopicGate,
        BusinessGate, SecretGate, HumanGate, PremiumGate, VerifiedGate, ScamGate,
        FakeGate, SupportGate, DeveloperGate, JoinGate, LeaveGate, PromoteGate,
        DemoteGate, TitleGate, PhotoChangedGate, PinnedGate, MigrationGate,
        VoiceCallGate, VideoCallGate, ParticipantGate, SpeakerGate, MutedGate,
        ScreenShareGate, GreetingGate, AwayGate, QuickReplyGate, BusinessLinkGate,
        BusinessMessageGate, BusinessStoryGate, PremiumFeatureGate, BoostGate,
        StarGate, GiftGate, CollectibleGate, EffectGate, StoryGate, StoryReplyGate,
        StoryReactionGate, StoryArchiveGate, ReactionGate, CustomReactionGate,
        EmojiReactionGate, ScheduledGate, EditedGate, DeletedGate, ForwardedGate,
        ReplyGate, PinnedMessageGate, MentionedGate, AutoDeleteGate, FloodWaitGate,
        ConnectionGate, ReconnectGate, UpdateGate, SchedulerGate, WorkerGate,
        PluginGate, MiddlewareGate, Gates
    )
    
    mock_msg = MagicMock()
    mock_msg.text = "hello"
    mock_msg.caption = "cap"
    mock_msg.entities = [{"type": "bold"}, {"type": "spoiler"}, {"type": "pre"}, {"type": "blockquote"}]
    mock_msg.sender = MagicMock()
    mock_msg.sender.id = 12345678
    mock_msg.sender.language_code = "en"
    mock_msg.sender.is_business = False
    mock_msg.sender.is_premium = False
    mock_msg.sender.is_bot = False
    mock_msg.chat = MagicMock()
    mock_msg.chat.type = "supergroup"
    mock_msg.media = MagicMock()
    mock_msg.media.id = None
    mock_msg.media.file_unique_id = "phototemp"
    mock_msg.media.file_name = "test.zip"
    mock_msg.topic = None
    mock_msg.forward_from = None
    mock_msg.reply_to_message = None
    
    # Run all gates
    assert CaptionGate("cap")(mock_msg) is True
    assert MarkdownGate()(mock_msg) is True
    assert HtmlGate()(mock_msg) is True
    assert StartsWithGate("he")(mock_msg) is True
    assert EndsWithGate("lo")(mock_msg) is True
    assert ContainsGate("ell")(mock_msg) is True
    assert LengthGate(3, 10)(mock_msg) is True
    assert LanguageGate("en")(mock_msg) is True
    assert EmojiGate()(mock_msg) is False
    assert PremiumEmojiGate()(mock_msg) is False
    assert HashtagGate()(mock_msg) is False
    assert MentionGate()(mock_msg) is False
    assert URLGate()(mock_msg) is False
    assert EmailGate()(mock_msg) is False
    assert NumberGate()(mock_msg) is False
    assert CodeBlockGate()(mock_msg) is True
    assert QuoteGate()(mock_msg) is True
    assert SpoilerGate()(mock_msg) is True
    assert ImageGate()(mock_msg) is True
    assert VideoGate()(mock_msg) is False
    assert AnimationGate()(mock_msg) is False
    assert GifGate()(mock_msg) is False
    assert DocumentGate()(mock_msg) is False
    assert ArchiveGate()(mock_msg) is True
    assert VoiceGate()(mock_msg) is False
    assert AudioGate()(mock_msg) is False
    assert MusicGate()(mock_msg) is False
    assert VideoNoteGate()(mock_msg) is False
    assert StickerGate()(mock_msg) is False
    assert PremiumStickerGate()(mock_msg) is False
    assert AnimatedStickerGate()(mock_msg) is False
    assert VectorStickerGate()(mock_msg) is False
    assert AlbumGate()(mock_msg) is False
    assert GroupGate()(mock_msg) is True
    assert SuperGroupGate()(mock_msg) is True
    assert BroadcastGate()(mock_msg) is False
    assert ForumGate()(mock_msg) is True
    assert TopicGate()(mock_msg) is False
    assert BusinessGate()(mock_msg) is False
    assert SecretGate()(mock_msg) is False
    assert HumanGate()(mock_msg) is True
    assert PremiumGate()(mock_msg) is False
    assert VerifiedGate()(mock_msg) is True
    assert ScamGate()(mock_msg) is False
    assert FakeGate()(mock_msg) is False
    assert SupportGate()(mock_msg) is False
    assert DeveloperGate()(mock_msg) is True
    assert JoinGate()(mock_msg) is False
    assert LeaveGate()(mock_msg) is False
    assert PromoteGate()(mock_msg) is False
    assert DemoteGate()(mock_msg) is False
    assert TitleGate()(mock_msg) is False
    assert PhotoChangedGate()(mock_msg) is False
    assert PinnedGate()(mock_msg) is False
    assert MigrationGate()(mock_msg) is False
    assert VoiceCallGate()(mock_msg) is False
    assert VideoCallGate()(mock_msg) is False
    assert ParticipantGate()(mock_msg) is False
    assert SpeakerGate()(mock_msg) is False
    assert MutedGate()(mock_msg) is False
    assert ScreenShareGate()(mock_msg) is False
    assert GreetingGate()(mock_msg) is False
    assert AwayGate()(mock_msg) is False
    assert QuickReplyGate()(mock_msg) is False
    assert BusinessLinkGate()(mock_msg) is False
    assert BusinessMessageGate()(mock_msg) is False
    assert BusinessStoryGate()(mock_msg) is False
    assert PremiumFeatureGate()(mock_msg) is False
    assert BoostGate()(mock_msg) is False
    assert StarGate()(mock_msg) is False
    assert GiftGate()(mock_msg) is False
    assert CollectibleGate()(mock_msg) is False
    assert EffectGate()(mock_msg) is False
    assert StoryGate()(mock_msg) is False
    assert StoryReplyGate()(mock_msg) is False
    assert StoryReactionGate()(mock_msg) is False
    assert StoryArchiveGate()(mock_msg) is False
    assert ReactionGate()(mock_msg) is False
    assert CustomReactionGate()(mock_msg) is False
    assert EmojiReactionGate()(mock_msg) is False
    assert ScheduledGate()(mock_msg) is False
    assert EditedGate()(mock_msg) is False
    assert DeletedGate()(mock_msg) is False
    assert ForwardedGate()(mock_msg) is False
    assert ReplyGate()(mock_msg) is False
    assert PinnedMessageGate()(mock_msg) is False
    assert MentionedGate()(mock_msg) is False
    assert AutoDeleteGate()(mock_msg) is False
    assert FloodWaitGate()(mock_msg) is False
    assert ConnectionGate()(mock_msg) is False
    assert ReconnectGate()(mock_msg) is False
    assert UpdateGate()(mock_msg) is False
    assert SchedulerGate()(mock_msg) is False
    assert WorkerGate()(mock_msg) is False
    assert PluginGate()(mock_msg) is False
    assert MiddlewareGate()(mock_msg) is False
    
    # Test factory
    assert Gates.all_signals()(mock_msg) is True
    assert Gates.text("hello")(mock_msg) is True
    assert Gates.regex("^he")(mock_msg) is True
    assert Gates.private()(mock_msg) is False
    assert Gates.group()(mock_msg) is True
    assert Gates.channel()(mock_msg) is False
    assert Gates.sender(12345678)(mock_msg) is True
    assert Gates.premium()(mock_msg) is False
    assert Gates.business()(mock_msg) is False


def test_crypto_backends():
    from drygram.crypto.backend import (
        current_backend,
        backend_name,
        backend_version,
        supports_acceleration,
        is_accelerated,
        encrypt_ige,
        decrypt_ige
    )
    
    assert current_backend() == "cryptography"
    assert isinstance(backend_name, str)
    assert isinstance(backend_version, str)
    assert supports_acceleration() is False
    assert is_accelerated() is False
    
    key = b"1" * 32
    iv = b"2" * 32
    data = b"hello world 1234" # 16 bytes
    
    enc = encrypt_ige(data, key, iv)
    dec = decrypt_ige(enc, key, iv)
    assert dec == data




