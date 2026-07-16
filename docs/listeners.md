# Update Listeners & Observers

Observers register callbacks to receive events processed by the dispatcher.

## Registering Observers

### Private Messages Watcher
```python
from drygram import DryClient, Gates, Message

app = DryClient("session_app", api_id=123, api_hash="abc")

@app.observe(Gates.private())
async def private_msg_observer(msg: Message):
    print(f"Message from {msg.sender.first_name}: {msg.text}")
```

### Channel Watcher
```python
@app.observe(Gates.channel())
async def channel_post_observer(msg: Message):
    print(f"Channel post: {msg.text}")
```

## Advanced Listeners

DryGram provides low-level listener classes under `drygram.compat` for subscribing to custom streams (such as raw update objects or connection changes):

```python
from drygram.compat import ConnectionListener

class MyConnectionWatcher(ConnectionListener):
    async def on_connect(self):
        print("Connected to Telegram DC")
        
    async def on_disconnect(self, exception):
        print(f"Connection lost: {exception}")

# Register custom listener
app.add_listener(MyConnectionWatcher())
```
