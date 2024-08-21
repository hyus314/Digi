from cryptography.fernet import Fernet
import base64

from main.settings import cipher_suite
# alabala
# Generate a key for encryption/decryption (this should be kept secure)

# Function to encrypt data
def encrypt_data(data):
    if not isinstance(data, str):
        encrypted_data = cipher_suite.encrypt(str(data).encode('utf-8'))
        test = str(encrypted_data)
    else:
        ValueError("Id is in wrong format.")
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    return int(decrypted_data)

def encrypt_msg(data):
    if isinstance(data, int):
        data = str(data)
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def decrypt_msg(encrypted_data):
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return int(decrypted_data)