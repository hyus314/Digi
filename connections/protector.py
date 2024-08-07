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

def encrypt_and_encode(room_name):
    # Encrypt the data
    encrypted = encrypt_data(room_name)
    
    # Encode the encrypted data to base64
    encoded = base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    # Truncate to ensure it's less than 100 characters
    return encoded[:95]

def decode_and_decrypt(encoded_data):
    # Add padding if necessary
    missing_padding = len(encoded_data) % 4
    if missing_padding:
        encoded_data += '=' * (4 - missing_padding)
    
    # Decode the base64 encoded data
    encrypted_data = base64.urlsafe_b64decode(encoded_data)
    
    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data)
    
    return decrypted_data
