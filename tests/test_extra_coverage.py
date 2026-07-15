# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from drygram import (
    DryError, SessionError, NetworkError, AuthError, FloodWait, RPCError,
    TaskScheduler, CallParticipant, CallManager, KeyboardButton, SQLiteSession
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
    cm = CallManager()
    await cm.enter_room(123)
    assert cm.playing is True
    
    await cm.seek(123, 10)
    await cm.add_to_queue("music2.mp3")
    assert cm.queue == ["music2.mp3"]
    
    await cm.set_volume(250)
    assert cm.volume == 200
    
    await cm.mute()
    assert cm.muted is True
    await cm.unmute()
    assert cm.muted is False
    
    await cm.start_recording("rec.wav")
    assert cm.is_recording is True
    assert cm.recording_file == "rec.wav"
    await cm.stop_recording()
    assert cm.is_recording is False
    
    def bad_callback(p):
        raise ValueError("bad participant")
    cm.on_participant_event(bad_callback)
    await cm.trigger_participant_event(CallParticipant(99))
    
    await cm.exit_room(123)

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
    from drygram.calls.manager import CallManager, CallParticipant
    cm = CallManager()
    await cm.enter_room(1)
    await cm.stream_video(1, "source", quality="1080p")
    await cm.pause(1)
    await cm.resume(1)
    await cm.seek(1, 100)
    await cm.start_screen_share(1)
    await cm.stop_screen_share(1)
    await cm.set_video_quality("1080p")
    await cm.toggle_adaptive_streaming(False)
    
    speakers_list = []
    cm.on_speaker_detection(lambda ids: speakers_list.extend(ids))
    await cm.trigger_speaker_detection([123])
    assert speakers_list == [123]
    
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

