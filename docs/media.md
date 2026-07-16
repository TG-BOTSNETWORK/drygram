# Media Handling Guide

DryGram supports delivering and downloading diverse media types including photos, videos, audio, voice notes, documents, and location coordinates.

## Delivering Media

Use high-level methods to send media directly to any chat:

### Sending Audio File
```python
message = await client.deliver_audio(
    chat_id=123456,
    file="path/to/song.mp3",
    caption="Check this out!"
)
```

### Sending Voice Note
```python
message = await client.deliver_voice(
    chat_id=123456,
    file="path/to/voice_note.ogg",
    caption="Voice message"
)
```

### Sending Location
```python
message = await client.send_location(
    chat_id=123456,
    latitude=51.5074,
    longitude=-0.1278
)
```

## Media Classes Reference

- `Photo`: Encapsulates Telegram photo sizes and image files.
- `Video`: Encapsulates video file attributes (duration, width, height).
- `Audio`: Encapsulates audio song properties (duration, performer, title).
- `VoiceNote`: Encapsulates voice message duration and unique file identifiers.
- `Document`: Represents general attachments (e.g. PDFs, archives).
- `Location`: Holds geographic latitude and longitude coordinates.
