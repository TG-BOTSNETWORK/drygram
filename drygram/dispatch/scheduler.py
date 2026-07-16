# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import time
from typing import Callable, Any, List, Optional

class ScheduledTask:
    """
    Representation of scheduled job task.

    Parameters
    ----------
    action : Callable[..., Any]
        Function to execute.
    delay : float
        Initial execution delay in seconds.
    interval : Optional[float], default=None
        Execution loop frequency in seconds.
    args : tuple, default=()
        Call arguments.
    kwargs : dict, default={}
        Call keyword arguments.

    Attributes
    ----------
    action : Callable[..., Any]
        Target function.
    run_at : float
        Unix epoch timestamp of target execution.
    interval : Optional[float]
        Recurring interval delay.
    args : tuple
        Positional arguments.
    kwargs : dict
        Keyword arguments.
    """

    def __init__(self, action: Callable[..., Any], delay: float, interval: Optional[float] = None, args: tuple = (), kwargs: dict = {}):
        """Initialize the task state."""
        self.action = action
        self.run_at = time.time() + delay
        self.interval = interval
        self.args = args
        self.kwargs = kwargs

class TaskScheduler:
    """
    Precision asynchronous scheduler engine.

    Attributes
    ----------
    tasks : List[ScheduledTask]
        Registry of scheduled tasks.
    running : bool
        True if the loop runner is active.
    """

    def __init__(self):
        """Initialize the TaskScheduler."""
        self.tasks: List[ScheduledTask] = []
        self._lock = asyncio.Lock()
        self._loop_task: Optional[asyncio.Task] = None
        self.running = False

    async def start(self) -> None:
        """Start the background scheduler task thread."""
        self.running = True
        self._loop_task = asyncio.create_task(self._scheduler_loop())

    async def stop(self) -> None:
        """Stop/Cancel the background scheduler task thread."""
        self.running = False
        if self._loop_task:
            self._loop_task.cancel()
            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass
            self._loop_task = None

    async def schedule(self, action: Callable[..., Any], delay: float, interval: Optional[float] = None, *args: Any, **kwargs: Any) -> ScheduledTask:
        """
        Schedule a task.

        Parameters
        ----------
        action : Callable[..., Any]
            Target callback.
        delay : float
            Delay before execution.
        interval : Optional[float], default=None
            If provided, run task periodically.
        *args : Any
            Positional parameters.
        **kwargs : Any
            Keyword parameters.

        Returns
        -------
        ScheduledTask
            The created task reference.
        """
        task = ScheduledTask(action, delay, interval, args, kwargs)
        async with self._lock:
            self.tasks.append(task)
        return task

    async def cancel(self, task: ScheduledTask) -> None:
        """
        Cancel a scheduled task.

        Parameters
        ----------
        task : ScheduledTask
            Task reference to cancel.
        """
        async with self._lock:
            if task in self.tasks:
                self.tasks.remove(task)

    async def _scheduler_loop(self) -> None:
        """Background loop executing due tasks."""
        while self.running:
            now = time.time()
            to_run = []
            async with self._lock:
                remaining_tasks = []
                for task in self.tasks:
                    if now >= task.run_at:
                        to_run.append(task)
                        if task.interval is not None:
                            task.run_at = now + task.interval
                            remaining_tasks.append(task)
                    else:
                        remaining_tasks.append(task)
                self.tasks = remaining_tasks
            
            for task in to_run:
                try:
                    if asyncio.iscoroutinefunction(task.action):
                        asyncio.create_task(task.action(*task.args, **task.kwargs))
                    else:
                        task.action(*task.args, **task.kwargs)
                except Exception:
                    pass
            await asyncio.sleep(0.1)
