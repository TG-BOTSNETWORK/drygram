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
VERSION = version_globals["VERSION"]
installation_banner = version_globals["installation_banner"]

def print_success_banner():
    print(installation_banner())

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
        "aiosqlite>=0.20.0",
        "redis>=5.0.0",
        "motor>=3.3.0",
        "asyncpg>=0.29.0"
    ],
    extras_require={
        "calls": [
            "py-tgcalls==2.3.3",
            "ntgcalls==2.2.5"
        ],
        "voice": [
            "py-tgcalls==2.3.3",
            "ntgcalls==2.2.5"
        ],
        "streaming": [
            "py-tgcalls==2.3.3",
            "ntgcalls==2.2.5"
        ],
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0"
        ]
    }
)
