# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from typing import Callable, Any, Tuple, List

class PriorityQueue:
    def __init__(self, num_workers: int = 5):
        self.queue: asyncio.PriorityQueue[Tuple[int, Any, Callable[..., Any], Tuple[Any, ...], dict]] = asyncio.PriorityQueue()
        self.num_workers = num_workers
        self.workers: List[asyncio.Task] = []
        self.running = False
        self._counter = 0

    async def start(self) -> None:
        self.running = True
        for _ in range(self.num_workers):
            self.workers.append(asyncio.create_task(self._worker_loop()))

    async def stop(self) -> None:
        self.running = False
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()

    async def push(self, priority: int, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._counter += 1
        await self.queue.put((priority, self._counter, func, args, kwargs))

    async def _worker_loop(self) -> None:
        while self.running:
            try:
                priority, _, func, args, kwargs = await self.queue.get()
                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                except Exception:
                    pass
                finally:
                    self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(0.1)
                continue
class QueueTask:
    def __init__(self, priority: int, action: Callable[..., Any]):
        self.priority = priority
        self.action = action
