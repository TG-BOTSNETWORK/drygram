# Telegram Business Accounts

DryGram provides complete wrapper APIs and observers for managing business account integrations, automated away responses, greeting messages, and quick business links.

## Business Connections

When a client operates as an authorized business bot or user:

### Fetch Business Profile
```python
profile = await client.business_profile()
print(f"Business Profile Info: {profile['description']}")
```

### Config Away Reply Messages
```python
# Set custom away reply trigger and message
await client.set_business_away("Currently unavailable. I will get back to you soon.")
```

### Config Greeting Messages
```python
# Set automated greeting message for new chats
await client.set_business_greeting("Welcome to our official business support!")
```

## Observing Business Messages

You can track and handle messages sent to the business account using Gates and listeners:

```python
from drygram import Gates, Message

@app.observe(Gates.private())
async def business_incoming_message(msg: Message):
    # Track business chat updates
    print(f"Business message received: {msg.text}")
```
