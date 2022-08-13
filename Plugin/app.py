""" app.py """
import importlib


class Application:
    """We are going to receive a list of plugins as parameter"""

    def __init__(self, plugins: list = None):
        """Checking if plugin were sent"""

        if plugins:
            # create a list of plugins
            self._plugins = [
                # Import the module and initialise it at the same time
                importlib.import_module(plugin, ".").Plugin()
                for plugin in plugins
            ]
        else:
            # If no plugin were set we use our default
            self._plugins = [importlib.import_module("default", ".").Plugin()]
# import inspect
# import importlib

# module = importlib.import_module('dir1.dir2.myfile.py')
# for name, obj in inspect.getmembers(module):
#     if inspect.isclass(module):
#         print(obj.id)   # id is defined in all the classes


    def run(self):
        """run the application"""
        print("Starting my application")
        print("-" * 10)
        print("This is my core system")

        # This is where the magic happens, and all the plugins are going to be called
        for plugin in self._plugins:
            plugin.process(5, 3)

        print("-" * 10)
        print("Ending my application")
        print()
