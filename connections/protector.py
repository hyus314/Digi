from cryptography.fernet import Fernet
import base64

from main.settings import cipher_suite
# alabala
# Generate a key for encryption/decryption (this should be kept secure)

# Function to encrypt data
def encrypt_data(data):
    if not isinstance(data, str):
        encrypted_data = cipher_suite.encrypt(str(data))
    else:
        ValueError("Id is in wrong format.")
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    return int(decrypted_data)