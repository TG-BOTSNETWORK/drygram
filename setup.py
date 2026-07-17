# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import sys
import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

version_globals = {}
with open(os.path.join(os.path.dirname(__file__), "drygram", "version.py"), "r", encoding="utf-8") as f:
    exec(f.read(), version_globals)
VERSION = version_globals["__version__"]
installation_banner = version_globals["installation_banner"]

def print_success_banner():
    try:
        banner_text = installation_banner()
        enc = sys.stdout.encoding or "utf-8"
        sys.stdout.write(banner_text.encode(enc, errors="replace").decode(enc) + "\n")
        sys.stdout.flush()
    except Exception:
        pass

class CustomInstall(install):
    def run(self):
        super().run()
        print_success_banner()

class CustomDevelop(develop):
    def run(self):
        super().run()
        print_success_banner()

setup(
    name="drygram",
    version=VERSION,
    packages=find_packages(),
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
    author="Santhu",
    author_email="telegramsanthu@gmail.com",
    description="Modern asynchronous Telegram MTProto framework.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TG-BOTSNETWORK/drygram",
    project_urls={
        "Homepage": "https://github.com/TG-BOTSNETWORK/drygram",
        "Documentation": "https://github.com/TG-BOTSNETWORK/drygram/docs",
        "Repository": "https://github.com/TG-BOTSNETWORK/drygram",
        "Bug Tracker": "https://github.com/TG-BOTSNETWORK/drygram/issues",
    },
    python_requires=">=3.13",
    license="GPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable"
    ],
    install_requires=[
        "cryptography>=42.0.0",
        "aiosqlite>=0.20.0"
    ],
    extras_require={
        "crypto": [
            "cryptography>=42.0.0"
        ],
        "calls": [
            "py-tgcalls==2.3.3",
            "ntgcalls==2.2.5"
        ],
        "mongodb": [
            "motor>=3.3.0"
        ],
        "redis": [
            "redis>=5.0.0"
        ],
        "postgres": [
            "asyncpg>=0.29.0"
        ],
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.4.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "mypy>=1.10.0",
            "bandit>=1.7.0",
            "safety>=3.0.0",
            "pip-audit>=2.7.0",
            "build>=1.2.0",
            "twine>=5.0.0"
        ],
        "docs": [
            "mkdocs-material>=9.5.0",
            "mkdocs-minify-plugin>=0.8.0",
            "mkdocs-git-revision-date-localized-plugin>=1.2.0"
        ]
    }
)
