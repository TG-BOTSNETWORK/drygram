# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Any
from drygram.dispatch.dispatcher import Dispatcher
from drygram.dispatch.watcher import Watcher

class PluginLoader:
    """
    Dynamic plugin module autoloader and hot-reloader.

    Parameters
    ----------
    dispatcher : Dispatcher
        Active dispatcher instance to hook handlers to.

    Attributes
    ----------
    dispatcher : Dispatcher
        Active dispatcher reference.
    loaded_plugins : Dict[str, Any]
        Dictionary mapping plugin module names to path and module references.
    registered_watchers : Dict[str, List[Watcher]]
        Dictionary mapping plugin module names to registered Watchers.
    """

    def __init__(self, dispatcher: Dispatcher):
        """Initialize the PluginLoader."""
        self.dispatcher = dispatcher
        self.loaded_plugins: Dict[str, Any] = {}
        self.registered_watchers: Dict[str, List[Watcher]] = {}

    def load_plugin(self, file_path: str) -> None:
        """
        Load a plugin module from source.

        Parameters
        ----------
        file_path : str
            Full path to the Python source file.
        """
        if not file_path.endswith(".py"):
            return
        
        module_name = os.path.basename(file_path)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            return
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        pre_watchers = []
        for group in self.dispatcher.watchers.values():
            pre_watchers.extend(list(group))
        
        spec.loader.exec_module(module)
        
        post_watchers = []
        for group in self.dispatcher.watchers.values():
            post_watchers.extend(list(group))
            
        added_watchers = [w for w in post_watchers if w not in pre_watchers]
        
        if hasattr(module, "setup"):
            module.setup(self.dispatcher)
            
            post_setup_watchers = []
            for group in self.dispatcher.watchers.values():
                post_setup_watchers.extend(list(group))
            added_watchers.extend([w for w in post_setup_watchers if w not in post_watchers])
            
        self.loaded_plugins[module_name] = (file_path, module)
        self.registered_watchers[module_name] = added_watchers

    def unload_plugin(self, module_name: str) -> None:
        """
        Unload a plugin module and remove its handlers.

        Parameters
        ----------
        module_name : str
            Module name of the loaded plugin.
        """
        if module_name not in self.loaded_plugins:
            return
        
        watchers = self.registered_watchers.get(module_name, [])
        for watcher in watchers:
            self.dispatcher.remove_watcher(watcher)
            
        if module_name in sys.modules:
            del sys.modules[module_name]
            
        del self.loaded_plugins[module_name]
        del self.registered_watchers[module_name]

    def reload_plugin(self, module_name: str) -> None:
        """
        Reload a loaded plugin module.

        Parameters
        ----------
        module_name : str
            Module name of the loaded plugin.
        """
        if module_name not in self.loaded_plugins:
            return
        
        file_path, _ = self.loaded_plugins[module_name]
        self.unload_plugin(module_name)
        self.load_plugin(file_path)

    def discover(self, directory: str) -> None:
        """
        Search directory and load all valid python plugins.

        Parameters
        ----------
        directory : str
            Target search directory.
        """
        if not os.path.exists(directory):
            return
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    self.load_plugin(os.path.join(root, file))
