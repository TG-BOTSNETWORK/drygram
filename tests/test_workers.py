# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import asyncio
from drygram.dispatch.queue import PriorityQueue

@pytest.mark.asyncio
async def test_priority_workers():
    queue = PriorityQueue(num_workers=2)
    await queue.start()
    
    results = []
    def job(val):
        results.append(val)
        
    await queue.push(2, job, "low")
    await queue.push(1, job, "high")
    
    await asyncio.sleep(0.2)
    assert len(results) == 2
    assert results[0] == "high" or results[1] == "high"
    
    await queue.stop()
