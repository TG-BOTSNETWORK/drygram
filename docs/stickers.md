# Stickers

DryGram supports fetching installed sticker sets, adding sticker sets, and managing favorite and recent stickers.

## Query Sticker Sets

To get a list of active sticker sets installed on the account:

```python
sets = await client.sticker_sets()
for s in sets:
    print(f"Sticker Set Title: {s['title']} | Name: {s['name']}")
```

## Favorite Stickers

Query your favorite stickers metadata:

```python
favorites = await client.favorite_stickers()
for sticker in favorites:
    print(f"Favorite Sticker ID: {sticker['file_id']}")
```
