# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import List, Tuple, Any, Optional
from drygram.commands.syntax import SyntaxEscaper

class RichText:
    """
    Constructs complex message formatting structures via chainable builders.
    Supports both HTML and MarkdownV2 compilation output targets.
    """
    def __init__(self) -> None:
        self.segments: List[Tuple[str, Any]] = []

    def text(self, val: str) -> "RichText":
        self.segments.append(("text", val))
        return self

    def bold(self, val: str) -> "RichText":
        self.segments.append(("bold", val))
        return self

    def italic(self, val: str) -> "RichText":
        self.segments.append(("italic", val))
        return self

    def underline(self, val: str) -> "RichText":
        self.segments.append(("underline", val))
        return self

    def strikethrough(self, val: str) -> "RichText":
        self.segments.append(("strikethrough", val))
        return self

    def spoiler(self, val: str) -> "RichText":
        self.segments.append(("spoiler", val))
        return self

    def code(self, val: str) -> "RichText":
        self.segments.append(("code", val))
        return self

    def code_block(self, val: str, language: str = "") -> "RichText":
        self.segments.append(("code_block", (val, language)))
        return self

    def blockquote(self, val: str, expandable: bool = False) -> "RichText":
        self.segments.append(("blockquote", (val, expandable)))
        return self

    def link(self, label: str, url: str) -> "RichText":
        self.segments.append(("link", (label, url)))
        return self

    def mention(self, label: str, user_id: int) -> "RichText":
        self.segments.append(("mention", (label, user_id)))
        return self

    def emoji(self, char: str, emoji_id: Optional[int] = None) -> "RichText":
        self.segments.append(("emoji", (char, emoji_id)))
        return self

    def to_markdown(self) -> str:
        """Compile segments to MarkdownV2 formatting string."""
        res = []
        for tag, content in self.segments:
            if tag == "text":
                res.append(SyntaxEscaper.escape_markdown_v2(content))
            elif tag == "bold":
                res.append(f"*{SyntaxEscaper.escape_markdown_v2(content)}*")
            elif tag == "italic":
                res.append(f"_{SyntaxEscaper.escape_markdown_v2(content)}_")
            elif tag == "underline":
                res.append(f"__{SyntaxEscaper.escape_markdown_v2(content)}__")
            elif tag == "strikethrough":
                res.append(f"~{SyntaxEscaper.escape_markdown_v2(content)}~")
            elif tag == "spoiler":
                res.append(f"||{SyntaxEscaper.escape_markdown_v2(content)}||")
            elif tag == "code":
                res.append(f"`{SyntaxEscaper.escape_markdown_v2(content)}`")
            elif tag == "code_block":
                val, lang = content
                res.append(f"```{lang}\n{val}\n```")
            elif tag == "blockquote":
                val, exp = content
                escaped_val = SyntaxEscaper.escape_markdown_v2(val)
                lines = [f"> {line}" for line in escaped_val.split("\n")]
                res.append("\n".join(lines))
            elif tag == "link":
                lbl, url = content
                res.append(f"[{SyntaxEscaper.escape_markdown_v2(lbl)}]({url})")
            elif tag == "mention":
                lbl, uid = content
                res.append(f"[{SyntaxEscaper.escape_markdown_v2(lbl)}](tg://user?id={uid})")
            elif tag == "emoji":
                char, eid = content
                if eid:
                    res.append(f"[{char}](tg://emoji?id={eid})")
                else:
                    res.append(char)
        return "".join(res)

    def to_html(self) -> str:
        """Compile segments to HTML formatting string."""
        res = []
        for tag, content in self.segments:
            if tag == "text":
                res.append(SyntaxEscaper.escape_html(content))
            elif tag == "bold":
                res.append(f"<b>{SyntaxEscaper.escape_html(content)}</b>")
            elif tag == "italic":
                res.append(f"<i>{SyntaxEscaper.escape_html(content)}</i>")
            elif tag == "underline":
                res.append(f"<u>{SyntaxEscaper.escape_html(content)}</u>")
            elif tag == "strikethrough":
                res.append(f"<s>{SyntaxEscaper.escape_html(content)}</s>")
            elif tag == "spoiler":
                res.append(f"<tg-spoiler>{SyntaxEscaper.escape_html(content)}</tg-spoiler>")
            elif tag == "code":
                res.append(f"<code>{SyntaxEscaper.escape_html(content)}</code>")
            elif tag == "code_block":
                val, lang = content
                lang_attr = f' class="language-{lang}"' if lang else ""
                res.append(f"<pre><code{lang_attr}>{SyntaxEscaper.escape_html(val)}</code></pre>")
            elif tag == "blockquote":
                val, exp = content
                exp_attr = " expandable" if exp else ""
                res.append(f"<blockquote{exp_attr}>{SyntaxEscaper.escape_html(val)}</blockquote>")
            elif tag == "link":
                lbl, url = content
                res.append(f'<a href="{url}">{SyntaxEscaper.escape_html(lbl)}</a>')
            elif tag == "mention":
                lbl, uid = content
                res.append(f'<a href="tg://user?id={uid}">{SyntaxEscaper.escape_html(lbl)}</a>')
            elif tag == "emoji":
                char, eid = content
                if eid:
                    res.append(f'<tg-emoji emoji-id="{eid}">{char}</tg-emoji>')
                else:
                    res.append(char)
        return "".join(res)

