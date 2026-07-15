# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram.dispatch.pipeline import MiddlewarePipeline

@pytest.mark.asyncio
async def test_middleware_pipeline():
    pipe = MiddlewarePipeline()
    
    order = []
    
    async def middleware1(event, next_call):
        order.append(1)
        res = await next_call()
        order.append(3)
        return res
        
    async def handler(event):
        order.append(2)
        return "done"
        
    pipe.use(middleware1)
    
    res = await pipe.execute("event", handler)
    assert res == "done"
    assert order == [1, 2, 3]
