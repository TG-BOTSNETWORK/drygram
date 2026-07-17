# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from cryptography.hazmat.primitives.ciphers import Cipher as CryptoCipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_ige(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypt data using AES-IGE mode via python-cryptography library."""
    if len(data) % 16 != 0:
        raise ValueError("Data length must be a multiple of 16")
    backend = default_backend()
    cipher = CryptoCipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    c_prev = iv[:16]
    p_prev = iv[16:]
    result = bytearray(len(data))
    for i in range(0, len(data), 16):
        p_i = data[i:i+16]
        x = bytes(a ^ b for a, b in zip(p_i, c_prev))
        c_i = encryptor.update(x)
        c_i_xor = bytes(a ^ b for a, b in zip(c_i, p_prev))
        result[i:i+16] = c_i_xor
        c_prev = c_i_xor
        p_prev = p_i
    return bytes(result)

def decrypt_ige(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt data using AES-IGE mode via python-cryptography library."""
    if len(data) % 16 != 0:
        raise ValueError("Data length must be a multiple of 16")
    backend = default_backend()
    cipher = CryptoCipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    c_prev = iv[:16]
    p_prev = iv[16:]
    result = bytearray(len(data))
    for i in range(0, len(data), 16):
        c_i = data[i:i+16]
        x = bytes(a ^ b for a, b in zip(c_i, p_prev))
        p_i = decryptor.update(x)
        p_i_xor = bytes(a ^ b for a, b in zip(p_i, c_prev))
        result[i:i+16] = p_i_xor
        p_prev = p_i_xor
        c_prev = c_i
    return bytes(result)
