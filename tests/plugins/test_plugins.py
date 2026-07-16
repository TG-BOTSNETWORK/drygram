# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import os
import shutil
from drygram.dispatch.dispatcher import Dispatcher
from drygram.plugins.loader import PluginLoader

def test_plugin_loader():
    disp = Dispatcher()
    loader = PluginLoader(disp)
    
    os.makedirs("test_plugins_dir", exist_ok=True)
    plugin_file = "test_plugins_dir/my_test_plugin.py"
    with open(plugin_file, "w") as f:
        f.write('''# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
def setup(dispatcher):
    pass
''')
    
    loader.discover("test_plugins_dir")
    assert "my_test_plugin" in loader.loaded_plugins
    
    loader.unload_plugin("my_test_plugin")
    assert "my_test_plugin" not in loader.loaded_plugins
    
    if os.path.exists("test_plugins_dir"):
        shutil.rmtree("test_plugins_dir")
