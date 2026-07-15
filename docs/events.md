# Event Pipeline

Updates are propagated via the Event Pipeline.

```python
@client.observe()
async def signal_receiver(event):
    print("Received event:", event)
```
