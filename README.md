<p align="center">
  <img src="assets/logo.png" alt="DryGram Logo" width="280">
</p>

# DryGram

Modern, fully asynchronous, production-ready Telegram MTProto v2.0 client framework built from scratch in Python.

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python Version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPL--3.0-green.svg" alt="License Badge"></a>
  <a href="https://github.com/TG-BOTSNETWORK/drygram/releases"><img src="https://img.shields.io/github/v/release/TG-BOTSNETWORK/drygram" alt="Latest Release"></a>
  <a href="https://pypi.org/project/drygram/"><img src="https://img.shields.io/pypi/dm/drygram" alt="Downloads"></a>
  <a href="https://github.com/TG-BOTSNETWORK/drygram/docs"><img src="https://img.shields.io/badge/Docs-MkDocs-blue.svg" alt="Documentation Badge"></a>
  <a href="https://github.com/TG-BOTSNETWORK/drygram/stargazers"><img src="https://img.shields.io/github/stars/TG-BOTSNETWORK/drygram?style=flat" alt="GitHub Stars"></a>
  <a href="https://github.com/TG-BOTSNETWORK/drygram/issues"><img src="https://img.shields.io/github/issues/TG-BOTSNETWORK/drygram" alt="GitHub Issues"></a>
  <a href="https://github.com/TG-BOTSNETWORK/drygram/actions"><img src="https://img.shields.io/github/actions/workflow/status/TG-BOTSNETWORK/drygram/test.yml" alt="Build Status"></a>
  <a href="https://pypi.org/project/drygram/"><img src="https://img.shields.io/pypi/v/drygram" alt="PyPI Version"></a>
</p>

---

## Introduction

DryGram is a production-grade, highly-optimized, fully asynchronous Telegram MTProto client framework built from scratch in Python 3.13+. It implements the secure MTProto v2.0 protocol and integrates the latest Telegram features natively.

Designed with architectural originality at its core, DryGram does NOT duplicate or copy Pyrogram, Telethon, or other existing wrappers. It features a decoupled structure, pluggable session stores, extensible middleware chains, and a robust update dispatcher system to achieve maximum performance and scalability.

---

## Features

| Feature | Description |
| :--- | :--- |
| **Authentication** | Support for Bot authorization, User authorization, 2FA password verification, and QR Login flows. |
| **Sessions** | Pluggable, highly-concurrent database storage backends: SQLite, MongoDB, Redis, and PostgreSQL. |
| **Stories** | High-level APIs for publishing stories, reacting to them, archiving stories, and adjusting story privacy. |
| **Business** | Full support for Telegram Business greeting/away responses, custom business links, and short reply templates. |
| **Premium** | Operations for Telegram Star payments, upgradeable gifts, collectibles, and custom Premium Emoji Statuses. |
| **Media** | Chunked uploads, high-speed concurrent downloads, and representations for Photos, Videos, Documents, Audios, and VoiceNotes. |
| **Text Formatting** | Built-in, high-speed parsers for Markdown and HTML messages. |
| **Keyboards** | Declarative markup interfaces for Reply and Inline keyboards, callback button handlers, and interactive menus. |
| **Plugin System & Middleware** | Extensible middleware pipelines, priority-based command watchers, and modular update routing. |
| **Raw MTProto & AsyncIO** | Direct invocation of raw TL schema functions via async loops. |

---

## Installation

### Installation Options

#### 1. Standard Installation (No native compilers required)
Install the core package via PyPI:
```bash
pip install drygram
```

#### 2. Optional Crypto Installation
Install with the optional `crypto` dependency group:
```bash
pip install "drygram[crypto]"
```
*Note: Installs the required standard cryptography package without requiring native compilers or Visual Studio Build Tools.*

#### 3. Optional Voice & Calling Support
Install with integrations for voice and video calling:
```bash
pip install "drygram[calls]"
```

#### 4. Optional Database Support
Install pluggable session database stores:
```bash
# MongoDB support
pip install "drygram[mongodb]"

# Redis support
pip install "drygram[redis]"

# PostgreSQL support
pip install "drygram[postgres]"
```

