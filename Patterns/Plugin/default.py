""" Define our default class """

from plugin import PluginBase


class Plugin(PluginBase):
    """Example Plugin Object"""

    def process(self, num1, num2):
        """Some prints to identify which plugin is been used"""
        print("This is my default plugin")
        print(f"Numbers are {num1} and {num2}")
