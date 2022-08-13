from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self):
        print("Plugin constructor")

    @abstractmethod
    def register(self):
        print("register")


class SamplePlugin(Plugin):
    def register(self):
        print("register")
