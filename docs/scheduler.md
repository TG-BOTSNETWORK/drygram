# Task Scheduler

DryGram includes a built-in asynchronous task scheduler to trigger deferred actions.

## Scheduling Tasks

```python
from drygram import DryClient
import asyncio

app = DryClient("session", api_id=123, api_hash="abc")

async def timed_job():
    print("Executing scheduled task.")

# Schedule job to run after 10 seconds
app.dispatcher.scheduler.add_task(timed_job, delay=10)
```
