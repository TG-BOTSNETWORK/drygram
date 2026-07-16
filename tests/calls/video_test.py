# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
import sys
from types import ModuleType
from drygram import DryClient

try:
    import pytgcalls
    PYTGCALLS_AVAILABLE = True
except ImportError:
    PYTGCALLS_AVAILABLE = False

@pytest.fixture(autouse=True)
def setup_pytgcalls_mock():
    class MockImportFinder:
        def find_spec(self, fullname, path, target=None):
            if fullname.startswith("pyrogram") or fullname.startswith("telethon"):
                from importlib.machinery import ModuleSpec
                return ModuleSpec(fullname, MockLoader())
            return None

    class MockLoader:
        def create_module(self, spec):
            class DM(ModuleType):
                def __getattr__(self, n):
                    if n == "Client":
                        return object
                    if n in ("ContinuePropagation", "StopPropagation"):
                        return Exception
                    if n[0].isupper():
                        return Exception if any(x in n for x in ("Error", "Exception", "Invalid", "Forbidden", "Failed", "Needed")) else object
                    return object
            return DM(spec.name)
        def exec_module(self, module):
            module.__path__ = []

    finder = MockImportFinder()
    sys.meta_path.insert(0, finder)
    orig_module = DryClient.__module__
    DryClient.__module__ = "pyrogram.client"
    yield
    DryClient.__module__ = orig_module
    sys.meta_path.remove(finder)
    for k in list(sys.modules.keys()):
        if k.startswith("pyrogram") or k.startswith("telethon"):
            sys.modules.pop(k, None)

pytestmark = pytest.mark.skipif(not PYTGCALLS_AVAILABLE, reason="py-tgcalls not installed")

@pytest.mark.asyncio
async def test_pytgcalls_video_instantiation_compatibility():
    client = DryClient("test_video_sess", api_id=123, api_hash="abc")
    call_client = pytgcalls.PyTgCalls(client)
    assert call_client is not None
