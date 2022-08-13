""" base factories """

from typing import Type,Any
from abc import ABC,abstractmethod

def register(cls):
    """ decorator to register a type """
    cls.register(cls)
    return cls

#from protocols import KeyGenerator, KeyStorage
class KeyGenerator(ABC):
    """Basic representation of a key generator."""
    implementations = {}

    @abstractmethod
    def generate(self, *args, **kwargs) -> Any:
        """Creates a new key"""
        raise NotImplementedError

    @classmethod
    def register(cls, typename:Type)->None:
        """ register the class as a key generator """
        cls.implementations[typename.__name__] = typename

    @classmethod
    def is_registered(cls, typename:Type):
        """ check to see if the cls has already been implemented """
        return typename in cls.implementations

class KeyStorage(ABC):
    """ Basic representation of a key storage system """
    implementations = {}

    @property
    def key (self)->Any:
        """ Key getter """
        raise NotImplementedError

    @key.setter
    def key (self, value: Any):
        """ Key setter """
        raise NotImplementedError

    @classmethod
    def register(cls, typename:Type)->None:
        """ register the class as a key generator """
        cls.implementations[typename.__name__] = typename

    @classmethod
    def is_registered(cls, typename:Type):
        """ check if the class is registered """
        return typename in cls.implementations


class KeyGeneratorFactory():
    """ base class for key generator factories """
    def get_key_generator(self, typename:str) -> KeyGenerator:
        """Returns a new key storage belonging to this factory."""
        if not KeyGenerator.is_registered(typename):
            raise ValueError
        return KeyGenerator.implementations[typename]


class KeyStorageFactory():
    """ base factory for the Key storage factories """
    def get_key_storage(self, typename:str) -> KeyStorage:
        """Returns a new key storage belonging to this factory."""
        if not KeyStorage.is_registered(typename):
            raise ValueError
        return KeyStorage.implementations[typename]
