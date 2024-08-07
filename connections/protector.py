from cryptography.fernet import Fernet
import base64

from main.settings import cipher_suite
# alabala
# Generate a key for encryption/decryption (this should be kept secure)

# Function to encrypt data
def encrypt_data(data):
    if isinstance(data, int):
        # Convert integer to bytes
        data_bytes = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    else:
        # Convert string to bytes
        data_bytes = data.encode('utf-8')
    
    # Encrypt the bytes
    encrypted_data = cipher_suite.encrypt(data_bytes)
    return encrypted_data

def decrypt_data(encrypted_data):
    # Decrypt the bytes
    decrypted_data_bytes = cipher_suite.decrypt(encrypted_data)
    
    try:
        # Attempt to decode to string
        decrypted_data = decrypted_data_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Fallback to int
        decrypted_data = int.from_bytes(decrypted_data_bytes, 'big')
    
    return decrypted_data

def encrypt_and_truncate(room_name, max_length=95):
    # Encrypt the data
    encrypted = encrypt_data(room_name)
    
    # Truncate the encrypted data to ensure it's less than max_length bytes
    truncated_encrypted = encrypted[:max_length]
    
    return truncated_encrypted

def decrypt_truncated_data(truncated_encrypted_data):
    # Directly decrypt the truncated encrypted data
    decrypted_data = decrypt_data(truncated_encrypted_data)
    
    return decrypted_data