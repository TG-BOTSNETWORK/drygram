# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import html

class SyntaxEscaper:
    """
    Handles character escaping for MarkdownV2 and HTML rendering.
    """
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape text for safe HTML formatting."""
        return html.escape(text)

    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        """Escape text for safe Telegram MarkdownV2 formatting."""
        special_chars = r"_*[]()~`>#+-=|{}.!"
        escaped = []
        for char in text:
            if char in special_chars:
                escaped.append("\\" + char)
            else:
                escaped.append(char)
        return "".join(escaped)
