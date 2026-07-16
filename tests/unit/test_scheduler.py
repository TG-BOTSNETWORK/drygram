# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import asyncio
from drygram import TaskScheduler

@pytest.mark.asyncio
async def test_scheduler_task():
    sched = TaskScheduler()
    await sched.start()
    
    run_count = 0
    def job():
        nonlocal run_count
        run_count += 1
        
    task = await sched.schedule(job, delay=0.1)
    await asyncio.sleep(0.3)
    assert run_count == 1
    
    await sched.stop()
