# Installation Guide

This guide details the prerequisites and step-by-step instructions for installing DryGram, configuring optional dependency extras, and leveraging the built-in Crypto Engine.

---

## Prerequisites

- **Python**: Version 3.13 or newer is required.
- **Operating System**: Linux (Ubuntu, Debian, Fedora, Arch Linux, CentOS, Alpine), macOS (Intel & Apple Silicon), or Windows (10, 11).
- **Core Dependencies**:
  - `cryptography>=42.0.0` (Core python-cryptography provider)
  - `aiosqlite>=0.20.0` (Default session engine)

---

## Installation Options

### 1. Standard Installation
Installs core features only. Does not require a compiler (e.g., MSVC, GCC, Clang, or Rust) to build native binary extensions:
```bash
pip install drygram
```

### 2. Optional Crypto Installation
Installs with the standard `crypto` dependency group (which installs the required `cryptography` package):
```bash
pip install "drygram[crypto]"
```

### 3. Optional Voice & Calling Interoperability
Installs interfaces and integration modules for external voice/video streaming libraries:
```bash
pip install "drygram[calls]"
```

### 4. Pluggable Session Databases
Install drivers for high-performance session databases:
```bash
# MongoDB support
pip install "drygram[mongodb]"

# Redis support
pip install "drygram[redis]"

# PostgreSQL support
pip install "drygram[postgres]"
```

### 5. Developer Tools
Install development, unit testing, and documentation formatting tools:
```bash
pip install "drygram[dev]"
```

---

## Crypto Backend Manager

DryGram features a built-in **Crypto Backend Manager** that exposes details of the active cryptographic engine.

### Cryptography Backend
- **Pure Python**: DryGram operates on a pure-Python cryptography backend backed by the standard `cryptography` package.
- **Compiler-Free**: Installing DryGram requires zero compiler setup, ensuring out-of-the-box compatibility across all major platforms and architectures (including Windows, Linux, macOS, and ARM64).
- **Stable API**: Cryptographic APIs (`Cipher.encrypt_ige`, `Cipher.decrypt_ige`) are exposed consistently.

### Checking Active Backend Status
```python
from drygram.crypto import current_backend, supports_acceleration, is_accelerated

print("Active Backend:", current_backend())         # Outputs "cryptography"
print("Hardware Accelerated:", supports_acceleration()) # Outputs False
print("Is Accelerated:", is_accelerated())          # Outputs False
```
