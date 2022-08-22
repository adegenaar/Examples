""" base class for the plugins """
from abc import ABC, abstractmethod


class PluginBase(ABC):
    """base class for the application plugins"""

    @abstractmethod
    def process(self, num1, num2):
        """example plugin"""
        raise NotImplementedError
