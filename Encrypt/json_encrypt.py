"""
    JSON encoder and decoder to encrypt and decrypt json files
"""
import datetime
import json
from os.path import exists
import os
from typing import Any, Callable

from cryptography.fernet import Fernet
from dateutil import parser


class EncryptedEncoder(json.JSONEncoder):
    """
    EncryptedEncoder Encrypt values for keys with the "enc_" prefix" or "

    Args:
        json (JSONEncoder): Super class for the Encoder
    """

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def __init__(
        self,
        *,
        skipkeys: bool = ...,
        ensure_ascii: bool = ...,
        check_circular: bool = ...,
        allow_nan: bool = ...,
        sort_keys: bool = ...,
        indent: int | None = ...,
        separators: tuple[str, str] | None = ...,
        default: Callable[..., Any] | None = ...
    ) -> None:
        super().__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
        )
        # see if we have a key file
        if exists("key.key"):
            with open("key.key", "rb") as keyfile:
                key = keyfile.read()
        elif os.environ("KEY"):
            key = os.environ("KEY")

        self.fernet = Fernet(key)

    def encode(self, o: Any) -> str:
        """
        encode If a key has a "enc_" prefix, encrypt the value

        Args:
            o (Any): JSON element

        Returns:
            str: Encoded json string
        """
        # allow any custom decoders to do their job...
        o = json.loads(super().encode(o))

        # Encode the value for keys that start with "enc_"
        for key in o.keys():
            if key.lower().startswith("enc_"):
                b = self.fernet.encrypt(o[key].encode())
                o[key] = b.decode("utf-8")

        return super().encode(o)

    def default(self, o):
        """
        default Handles the encoding of the unknown "datetime" type

        Args:
            o (JSON): A datetime object to be encoded

        Returns:
            str: JSON Element
        """
        if isinstance(o, datetime.datetime):
            # from the original sample to encode and decode datetime objects
            return {
                "_type": "datetime",
                "value": o.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT)),
            }
        return super().default(o)


class EncryptedDecoder(json.JSONDecoder):
    """
    Decrypt any keys that start with "enc_"

    Args:
        json (json.JSONDecoder): Super class for the decoder
    """

    def __init__(self, *args, **kwargs):
        """
        __init__ auto attach the decoder
        """
        # see if we have a key file
        if exists("key.key"):
            with open("key.key", "rb") as keyfile:
                key = keyfile.read()
        elif os.environ("KEY"):
            key = os.environ("KEY")

        self.fernet = Fernet(key)
        json.JSONDecoder.__init__(self, object_hook=self.decrypt_object_hook, *args, **kwargs)

    def decrypt_object_hook(self, obj):
        """
        decrypt_object_hook Object hook to decrypt the value of the key

        Args:
            obj ([type]): JSON element to be decoded

        Returns:
            [type]: the JSON Element
        """
        for key in obj.keys():
            if key.lower().startswith("enc_"):
                b = self.fernet.decrypt(obj[key].encode())
                obj[key] = b.decode("utf-8")

        # from the original sample to encode and decode datetime objects
        if "_type" not in obj:
            return obj
        thetype = obj["_type"]
        if thetype == "datetime":
            return parser.parse(obj["value"])
        return obj


def main():

    data = {
        "name": "Silent Bob",
        "enc_password": "my secrets",
        "dt": datetime.datetime(2013, 11, 11, 10, 40, 32),
    }

    s = json.dumps(data, cls=EncryptedEncoder, indent=4)
    #     {
    #       "name": "Silent Bob",
    #       "enc_password": "gAAAAABh7c4gWooW8XL-ku1ClWAA2VIzbpO99EzM3ug-kyDbSDMERj27H1Jz0-oJNL_dkKgLtNkm78WsnMGDLyLUQyzKujl60g==",
    #       "dt": {
    #         "_type": "datetime",
    #         "value": "2013-11-11 10:40:32"
    #       }
    #     }
    print(s)
    print(json.loads(s, cls=EncryptedDecoder))


if __name__ == "__main__":
    main()
