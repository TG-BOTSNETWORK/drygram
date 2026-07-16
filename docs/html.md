# HTML Parsing

DryGram includes an HTML parser to render Telegram entities using standard HTML formatting tags.

## Formatting Messages with HTML

Specify `parse_mode="html"` when delivering messages:

```python
await client.deliver(
    chat_id=123456,
    text="Welcome <b>User</b>! Visit our <a href='https://telegram.org'>website</a>.",
    parse_mode="html"
)
```

## Supported HTML Tags

- `<b>` or `<strong>`: **Bold**
- `<i>` or `<em>`: *Italics*
- `<code>`: `Code block`
- `<pre>`: Monospace pre-formatted text block.
- `<a href="...">`: Hyperlink
- `<u>`: Underline
- `<s>`: Strikethrough
