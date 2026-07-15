# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import DryClient
from drygram.errors.rpc import AuthError

@pytest.mark.asyncio
async def test_password_login_flow():
    client = DryClient("test_pwd", api_id=1, api_hash="abc")
    await client.start()
    
    assert await client.submit_password("correct_pass") is True
    
    with pytest.raises(AuthError):
        await client.submit_password("invalid")
        
    await client.stop()
