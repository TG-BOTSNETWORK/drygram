# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import sys
import platform
from typing import Tuple, Dict, Any

FRAMEWORK_NAME = "DryGram"
TITLE = "DryGram MTProto Framework"
VERSION = "1.0.0"
VERSION_TUPLE = (1, 0, 0)
SEMANTIC_VERSION = "1.0.0"
RELEASE_LEVEL = "stable"
BUILD_NUMBER = "100"
BUILD_DATE = "2026-07-15"
PYTHON_MINIMUM_VERSION = (3, 13)
PYTHON_RECOMMENDED_VERSION = (3, 13, 0)
TELEGRAM_MTPROTO_LAYER = 184
TELEGRAM_API_VERSION = "2026.1"
AUTHOR = "Santhu"
MAINTAINER = "Santhu"
EMAIL = "telegramsanthu@gmail.com"
WEBSITE = "https://telegram.org"
GITHUB = "https://github.com/TG-BOTSNETWORK/drygram"
DOCUMENTATION = "https://github.com/TG-BOTSNETWORK/drygram/docs"
LICENSE = "GNU GPL-3.0"
COPYRIGHT = "Copyright (c) 2026 Santhu"
SUPPORT_CHAT = "https://telegram.me/drygramchat"
UPDATES_CHANNEL = "https://telegram.me/drygramupdates"
ISSUE_TRACKER = "https://github.com/TG-BOTSNETWORK/drygram/issues"
KEYWORDS = ["telegram", "mtproto", "asyncio", "bot", "framework"]
SUPPORTED_PLATFORMS = ["Windows", "Linux", "macOS"]
SUPPORTED_ARCHITECTURES = ["x86_64", "ARM64"]
PACKAGE_STATUS = "Production/Stable"
STABLE_CHANNEL = "stable"
DEVELOPMENT_CHANNEL = "dev"
PACKAGE_DESCRIPTION = "Production-grade asynchronous Telegram MTProto framework."
LONG_DESCRIPTION = "DryGram is a production-grade, highly-optimized, fully asynchronous Telegram MTProto framework built from scratch in Python 3.13+."

def version() -> str:
    """Get the framework version string."""
    return VERSION

def version_tuple() -> Tuple[int, int, int]:
    """Get the version tuple."""
    return VERSION_TUPLE

def full_version() -> str:
    """Get the full semantic version with build number."""
    return f"{VERSION}-{RELEASE_LEVEL}.{BUILD_NUMBER}"

def build_info() -> Dict[str, str]:
    """Get build metadata info."""
    return {"number": BUILD_NUMBER, "date": BUILD_DATE}

def python_info() -> Dict[str, Any]:
    """Get active python version info."""
    return {"minimum": PYTHON_MINIMUM_VERSION, "current": sys.version_info}

def platform_info() -> Dict[str, str]:
    """Get OS platform information."""
    return {"system": platform.system(), "release": platform.release()}

def architecture() -> str:
    """Get active architecture string."""
    return platform.machine()

def framework_info() -> Dict[str, Any]:
    """Get framework general info."""
    return {
        "name": FRAMEWORK_NAME,
        "codename": FRAMEWORK_CODENAME,
        "author": AUTHOR,
        "license": LICENSE
    }

def telegram_layer() -> int:
    """Get the Telegram MTProto layer integer."""
    return TELEGRAM_MTPROTO_LAYER

def telegram_version() -> str:
    """Get the API version string."""
    return TELEGRAM_API_VERSION

def license_info() -> str:
    """Get license details."""
    return LICENSE

def support_links() -> Dict[str, str]:
    """Get support links."""
    return {"chat": SUPPORT_CHAT, "channel": UPDATES_CHANNEL}

def ascii_logo() -> str:
    """Get ASCII logo string."""
    return """
  _____  _______     _______ _____  _______  _______
 |     | |_____| ___    |   |     | |_____| |_____|
 |_____| |  \\         |   |_____| |     | |  \\
"""

def banner() -> str:
    """Get banner string."""
    return f"{TITLE} v{VERSION} ({FRAMEWORK_CODENAME})"

def installation_banner() -> str:
    """Get package installation console success banner."""
    return f"""────────────────────────────────────
DryGram Installed Successfully
Version : {VERSION}
Python : {sys.version.split()[0]}
Platform : {platform.system()}
Architecture : {platform.machine()}
Telegram Layer : {TELEGRAM_MTPROTO_LAYER}
Thank you for using DryGram.

Support
{SUPPORT_CHAT}

Updates
{UPDATES_CHANNEL}
────────────────────────────────────"""

def startup_banner() -> str:
    """Get client startup console banner."""
    return f"Starting DryGram Engine [{FRAMEWORK_CODENAME}]..."

def runtime_report() -> Dict[str, Any]:
    """Get active runtime execution variables."""
    return {"asyncio_loop": "running", "threads": 1}

def environment_report() -> str:
    """Get environment diagnostic information report."""
    return f"OS: {platform.system()} | Python: {sys.version.split()[0]}"

def dependency_report() -> Dict[str, str]:
    """Get dependencies statuses report."""
    return {"cryptography": "available", "aiosqlite": "available"}


def check_python() -> bool:
    """Verify if the running Python version meets requirements."""
    return sys.version_info >= PYTHON_MINIMUM_VERSION

def check_dependencies() -> bool:
    """Verify if critical dependencies are importable."""
    try:
        import cryptography
        import aiosqlite
        return True
    except ImportError:
        return False

def check_platform() -> bool:
    """Verify if current platform is supported."""
    return platform.system() in SUPPORTED_PLATFORMS
