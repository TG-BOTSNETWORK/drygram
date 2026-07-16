# Installation Guide

This guide details the prerequisites and step-by-step instructions for installing DryGram and setting up its optional database backends.

## Prerequisites

- **Python**: Version 3.13 or newer is required.
- **Operating System**: Linux (Ubuntu, Debian, CentOS), macOS (11+), or Windows (10, 11, Server).
- **Core Dependencies**:
  - `cryptography>=42.0.0` (for AES session encryption and MTProto transport encryption)
  - `aiosqlite>=0.20.0` (default SQLite session engine)

## Package Installation

To install DryGram via pip:

```bash
pip install drygram
```

To install from source (editable mode for developers):

```bash
git clone https://github.com/TG-BOTSNETWORK/drygram.git
cd DryGram
pip install -e .
```

## Setting up Backend Databases

Depending on your scaling needs, install the driver package matching your desired session storage backend:

### Redis Session Backend
Requires the `redis` client package:
```bash
pip install redis>=5.0.0
```

### MongoDB Session Backend
Requires the `motor` asynchronous MongoDB driver:
```bash
pip install motor>=3.3.0
```

### PostgreSQL Session Backend
Requires the `asyncpg` asynchronous PostgreSQL driver:
```bash
pip install asyncpg>=0.29.0
```

## Verifying the Installation

After installing, confirm that the drygram package initializes correctly and lists the correct layer compatibility:

```bash
python -c "import drygram; print(drygram.VERSION)"
```
