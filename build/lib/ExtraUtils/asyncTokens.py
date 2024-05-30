from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def gen_keypair():
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pub_key = priv_key.public_key()
    return (priv_key, pub_key)

def encrypt(nachricht, pub_key):
    message = pub_key.encrypt(
        nachricht.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return message

def serial(key):
    try:
        return key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    except AttributeError:
        return key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

def load_private(key):
    priv_key = serialization.load_pem_private_key(
        key.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    return priv_key

def load(key):
    pub_key = load_pem_public_key(
        key.encode('utf-8'),
        backend=default_backend()
    )
    return pub_key

def sign(message, priv_key):
    signature = priv_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify(message, signature, pub_key):
    try:
        pub_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

def decrypt(message, priv_key):
    decrypted_message = priv_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

# Example:
# priv_key, pub_key = generiere_rsa_schluesselpaar()
# message = encrypt("Geheime Nachricht", pub_key)
# print(f"Verschlüsselt: {message}")
# 
# decrypted_message = decrypt(message, priv_key)
# print(f"Entschlüsselt: {decrypted_message}")