# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import inspect
from typing import Callable, Any, List

class MiddlewarePipeline:
    def __init__(self):
        self.middlewares: List[Callable[[Any, Callable[[], Any]], Any]] = []

    def use(self, middleware: Callable[[Any, Callable[[], Any]], Any]) -> None:
        self.middlewares.append(middleware)

    async def execute(self, event: Any, final_handler: Callable[[Any], Any]) -> Any:
        index = -1

        async def dispatch(i: int) -> Any:
            nonlocal index
            if i <= index:
                raise RuntimeError("next() called multiple times")
            index = i
            if i < len(self.middlewares):
                middleware = self.middlewares[i]
                
                async def next_call() -> Any:
                    return await dispatch(i + 1)
                
                if asyncio.iscoroutinefunction(middleware):
                    return await middleware(event, next_call)
                else:
                    res = middleware(event, next_call)
                    if asyncio.iscoroutine(res) or inspect.isawaitable(res):
                        return await res
                    return res
            else:
                if asyncio.iscoroutinefunction(final_handler):
                    return await final_handler(event)
                else:
                    res = final_handler(event)
                    if asyncio.iscoroutine(res) or inspect.isawaitable(res):
                        return await res
                    return res

        return await dispatch(0)
