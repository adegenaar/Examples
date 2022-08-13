""" Classes that create various encryption keys """
import base64
import os
from typing import ByteString

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


from key_factories import KeyGenerator, register

@register
class FernetKeyGenerator(KeyGenerator):
    """Generate a key using the cryptography.fernet object."""

    def generate(self, *args, **kwargs)->ByteString:
        """ Generate a Fernet key """
        return Fernet.generate_key()

@register
class FernetSaltedKeyGenerator(KeyGenerator):
    """Generate a key using the cryptography.fernet object."""

    def generate(self,*args, **kwargs)->str:
        """
        generate a key starting with a password and a salt value

        Args:
            password (ByteString): Password to use as the basis of the encryption key
            salt (int): salt value used to generate the encryption key

        Returns:
            Any: the Fernet key
        """
        password:str = None
        salt:int = os.urandom(16)

        if "password" in kwargs:
            password:ByteString = kwargs["password"].encode("utf-8")
        if "salt" in kwargs:
            salt:int = kwargs["salt"]

        if len(args) == 2:
            password:ByteString = args[0].encode("utf-8")
            salt:int = args[1]

        if len(args) == 1:
            password:ByteString = args[0].encode("utf-8")

        if not password:
            raise ValueError("A password must be supplied")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        return key
