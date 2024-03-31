from cryptography.fernet import Fernet

# Generate a key for encryption/decryption (this should be kept secure)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt data
def encrypt_data(data):
    # Convert integer to bytes
    data_bytes = data.to_bytes((data.bit_length() + 7) // 8, 'big')
    encrypted_data = cipher_suite.encrypt(data_bytes)
    return encrypted_data

# Function to decrypt data to integer
def decrypt_data(encrypted_data):
    decrypted_data_bytes = cipher_suite.decrypt(encrypted_data)
    decrypted_int = int.from_bytes(decrypted_data_bytes, 'big')
    return decrypted_int