""" Key storage implementations """
from pathlib import Path
from typing import Any

from key_factories import KeyStorage, register

@register
class KeyFileStorage(KeyStorage):
    """ Store a key in the file """

    def __init__(self, filename:Path = Path("key.key")) -> None:
        self.filename = filename

    @property
    def key (self)->Any:
        """
        key Retrieve the key from the file

        Raises:
            FileNotFoundError: If the file does not exist

        Returns:
            Any: the contents of the file as the key
        """
        if not Path.exists( self.filename):
            raise FileNotFoundError

        with open(self.filename, "rb") as keyfile:
            key = keyfile.read()
        return key

    @key.setter
    def key (self, value: Any):
        """
        key Setter - saves the key to the file

        Args:
            value (Any): value of the key to save
        """
        with open(self.filename, "wb") as keyfile:
            keyfile.write(str(value).encode("utf-8"))