class MarkdownBuilder:
    """Targeted MarkdownV2 text formatter."""
    def __init__(self) -> None:
        self._rt = RichText()
    def text(self, val: str) -> "MarkdownBuilder": self._rt.text(val); return self
    def bold(self, val: str) -> "MarkdownBuilder": self._rt.bold(val); return self
    def italic(self, val: str) -> "MarkdownBuilder": self._rt.italic(val); return self
    def underline(self, val: str) -> "MarkdownBuilder": self._rt.underline(val); return self
    def strikethrough(self, val: str) -> "MarkdownBuilder": self._rt.strikethrough(val); return self
    def spoiler(self, val: str) -> "MarkdownBuilder": self._rt.spoiler(val); return self
    def code(self, val: str) -> "MarkdownBuilder": self._rt.code(val); return self
    def code_block(self, val: str, language: str = "") -> "MarkdownBuilder": self._rt.code_block(val, language); return self
    def blockquote(self, val: str, expandable: bool = False) -> "MarkdownBuilder": self._rt.blockquote(val, expandable); return self
    def link(self, label: str, url: str) -> "MarkdownBuilder": self._rt.link(label, url); return self
    def mention(self, label: str, user_id: int) -> "MarkdownBuilder": self._rt.mention(label, user_id); return self
    def emoji(self, char: str, emoji_id: Optional[int] = None) -> "MarkdownBuilder": self._rt.emoji(char, emoji_id); return self
    def build(self) -> str: return self._rt.to_markdown()

class HTMLBuilder:
    """Targeted HTML text formatter."""
    def __init__(self) -> None:
        self._rt = RichText()
    def text(self, val: str) -> "HTMLBuilder": self._rt.text(val); return self
    def bold(self, val: str) -> "HTMLBuilder": self._rt.bold(val); return self
    def italic(self, val: str) -> "HTMLBuilder": self._rt.italic(val); return self
    def underline(self, val: str) -> "HTMLBuilder": self._rt.underline(val); return self
    def strikethrough(self, val: str) -> "HTMLBuilder": self._rt.strikethrough(val); return self
    def spoiler(self, val: str) -> "HTMLBuilder": self._rt.spoiler(val); return self
    def code(self, val: str) -> "HTMLBuilder": self._rt.code(val); return self
    def code_block(self, val: str, language: str = "") -> "HTMLBuilder": self._rt.code_block(val, language); return self
    def blockquote(self, val: str, expandable: bool = False) -> "HTMLBuilder": self._rt.blockquote(val, expandable); return self
    def link(self, label: str, url: str) -> "HTMLBuilder": self._rt.link(label, url); return self
    def mention(self, label: str, user_id: int) -> "HTMLBuilder": self._rt.mention(label, user_id); return self
    def emoji(self, char: str, emoji_id: Optional[int] = None) -> "HTMLBuilder": self._rt.emoji(char, emoji_id); return self
    def build(self) -> str: return self._rt.to_html()

class CodeBuilder:
    """Syntax highlighted block code builder."""
    def __init__(self, language: str = "") -> None:
        self.language = language
        self.lines: List[str] = []
    def add_line(self, line: str) -> "CodeBuilder":
        self.lines.append(line)
        return self
    def to_markdown(self) -> str:
        return f"```{self.language}\n" + "\n".join(self.lines) + "\n```"
    def to_html(self) -> str:
        lang_attr = f' class="language-{self.language}"' if self.language else ""
        return f"<pre><code{lang_attr}>" + SyntaxEscaper.escape_html("\n".join(self.lines)) + "</code></pre>"

class QuoteBuilder:
    """Blockquote and quotation snippet builder."""
    def __init__(self, expandable: bool = False) -> None:
        self.expandable = expandable
        self.text_content = ""
    def content(self, text: str) -> "QuoteBuilder":
        self.text_content = text
        return self
    def to_markdown(self) -> str:
        escaped = SyntaxEscaper.escape_markdown_v2(self.text_content)
        return "\n".join(f"> {line}" for line in escaped.split("\n"))
    def to_html(self) -> str:
        exp_attr = " expandable" if self.expandable else ""
        return f"<blockquote{exp_attr}>" + SyntaxEscaper.escape_html(self.text_content) + "</blockquote>"

