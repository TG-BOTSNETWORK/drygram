# Composable Filters (Gates)

Gates are boolean filters used to route incoming updates to specific observers. They can be combined using Python's bitwise operators (`&` for AND, `|` for OR, `~` for NOT).

## Composing Gates

```python
from drygram import Gates

# Matches messages containing text in private chats, EXCEPT when the text is "ping"
my_gate = Gates.private() & Gates.text() & ~Gates.text("ping")

# Matches images in either private chats or group chats
media_gate = Gates.media() & (Gates.private() | Gates.group())
```

## Built-In Gates Reference

| Filter | Description | Example |
|---|---|---|
| `Gates.private()` | Incoming message is from a private chat | `Gates.private()` |
| `Gates.group()` | Incoming message is from a group or supergroup | `Gates.group()` |
| `Gates.channel()` | Incoming message is from a channel | `Gates.channel()` |
| `Gates.text(query)` | Matches text messages; optionally checks for specific query | `Gates.text("hello")` |
| `Gates.media()` | Message contains photo, video, document, or audio | `Gates.media()` |
| `Gates.photo()` | Message contains photo media | `Gates.photo()` |
| `Gates.video()` | Message contains video media | `Gates.video()` |
| `Gates.voice()` | Message contains voice note | `Gates.voice()` |
| `Gates.document()` | Message contains general file attachment | `Gates.document()` |

## Custom Gates

You can implement custom filtering logic by subclassing `Gate` or using `Gate.create`:

```python
from drygram import Gate, Message

# Create a gate that matches messages sent by administrators
def check_admin(msg: Message) -> bool:
    # Custom checker logic
    return getattr(msg.sender, "is_admin", False)

admin_gate = Gate.create(check_admin)
```
