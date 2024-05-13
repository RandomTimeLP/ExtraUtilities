from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# RSA Schlüsselpaar generieren
def generiere_rsa_schluesselpaar():
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pub_key = priv_key.public_key()
    return (priv_key, pub_key)

# Nachricht mit dem öffentlichen Schlüssel verschlüsseln
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

def serialize_key(key):
    return key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

def deserialize_key(key):
    pub_key = load_pem_public_key(
        key.encode('utf-8'),
        backend=default_backend()
    )
    return pub_key


# Nachricht mit dem privaten Schlüssel entschlüsseln
def decrypt(message, priv_key):
    entschluesselte_nachricht = priv_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return entschluesselte_nachricht.decode()

# Beispiel
priv_key, pub_key = generiere_rsa_schluesselpaar()
message = verschluesseln("Geheime Nachricht", pub_key)
print(f"Verschlüsselt: {message}")

entschluesselte_nachricht = decrypt(message, priv_key)
print(f"Entschlüsselt: {entschluesselte_nachricht}")