# WebRTC Streaming & Playlists

DryGram supports advanced WebRTC audio/video streaming, playback playlists, queues, volume control, pausing, and resuming.

## Playlists and Queues

Manage track playlists by piping media chunks sequentially to the voice chat connection:

```python
playlist = ["song1.raw", "song2.raw", "song3.raw"]

for track in playlist:
    print(f"Streaming track: {track}")
    # Stream data chunks to Webrtc connection socket
```

## Control Hooks

- **Pause**: Pause Webrtc playback stream.
- **Resume**: Resume Webrtc playback stream.
- **Volume**: Scale audio input values dynamically.
- **Record**: Record incoming audio chunks from other participants.

## ntgcalls Integration

```python
from ntgcalls import NTgCalls
from ntgcalls import Stream

calls = NTgCalls(client)
await calls.join(chat_id=-10012345678, stream=Stream.from_file("audio.raw"))

# Pause stream
calls.pause()

# Resume stream
calls.resume()

# Set volume
calls.set_volume(80)
```
