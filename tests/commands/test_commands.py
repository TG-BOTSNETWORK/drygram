# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
from decimal import Decimal
from drygram.commands import (
    CommandParser,
    PrefixManager,
    AliasManager,
    CommandMatcher,
    CommandPermission,
    CooldownManager,
    Autocompleter,
    SyntaxEscaper,
    RichText,
    MarkdownBuilder,
    HTMLBuilder,
    CodeBuilder,
    QuoteBuilder,
    LinkBuilder,
    MentionBuilder,
    EmojiBuilder,
    TableBuilder,
    ListBuilder,
    MessageBuilder,
    CommandRegistry,
    Command,
    CommandContext,
    CommandExecutor
)

def test_command_parser():
    # standard parsing
    args, flags = CommandParser.parse("hello world --force -n test")
    assert args == ["hello", "world"]
    assert flags == {"force": True, "n": "test"}

    # nested quotes and escape characters
    args_quoted, flags_quoted = CommandParser.parse("greet \"Santhu 'developer'\" --msg \"hello world\"")
    assert args_quoted == ["greet", "Santhu 'developer'"]
    assert flags_quoted == {"msg": "hello world"}

def test_prefix_manager():
    mgr = PrefixManager(default_prefixes=["/"])
    class DummyChat: id = 111
    class DummySender: id = 222
    class DummyMsg:
        chat = DummyChat()
        sender = DummySender()
    
    assert mgr.resolve(None, DummyMsg()) == ["/"]

    mgr.set_chat_prefixes(111, ["!"])
    assert mgr.resolve(None, DummyMsg()) == ["!"]

def test_alias_manager():
    mgr = AliasManager()
    mgr.register_alias("st", "status")
    assert mgr.resolve_alias("st") == "status"
    assert mgr.resolve_alias("status") == "status"

def test_command_matcher():
    res = CommandMatcher.match_trigger("/start hello world", ["/"])
    assert res == ("start", "hello world")
    
    res_none = CommandMatcher.match_trigger("hello world", ["/"])
    assert res_none is None

def test_command_permissions():
    perms = CommandPermission(private_only=True)
    class DummyChat: type = "group"
    class DummySender: id = 222
    class DummyMsg:
        chat = DummyChat()
        sender = DummySender()
    class DummyContext:
        chat = DummyChat()
        user = DummySender()
        message = DummyMsg()
        
    assert not perms.check(DummyContext())

def test_cooldown_manager():
    mgr = CooldownManager(rate=2, per=1.0)
    is_limited, rem = mgr.check_cooldown("user1")
    assert not is_limited
    mgr.update_cooldown("user1")
    
    is_limited, rem = mgr.check_cooldown("user1")
    assert not is_limited
    mgr.update_cooldown("user1")
    
    is_limited, rem = mgr.check_cooldown("user1")
    assert is_limited
    assert rem > 0.0

def test_autocompleter():
    comp = Autocompleter(choices=["apple", "banana", "cherry"])
    assert comp.get_suggestions("a") == ["apple", "banana"]

def test_rich_text_builders():
    # RichText HTML / Markdown output
    rt = RichText().bold("hello").text(" ").italic("world")
    assert rt.to_html() == "<b>hello</b> <i>world</i>"
    assert rt.to_markdown() == "*hello* _world_"

    # Builders
    assert MarkdownBuilder().bold("hi").build() == "*hi*"
    assert HTMLBuilder().italic("hi").build() == "<i>hi</i>"
    assert CodeBuilder("python").add_line("print()").to_markdown() == "```python\nprint()\n```"
    assert QuoteBuilder().content("quote").to_html() == "<blockquote>quote</blockquote>"
    assert LinkBuilder().label("google").url("http://google.com").to_html() == '<a href="http://google.com">google</a>'
    assert MentionBuilder().label("user").user_id(123).to_markdown() == "[user](tg://user?id=123)"
    assert EmojiBuilder().char("🔥").emoji_id(999).to_html() == '<tg-emoji emoji-id="999">🔥</tg-emoji>'

def test_list_table_builders():
    lst = ListBuilder(ordered=True).add_item("first").add_item("second")
    assert lst.to_html() == "<ol>\n<li>first</li>\n<li>second</li>\n</ol>"
    
    tbl = TableBuilder().add_headers("name", "age").add_row("john", "25")
    assert "john | 25" in tbl.to_markdown()

@pytest.mark.asyncio
async def test_command_execution():
    registry = CommandRegistry()
    called = False
    
    def test_cmd(ctx: CommandContext, name: str, force: bool = False):
        nonlocal called
        called = True
        assert name == "Santhu"
        assert force is True
        
    cmd = Command("test", test_cmd)
    registry.register_command(cmd)
    
    class DummyClient:
        session = None
        raw = None
        dispatcher = None
        network = None
        storage = None
        
    class DummyMsg:
        chat = None
        sender = None
        
    ctx = CommandContext(DummyClient(), DummyMsg(), cmd, ["Santhu"], {"force": True})
    await CommandExecutor.execute(ctx)
    assert called is True
