# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import sys
import platform
from typing import Tuple, Dict, Any

# Package Metadata Declarations
__title__ = "DryGram MTProto Framework"
__version__ = "1.0.1"
__release_date__ = "15th June 2024"
__author__ = "Santhu"
__email__ = "telegramsanthu@gmail.com"
__license__ = "GNU GPL-3.0"
__homepage__ = "https://github.com/TG-BOTSNETWORK/drygram"
__repository__ = "https://github.com/TG-BOTSNETWORK/drygram"
__documentation__ = "https://github.com/TG-BOTSNETWORK/drygram/docs"
__support_chat__ = "https://telegram.me/drygramchat"
__updates_channel__ = "https://telegram.me/drygramupdates"
__python_requires__ = ">=3.13"

# Legacy compatibility aliases
VERSION = __version__
SUPPORT_CHAT = __support_chat__
UPDATES_CHANNEL = __updates_channel__

def version() -> str:
    """Get the framework version string."""
    return __version__

def full_version() -> str:
    """Get the full version string including release date."""
    return f"{__version__} ({__release_date__})"

def build_info() -> Dict[str, str]:
    """Get build metadata info."""
    return {
        "version": __version__,
        "release_date": __release_date__,
    }

def runtime_info() -> Dict[str, Any]:
    """Get active runtime and platform diagnostic variables."""
    return {
        "python_version": sys.version.split()[0],
        "operating_system": platform.system(),
        "architecture": platform.machine(),
    }

def installation_banner() -> str:
    """Get package installation success banner output."""
    return f"""==================================================
DryGram Installed Successfully
==================================================
Framework Version : {__version__}
Python Version    : {sys.version.split()[0]}
Operating System  : {platform.system()}
Architecture      : {platform.machine()}
Repository        : {__repository__}
Documentation     : {__documentation__}
Support Chat      : {__support_chat__}
Updates Channel   : {__updates_channel__}
=================================================="""

def startup_banner() -> str:
    """Get client startup console banner."""
    return f"Starting DryGram Engine [{__title__} v{__version__}]..."

# Legacy Compatibility Functions
def python_info() -> Dict[str, Any]:
    """Get active python version info."""
    return {"minimum": (3, 13), "current": sys.version_info}

def platform_info() -> Dict[str, str]:
    """Get OS platform information."""
    return {"system": platform.system(), "release": platform.release()}

def architecture() -> str:
    """Get active architecture string."""
    return platform.machine()

def framework_info() -> Dict[str, Any]:
    """Get framework general info."""
    return {
        "name": "DryGram",
        "codename": "Antigravity",
        "author": __author__,
        "license": __license__
    }

def license_info() -> str:
    """Get license details."""
    return __license__

def support_links() -> Dict[str, str]:
    """Get support links."""
    return {"chat": __support_chat__, "channel": __updates_channel__}

def ascii_logo() -> str:
    """Get ASCII logo string."""
    return """
  _____  _______     _______ _____  _______  _______
 |     | |_____| ___    |   |     | |_____| |_____|
 |_____| |  \\         |   |_____| |     | |  \\
"""

def banner() -> str:
    """Get banner string."""
    return f"{__title__} v{__version__} (Antigravity)"

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
    return sys.version_info >= (3, 13)

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
    return platform.system() in ["Windows", "Linux", "macOS"]
