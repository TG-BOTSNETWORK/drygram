# Telegram Stories

DryGram supports publishing profile stories, deleting stories, checking viewer statistics, and reacting to stories.

## Publishing Stories

You can publish stories containing photo or video media attachments:

```python
story = await client.publish_story(
    media="path/to/story_image.jpg",
    caption="My morning story!"
)
print(f"Published story ID: {story.id}")
```

## Story Viewer Statistics

To retrieve the viewers list and view times of an active story:

```python
viewers = await client.story_viewers(story_id=123)
for viewer in viewers:
    print(f"User ID: {viewer['user_id']} | Viewed at: {viewer['viewed_at']}")
```

## Story Reactions

To retrieve reactions on a story:

```python
reactions = await client.story_reactions(story_id=123)
for reaction in reactions:
    print(f"Reaction Emoji: {reaction['emoji']} | Count: {reaction['count']}")
```
