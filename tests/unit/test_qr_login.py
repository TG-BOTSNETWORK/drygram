# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient

@pytest.mark.asyncio
async def test_qr_login_flow():
    client = DryClient("test_qr", api_id=1, api_hash="abc")
    await client.start()
    qr_link = await client.request_qr_code()
    assert qr_link.startswith("tg://login")
    await client.stop()
