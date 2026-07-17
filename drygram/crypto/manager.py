# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import cryptography
from drygram.crypto.python_backend import encrypt_ige, decrypt_ige

_backend_name = "cryptography"
_backend_version = getattr(cryptography, "__version__", "unknown")
_supports_acceleration = False
_is_accelerated = False

def current_backend() -> str:
    """Return the name of the currently active cryptographic backend."""
    return _backend_name

def supports_acceleration() -> bool:
    """Return whether cryptographic acceleration is supported on the system."""
    return _supports_acceleration

def is_accelerated() -> bool:
    """Return whether the currently active backend is accelerated."""
    return _is_accelerated

encrypt_ige = encrypt_ige
decrypt_ige = decrypt_ige
backend_name = _backend_name
backend_version = _backend_version
