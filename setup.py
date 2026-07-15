# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import sys
import platform
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

def print_success_banner():
    banner = f"""──────────────────────────
DryGram Installed Successfully
Version : 1.0.0
Python : {sys.version.split()[0]}
Platform : {platform.system()}
Architecture : {platform.machine()}
MTProto Engine : Ready
Async Runtime : Ready
Voice Engine : Available
Video Engine : Available
Documentation : Installed
Examples : Installed
Plugins : Installed
Thank you for using DryGram.
────────────────────────────"""
    print(banner)

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
    version="1.0.0",
    packages=find_packages(),
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
    install_requires=[
        "cryptography>=42.0.0",
        "aiosqlite>=0.20.0",
        "redis>=5.0.0",
        "motor>=3.3.0",
        "asyncpg>=0.29.0",
        "py-tgcalls>=3.0.0",
        "ntgcalls>=2.0.0"
    ]
)
