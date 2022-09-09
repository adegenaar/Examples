"""
    use the rsa routines inside the cryptography library
"""
import os
from typing import Any

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, padding


def generate_rsa_key(filename:str="privatekey.pem")->rsa.RSAPrivateKey:
    """Generate RSA key

    Args:
        filename (str): filename for the RSA key
    """
    # Generate our key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    return key


def write_private_key(key, filename:str="privatekey.pem")->None:
    """write our private key to the disk for safe keeping

    Args:
        filename (str, optional): name of the keyfile. Defaults to "privatekey.pem".
    """
    # Write our key to disk for safe keeping
    with open(filename, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(os.environ["PASS_PHRASE"].encode()),
        ))


def read_private_key(filename:str="privatekey.pem")->rsa.RSAPrivateKey | dsa.DSAPrivateKey :
    """load the private key from the disk

    Args:
        filename (str, optional): filename for the private key. Defaults to "privatekey.pem".
    """
    password = os.environ["PASS_PHRASE"].encode('utf-8')
    with open("privatekey.pem", "rb") as f:
        key1 = serialization.load_pem_private_key(f.read(), password=password)

    return key1


def sign_with_rsa_key(key:rsa.RSAPrivateKey, message:str)->Any:
    key.sign(message.encode('utf-8'),   
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()   
    )


def sign_with_dsa_key(key:dsa.DSAPrivateKey, message:str)->Any:
    return key.sign(message.encode('utf-8'),   
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()   
    )
    

def verify(private_key):
    public_key = private_key.public_key()
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )    


message = "This is my super important message that needs to be signed"

key1 = generate_rsa_key()
write_private_key(key1)

key2 = read_private_key()

if isinstance(key2,rsa.RSAPrivateKey):
    signature = sign_with_rsa_key(key2, message)
elif isinstance(key2,dsa.DSAPrivateKey):
    signature = sign_with_dsa_key(key2, message)

public_key = key1.public_key()
encrypted_message = public_key.encrypt(
    message.encode('utf-8'),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(encrypted_message)

plaintext = key2.decrypt(
    encrypted_message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(plaintext.decode())