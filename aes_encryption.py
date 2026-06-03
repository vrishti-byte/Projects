from cryptography.fernet import Fernet


def generate_aes_key():
    return Fernet.generate_key()


def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted = cipher.encrypt(data)
    return encrypted


def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_data)
    return decrypted