#### 5. Development Installation
Install for library contribution and testing:
```bash
pip install "drygram[dev]"
```

### Alternative Package Managers
Using **uv**:
```bash
uv pip install drygram
```

Using **Poetry**:
```bash
poetry add drygram
```

### Installation from Source
To install the latest development code from GitHub:
```bash
git clone https://github.com/TG-BOTSNETWORK/drygram.git
cd drygram
pip install -e .
```

To install development and testing dependencies:
```bash
pip install -e .[dev]
```

---

## Quick Start

The following is a complete runnable bot that responds to `/start` messages:

```python
import asyncio
from drygram import DryClient, Gates, Message

# Initialize the client
app = DryClient("bot_session", api_id=12345, api_hash="abcdef", bot_token="YOUR_BOT_TOKEN")

# Register an update observer for /start text commands
@app.observe(Gates.text("/start"))
async def start_handler(msg: Message):
    await app.echo(msg, "Hello! I am a DryGram bot.")

async def main():
    async with app:
        print("Bot started. Press Ctrl+C to stop.")
        await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Session String Example

You can export and import session strings to run the client without persistent session files on disk:

```python
import asyncio
from drygram import DryClient

async def main():
    async with DryClient("session_name", api_id=12345, api_hash="abc") as app:
        # Export the active authenticated session to an encoded string
        session_str = await app.export_session()
        print("Session String:", session_str)

        # Import the session string into another instance
        await app.import_session(session_str)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Project Structure

```
drygram/
├── drygram/           # Primary package source code
├── docs/              # Detailed guides and manuals
├── examples/          # Complete client usage examples
├── tests/             # Comprehensive testing suite
├── pyproject.toml     # Project metadata and configurations
└── setup.py           # Legacy installer script
```

---

## Documentation

The full documentation is available under the [docs/](docs) directory, containing tutorials and details about the architecture. You can also build it locally using MkDocs:
```bash
pip install mkdocs-material
mkdocs serve
```

---

## Supported Platforms

- **Windows**: x86, x64, ARM64, and WSL.
- **Linux**: Ubuntu, Debian, Arch Linux, Fedora, CentOS, and Alpine.
- **macOS**: Intel and Apple Silicon (M1/M2/M3).
- **Containerization**: Full support for Docker and Kubernetes environments.

---

## Cryptographic Backend & Performance

DryGram dynamically manages cryptographic execution via its built-in Backend Manager:

| Backend | Implementation | Acceleration | Performance Note |
| :--- | :--- | :--- | :--- |
| **Cryptography** | Pure Python Engine | **Disabled** | High compatibility; works out-of-the-box on any platform without compiler tools. |

DryGram operates exclusively on standard Python-compatible cryptography libraries, ensuring compiled C extensions or platform-specific Visual Studio Build Tools are never required.

---

## Optional Voice Support

Voice and video calling functionality are supported through external integrations. Users can utilize third-party WebRTC/calling libraries alongside `DryClient` for streaming capabilities:
- **py-tgcalls** == `2.3.3`
- **ntgcalls** == `2.2.5`

These dependencies can be installed using the optional `calls` extra group:
```bash
pip install "drygram[calls]"
```

---

## Community

- **Support Chat**: [DryGram Support Chat](https://telegram.me/drygramchat)
- **Updates Channel**: [DryGram Updates Channel](https://telegram.me/drygramupdates)
- **GitHub Repository**: [GitHub Issues & Code](https://github.com/TG-BOTSNETWORK/drygram)

---

## Special Thanks

- **Telegram Team** for providing public MTProto documentation and protocol specifications.
- **The Python Open-Source Community** for developing the underlying dependencies and testing systems that power modern async development.
- **Contributors** and community members helping review code and report issues.

---

## Credits

- **Designed and Developed by**: [Santhu](https://github.com/Santhu)
- **Project Name**: DryGram
- **Source Code**: [TG-BOTSNETWORK/drygram](https://github.com/TG-BOTSNETWORK/drygram)

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).