# Asynchronous Voice Calls

DryGram provides a high-level API to handle direct voice calls and manage group voice chats natively on the MTProto layer.

## Starting 1-on-1 Calls

To start a direct voice call with another user:

```python
success = await client.voice_call(user_id=123456)
```

## Group Voice Chats

To join an active group voice chat:

```python
await client.join_voice(chat_id=-10012345678)
```

To leave:

```python
await client.leave_voice(chat_id=-10012345678)
```

## Integration with WebRTC

You can pipe audio tracks into voice chats using Webrtc clients:

```python
from py_tgcalls import PyTgCalls
from py_tgcalls import Stream

call = PyTgCalls(client)
await call.start()
await call.join_group_call(-10012345678, Stream.get_input_stream())
```
