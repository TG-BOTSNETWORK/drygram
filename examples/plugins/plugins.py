# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import os
from drygram import DryClient
from drygram.plugins.loader import PluginLoader

app = DryClient("plugins_session", api_id=12345, api_hash="abcdef")

async def main():
    await app.start()
    loader = PluginLoader(app.dispatcher)
    os.makedirs("my_plugins", exist_ok=True)
    with open("my_plugins/hello_plugin.py", "w") as f:
        f.write('''# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
from drygram import Gates, Message
def setup(dispatcher):
    @dispatcher.register_watcher(Gates.text("hi"))
    async def greet(msg: Message):
        pass
''')
    loader.discover("my_plugins")
    print(f"Loaded plugins: {list(loader.loaded_plugins.keys())}")
    loader.reload_plugin("hello_plugin")
    loader.unload_plugin("hello_plugin")
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
