"""
KeyRing sample

for more information see https://pypi.org/project/keyring/
"""
import sys
from argparse import ArgumentParser, Namespace

import keyring
from cryptography.fernet import Fernet


def parse_args() -> Namespace:
    """
    Argument parsing routines
    """
    parser = ArgumentParser(
        description="Keyring sample program",
    )
    parser.add_argument("-s", "--set", nargs=2, help="--set <system> <secret>")
    parser.add_argument("-g", "--get", nargs=2, help="--get <system> <secret>")
    parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag
    args: Namespace = parser.parse_args()

    return args


def encrypt_file(key: bytes, content: str, tokenfile="SecToken.Bin") -> None:
    """encrypt file

    Args:
        key (str): encryption key
        content (str): content of the file to encrypt
        tokenfile (str, optional): Path/filename of the encrypted token. Defaults to "SecToken.Bin".
    """
    cipher_suite = Fernet(key)
    ciphered_text1: bytes = cipher_suite.encrypt((content).encode())

    with open(tokenfile, "wb") as file_object:
        file_object.write(ciphered_text1)  # writing encrypted token to file


def decrypt_file(key: bytes, tokenfile="SecToken.Bin") -> str | None:
    """decrypt file

    Args:
        key (str): encryption key
        tokenfile (str, optional): Path/filename of the encrypted token. Defaults to "SecToken.Bin".

    Returns:
        str | None: content of the decrypted file
    """
    cipher_suite = Fernet(key)

    with open(tokenfile, "rb") as file_object:
        for line in file_object:
            encryptedpwd: bytes = line
            uncipher_text: bytes = cipher_suite.decrypt(encryptedpwd)
            u_token: str = bytes(uncipher_text).decode("utf-8")  # convert to string
            return u_token
    return None


def main() -> int:
    """main entry point

    Returns:
        int: return value
    """
    args: Namespace = parse_args()

    if args.verbose:
        pass

    if args.set:
        system: str = args.set[0]
        user: str = args.set[1]
        # secret: str | None = getpass.getpass(prompt="Secret: ")
        secret: str | None = keyring.get_password(system, user)
        if secret is None:
            secret = Fernet.generate_key().decode()
            keyring.set_password(system, user, secret)

        encrypt_file(secret.encode(), "super secret content")

    if args.get:
        system: str = args.get[0]
        user: str = args.get[1]
        secret: str | None = keyring.get_password(system, user)
        if secret:
            token = decrypt_file(secret.encode())
            print(f"{token=}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