class LinkBuilder:
    """Format and build links."""
    def __init__(self) -> None:
        self._label = ""
        self._url = ""
    def label(self, val: str) -> "LinkBuilder": self._label = val; return self
    def url(self, val: str) -> "LinkBuilder": self._url = val; return self
    def to_markdown(self) -> str:
        return f"[{SyntaxEscaper.escape_markdown_v2(self._label)}]({self._url})"
    def to_html(self) -> str:
        return f'<a href="{self._url}">{SyntaxEscaper.escape_html(self._label)}</a>'

class MentionBuilder:
    """Format and build inline user mentions."""
    def __init__(self) -> None:
        self._label = ""
        self._user_id = 0
    def label(self, val: str) -> "MentionBuilder": self._label = val; return self
    def user_id(self, val: int) -> "MentionBuilder": self._user_id = val; return self
    def to_markdown(self) -> str:
        return f"[{SyntaxEscaper.escape_markdown_v2(self._label)}](tg://user?id={self._user_id})"
    def to_html(self) -> str:
        return f'<a href="tg://user?id={self._user_id}">{SyntaxEscaper.escape_html(self._label)}</a>'

class EmojiBuilder:
    """Format and build custom/Premium emoji markup."""
    def __init__(self) -> None:
        self._char = ""
        self._emoji_id = 0
    def char(self, val: str) -> "EmojiBuilder": self._char = val; return self
    def emoji_id(self, val: int) -> "EmojiBuilder": self._emoji_id = val; return self
    def to_markdown(self) -> str:
        return f"[{self._char}](tg://emoji?id={self._emoji_id})"
    def to_html(self) -> str:
        return f'<tg-emoji emoji-id="{self._emoji_id}">{self._char}</tg-emoji>'

class TableBuilder:
    """Generate inline text tables."""
    def __init__(self) -> None:
        self.headers: List[str] = []
        self.rows: List[List[str]] = []
    def add_headers(self, *headers: str) -> "TableBuilder":
        self.headers = list(headers)
        return self
    def add_row(self, *row: str) -> "TableBuilder":
        self.rows.append(list(row))
        return self
    def to_markdown(self) -> str:
        lines = []
        if self.headers:
            lines.append(" | ".join(SyntaxEscaper.escape_markdown_v2(h) for h in self.headers))
            lines.append("-|-".join("-" * len(h) for h in self.headers))
        for row in self.rows:
            lines.append(" | ".join(SyntaxEscaper.escape_markdown_v2(r) for r in row))
        return "\n".join(lines)
    def to_html(self) -> str:
        lines = ["<table>"]
        if self.headers:
            lines.append("<tr>" + "".join(f"<th>{SyntaxEscaper.escape_html(h)}</th>" for h in self.headers) + "</tr>")
        for row in self.rows:
            lines.append("<tr>" + "".join(f"<td>{SyntaxEscaper.escape_html(r)}</td>" for r in row) + "</tr>")
        lines.append("</table>")
        return "\n".join(lines)

class ListBuilder:
    """Format ordered or unordered list collections."""
    def __init__(self, ordered: bool = False) -> None:
        self.ordered = ordered
        self.items: List[str] = []
    def add_item(self, item: str) -> "ListBuilder":
        self.items.append(item)
        return self
    def to_markdown(self) -> str:
        lines = []
        for i, item in enumerate(self.items, 1):
            prefix = f"{i}\\. " if self.ordered else "• "
            lines.append(f"{prefix}{SyntaxEscaper.escape_markdown_v2(item)}")
        return "\n".join(lines)
    def to_html(self) -> str:
        tag = "ol" if self.ordered else "ul"
        lines = [f"<{tag}>"]
        for item in self.items:
            lines.append(f"<li>{SyntaxEscaper.escape_html(item)}</li>")
        lines.append(f"</{tag}>")
        return "\n".join(lines)

class MessageBuilder:
    """Compiles overall message payloads."""
    def __init__(self) -> None:
        self._rt = RichText()
    def text(self, val: str) -> "MessageBuilder": self._rt.text(val); return self
    def bold(self, val: str) -> "MessageBuilder": self._rt.bold(val); return self
    def italic(self, val: str) -> "MessageBuilder": self._rt.italic(val); return self
    def underline(self, val: str) -> "MessageBuilder": self._rt.underline(val); return self
    def code(self, val: str) -> "MessageBuilder": self._rt.code(val); return self
    def build_markdown(self) -> str: return self._rt.to_markdown()
    def build_html(self) -> str: return self._rt.to_html()
