# Listeners (Watchers)

Watchers bind gates and callbacks.

```python
from drygram import Watcher
watcher = Watcher(callback=my_callback, gate=Gates.private())
client.dispatcher.add_watcher(watcher)
```
