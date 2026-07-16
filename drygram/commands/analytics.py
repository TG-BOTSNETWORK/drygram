# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

from typing import Dict, Any
from drygram.commands.history import CommandHistory

class CommandAnalytics:
    """
    Computes analytics and usage frequencies from execution history.
    """
    def __init__(self, history: CommandHistory):
        self.history = history

    def get_statistics(self) -> Dict[str, Any]:
        """Compute aggregated performance metrics."""
        records = self.history.records
        total = len(records)
        successes = sum(1 for r in records if r.success)
        failures = total - successes
        
        stats: Dict[str, Any] = {
            "total_executions": total,
            "successful_executions": successes,
            "failed_executions": failures,
            "per_command": {}
        }
        
        for r in records:
            name = r.command_name
            if name not in stats["per_command"]:
                stats["per_command"][name] = {"total": 0, "success": 0, "failed": 0}
            stats["per_command"][name]["total"] += 1
            if r.success:
                stats["per_command"][name]["success"] += 1
            else:
                stats["per_command"][name]["failed"] += 1
                
        return stats

def get_statistics() -> Dict[str, Any]:
    """Module-level compatibility function to retrieve aggregated stats."""
    from drygram.commands.history import _global_history
    analytics = CommandAnalytics(_global_history)
    return analytics.get_statistics()
