# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
from drygram import DryClient

try:
    import ntgcalls
    NTGCALLS_AVAILABLE = True
except ImportError:
    NTGCALLS_AVAILABLE = False

pytestmark = pytest.mark.skipif(not NTGCALLS_AVAILABLE, reason="ntgcalls not installed")

@pytest.mark.asyncio
async def test_ntgcalls_instantiation_compatibility():
    client = DryClient("test_ntgcalls_sess", api_id=123, api_hash="abc")
    call_client = ntgcalls.NTgCalls()
    assert call_client is not None
