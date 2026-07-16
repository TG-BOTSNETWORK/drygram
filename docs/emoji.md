# Custom Emojis

DryGram supports querying custom animated and static emoji sets, setting profile status emoji, and using custom emoji in messages.

## Custom Emoji Sets

To fetch a list of custom emoji sets:

```python
emoji_packs = await client.emoji_sets()
for pack in emoji_packs:
    print(f"Pack Name: {pack['pack_name']}")
```

## Profile Emoji Status

Set custom emoji status (requires Premium):

```python
from drygram.types.premium import PremiumEmojiStatus

status = PremiumEmojiStatus(custom_emoji_id=123456789)
await client.update_profile(emoji_status=status)
```
