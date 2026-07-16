# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from typing import Dict, List, Callable, Any, Optional
from drygram.dispatch.watcher import Watcher
from drygram.dispatch.gate import Gate
from drygram.dispatch.pipeline import MiddlewarePipeline
from drygram.dispatch.queue import PriorityQueue
from drygram.dispatch.scheduler import TaskScheduler

class Dispatcher:
    """
    Update events dispatcher engine.

    Attributes
    ----------
    watchers : Dict[int, List[Watcher]]
        Registered event watchers grouped by integer priority.
    pipeline : MiddlewarePipeline
        Global execution middleware pipeline.
    queue : PriorityQueue
        Execution queue for offloaded jobs.
    scheduler : TaskScheduler
        Active scheduled tasks registry.
    running : bool
        True if dispatcher background loops are running.
    """

    def __init__(self):
        """Initialize the Dispatcher state."""
        self.watchers: Dict[int, List[Watcher]] = {}
        self.pipeline = MiddlewarePipeline()
        self.queue = PriorityQueue()
        self.scheduler = TaskScheduler()
        self.running = False

    def add_watcher(self, watcher: Watcher) -> None:
        """
        Register a new Watcher handler.

        Parameters
        ----------
        watcher : Watcher
            The Watcher instance to add.
        """
        group = watcher.group
        if group not in self.watchers:
            self.watchers[group] = []
        self.watchers[group].append(watcher)

    def remove_watcher(self, watcher: Watcher) -> None:
        """
        Unregister an existing Watcher handler.

        Parameters
        ----------
        watcher : Watcher
            The Watcher instance to remove.
        """
        group = watcher.group
        if group in self.watchers and watcher in self.watchers[group]:
            self.watchers[group].remove(watcher)

    def register_watcher(self, gate: Optional[Gate] = None, group: int = 0) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        Register watcher callback function via decorator.

        Parameters
        ----------
        gate : Optional[Gate], default=None
            Filter condition check rule.
        group : int, default=0
            Group priority index.

        Returns
        -------
        Callable
            Decorator callback wrapper.
        """
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            watcher = Watcher(func, gate, group)
            self.add_watcher(watcher)
            return func
        return decorator

    def use_middleware(self, middleware: Callable[[Any, Callable[[], Any]], Any]) -> None:
        """
        Use a middleware callback.

        Parameters
        ----------
        middleware : Callable
            Middleware function taking (event, next_call) parameters.
        """
        self.pipeline.use(middleware)

    async def start(self) -> None:
        """Start background queue loops and scheduler workers."""
        self.running = True
        await self.queue.start()
        await self.scheduler.start()

    async def stop(self) -> None:
        """Stop active queues and scheduled task runners."""
        self.running = False
        await self.queue.stop()
        await self.scheduler.stop()

    async def feed_signal(self, event: Any) -> None:
        """
        Feed/Route an incoming event signal down the middleware pipeline.

        Parameters
        ----------
        event : Any
            The event signal payload.
        """
        await self.pipeline.execute(event, self._dispatch_event)

    async def _dispatch_event(self, event: Any) -> None:
        """
        Internally dispatch events to matching Watchers sequentially.

        Parameters
        ----------
        event : Any
            The event to dispatch.
        """
        sorted_groups = sorted(self.watchers.keys())
        for group in sorted_groups:
            for watcher in self.watchers[group]:
                try:
                    handled = await watcher.execute(event)
                    if handled:
                        break
                except Exception:
                    pass
