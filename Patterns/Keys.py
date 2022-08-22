"""
    Encryption examples
"""

from cryptography.fernet import Fernet
import os

#
def main():
    key = ""
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        print(f"key = {key}")

        with open("key.key", "wb") as keyfile:
            keyfile.write(key)

        with open("key.key", "rb") as keyfile:
            key2 = keyfile.read()

        if key == key2:
            print("They match!")
    else:
        with open("key.key", "rb") as keyfile:
            key2 = keyfile.read()

    key3 = os.environ.get("KEY")
    if key3:
        bkey3 = key3.encode("utf-8")
        if key2 == bkey3:
            print("Filekey and os key match!")
    else:
        print("KEY is not in the environment!")

    f = Fernet(key3)
    token = f.encrypt(b"my deep dark secret")
    print(token)
    decrypted = f.decrypt(token)
    print(decrypted)


if __name__ == "__main__":
    main()
