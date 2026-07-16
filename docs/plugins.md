# Plugin Development Guide

Plugins allow modularizing DryGram applications by separating message handlers, middlewares, and startup actions into discrete submodules.

## Creating a Plugin

Create a Python module directory containing handlers:

`my_plugin.py`:
```python
from drygram import Gates, Message
from drygram.compat import Router

# Initialize a Router instance
plugin_router = Router()

@plugin_router.observe(Gates.private() & Gates.text("hello"))
async def hello_handler(msg: Message):
    await msg.respond("Hello from plugin!")
```

## Registering Plugins

Load and register routers directly on `DryClient`:

```python
from drygram import DryClient
from my_plugin import plugin_router

app = DryClient("session", api_id=123, api_hash="abc")

# Register plugin router
app.add_router(plugin_router)
```
