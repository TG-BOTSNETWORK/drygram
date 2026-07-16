# Messages & Delivery

DryGram provides a full suite of helper methods for delivering, editing, deleting, forwarding, and copying messages in private chats, groups, and channels.

## Delivering Messages

```python
# Deliver text message
msg = await client.deliver(chat_id=12345, text="Hello!")

# Deliver photo message
photo_msg = await client.deliver_image(chat_id=12345, file="image.jpg", caption="My photo")
```

## Modifying Messages

```python
# Edit message text
await client.edit(chat_id=12345, message_id=msg.id, text="Updated text!")

# Delete messages
await client.delete(chat_id=12345, message_ids=[msg.id])
```

## Relaying & Copying Messages

```python
# Forward message
await client.forward(chat_id=99999, from_chat_id=12345, message_ids=[msg.id])

# Copy message (without forward header)
await client.copy(chat_id=99999, from_chat_id=12345, message_ids=[msg.id])
```
