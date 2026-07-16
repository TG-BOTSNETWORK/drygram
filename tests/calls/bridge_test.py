# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
from drygram.bridge import BridgeClient, BridgeAdapter

@pytest.mark.asyncio
async def test_bridge_client_compatibility():
    client = BridgeClient("test_bridge_sess", api_id=123, api_hash="abc")
    await client.start()
    
    assert client.loop is not None
    assert client.mtproto is not None
    assert client.storage is not None
    assert client.network is not None
    assert client.raw is not None
    assert client.is_connected is True

    adapter = BridgeAdapter(client)
    assert adapter.mtproto is client.mtproto
    assert adapter.session is client.session
    assert adapter.loop is client.loop
    assert adapter.dispatcher is client.dispatcher
    assert adapter.network is client.network

    await client.stop()
