# Telegram Premium & Stars

DryGram supports checking premium accounts, querying custom premium stickers/emojis, and interacting with Telegram Stars.

## Telegram Stars API

Stars are the virtual currency on Telegram used to buy digital products, pay channel creators, and purchase gifts.

### Checking Stars Balance
```python
balance = await client.stars_balance()
print(f"Current Stars Balance: {balance}")
```

### Sending Stars
```python
# Send 50 Stars to a user
success = await client.send_stars(user_id=123456, stars=50)
```

## Profile Gifts

You can query the catalog of available gifts and send them to other users:

### Query Gift Catalog
```python
gifts = await client.gift_catalog()
for gift in gifts:
    print(f"Gift ID: {gift['gift_id']} | Stars Price: {gift['stars_price']}")
```

### Sending a Gift
```python
# Send gift with ID 1 to a user
success = await client.send_gift(user_id=123456, gift_id=1)
```
