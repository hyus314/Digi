from cryptography.fernet import Fernet
import base64

from main.settings import cipher_suite

# Generate a key for encryption/decryption (this should be kept secure)
cipher_suite = cipher_suite

# Function to encrypt data
def encrypt_data(data):
    if isinstance(data, int):
        # Convert integer to bytes
        data_bytes = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    else:
        # Convert string to bytes
        data_bytes = data.encode()
    encrypted_data = cipher_suite.encrypt(data_bytes)
    return encrypted_data

# Function to decrypt data to string
def decrypt_data(encrypted_data):
    decrypted_data_bytes = cipher_suite.decrypt(encrypted_data)
    try:
        decrypted_data = decrypted_data_bytes.decode()  # Attempt to decode to string
    except UnicodeDecodeError:
        decrypted_data = int.from_bytes(decrypted_data_bytes, 'big')  # Fallback to int
    return decrypted_data

def encrypt_and_encode(room_name):
    encrypted = encrypt_data(room_name)
    encoded = base64.urlsafe_b64encode(encrypted).decode('utf-8')
    return encoded[:95]  # Truncate to ensure it's less than 100 characters
