"""
    Encryption utilities
"""
import os
from os import path
#from os.path import exists
from typing import Protocol, ByteString

from cryptography.fernet import Fernet


class Crypt (Protocol):

    def encrypt(self, data:str)->str:
        ...

    def decrypt(self, encrypted_data:str)->str:
        ...

class FernetCrypt (Crypt):
    """
    FernetCrypt Fernet implementation of the encryption

    Args:
        Crypt ([type]): [description]
    """
    def __init__(self, filename=None, keyname=None) -> None:
        super().__init__()
        self.filename = filename
        self.keyname = keyname
        self._key = None

    @property
    def key(self)->ByteString:
        """
        Lazy retrieval of the key.

        Raises:
            FileNotFoundError: if a filename was specified for the key file and file doesn't exist

        Returns:
            ByteString: key
        """
        if not self._key:
            if self.keyname and os.environ[self.keyname]:
                self.key = os.environ[self.keyname]
            if self.filename:
                if not os.path.exists(self.filename):
                    raise FileNotFoundError
                with open(self.filename, "rb") as keyfile:
                    self.key = keyfile.read()
        return self._key

    @key.setter
    def key(self, value:ByteString):
        """
        key Setter for the key

        Args:
            value (ByteString): value for the key
        """
        self._key = value

    @key.deleter
    def key(self):
        del self._key

    def encrypt(self, data:str)->str:
        """
        encrypt Encrypt the string

        Args:
            data (str): data to be encrypted

        Returns:
            str: the encrypted data
        """
        encoder = Fernet(self.key)
        # encrypt data
        encrypted_data = encoder.encrypt(data)
        return encrypted_data

    def encrypt_file(self, filename:path):
        """
        Encrypt the contents of the given file

        Args:
            filename (Path): path to the file to encrypt

        Raises:
            FileNotFoundError: check for the existence of the file
        """
        if not os.path.exists(filename):
            raise FileNotFoundError

        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()

        encrypted_data = self.encrypt(file_data)

        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    def decrypt(self, encrypted_data: str)->str:
        """
        Decrypt the encrypted data
        """
        decoder = Fernet(self.key)

        # decrypt data
        decrypted_data = decoder.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')

    def decrypt_file(self, filename: path):
        """
        decrypts the file and write it back to the same file
        """
        if not os.path.exists(filename):
            raise FileNotFoundError

        with open(filename, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        decrypted_data = self.decrypt(encrypted_data)
        # write the original file
        with open(filename, "wb") as file:
            file.write(decrypted_data)

    def write_key(self):
        """
        Generates a key and save it into a file
        """
        key = self.key
        if not key:
            key = Fernet.generate_key()

        with open(self.filename, "wb") as key_file:
            key_file.write(key)
        self.key = key


def main():
    #f = FernetCrypt (filename = "key.key")
    f = FernetCrypt (keyname = "KEY")

    message = "some secret message".encode()

    encrypted = f.encrypt(message)
    print(encrypted)

    decrypted = f.decrypt(encrypted)
    print(decrypted)


if __name__ == "__main__":
    main()


# 1. Generate a key
# 2. Add your key to your environment
#   Move your key, for example, to mv key.key /home/my_user/keys/myproject.key
#   then, store the key in a environment variable with:
#   export PYMS_KEY_FILE=/home/my_user/keys/myproject.key
# 3. Encrypt your information and store it in config
# 4. Decrypt from your config file
#   use a prefix (such as enc_ or ENC_) to mark a key that needs to be encrypted/decrypted
