# Event Pipeline & Middlewares

DryGram implements an advanced asynchronous event routing pipeline. When updates arrive from the Telegram MTProto servers, they are fed into the client dispatcher, passed through the middleware pipeline, and routed to matching observers.

## Middleware Pipeline

Middlewares intercept incoming signals (such as `Message` or `Update`) before they reach observers. Middlewares can log events, apply rate limiting, perform authentication checks, or abort processing.

A middleware is an asynchronous callable that takes a `Signal` and a `next_handler` callback:

```python
import time
from drygram import DryClient, Message

app = DryClient("my_app", api_id=123, api_hash="abc")

# Registering a latency logging middleware
@app.middleware()
async def latency_tracker(msg: Message, next_handler):
    start = time.perf_counter()
    
    # Pass control to the next middleware or event observer
    result = await next_handler(msg)
    
    duration = time.perf_counter() - start
    print(f"Signal processed in {duration:.4f}s")
    return result
```

## Update Observers

Register handler observers using the `@app.observe` decorator. Handlers only receive events that match the supplied `Gate` filters:

```python
from drygram import Gates, Message

# Handle only text messages in private chats
@app.observe(Gates.private() & Gates.text())
async def private_text_handler(msg: Message):
    print(f"Received: {msg.text}")
```

## Priority Worker Pools

The dispatcher delegates handler execution to an internal task queue backed by configurable priority worker pools. This prevents slow network calls in one handler from blocking the ingestion of other incoming events.
