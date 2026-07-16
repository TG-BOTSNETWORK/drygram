# Video Calls & Conferences

DryGram supports conducting video calls and joining supergroup video conferences.

## Starting Video Calls

```python
success = await client.video_call(user_id=123456)
```

## Joining Video Conferences

```python
await client.join_video(chat_id=-10012345678)
```

To leave:

```python
await client.leave_video(chat_id=-10012345678)
```

## Stream Video Feeds

Stream video files using Webrtc:

```python
from ntgcalls import NTgCalls
from ntgcalls import VideoStream

tg_calls = NTgCalls(client)
await tg_calls.join(
    chat_id=-10012345678,
    video_stream=VideoStream.from_file("video.mp4")
)
```
