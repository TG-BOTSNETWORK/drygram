# Markdown Parsing

DryGram includes a high-performance markdown parser to apply text formatting (bold, italic, code blocks, links) to sent messages.

## Basic Formatting

The markdown parser is active by default when sending messages:

```python
# Delivers formatted text using markdown syntax
await client.deliver(
    chat_id=123456,
    text="This is **bold** and *italic* text, with `inline code`."
)
```

## Supported Markdown Entities

- **Bold**: `**text**` or `__text__`
- *Italics*: `*text*` or `_text_`
- `Code`: `` `code` ``
- [Links](https://telegram.org): `[text](url)`
- Spoiled: `||text||`
