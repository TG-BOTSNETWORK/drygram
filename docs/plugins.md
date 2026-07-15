# Plugin Loader

Hot-reload plugin architecture.

```python
from drygram.plugins.loader import PluginLoader
loader = PluginLoader(app.dispatcher)
loader.discover("my_plugins")
```
