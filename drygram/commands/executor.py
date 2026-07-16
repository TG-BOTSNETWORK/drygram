# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import inspect
from typing import Any, List, Dict
from drygram.commands.context import CommandContext
from drygram.commands.converters import Converter

class CommandExecutor:
    """
    Analyzes parameters, parses arguments/flags, converts types, and invokes callback.
    """
    @staticmethod
    async def execute(context: CommandContext) -> Any:
        """Parse arguments against signature and execute command."""
        command = context.command
        func = command.callback
        sig = inspect.signature(func)
        
        args = []
        kwargs = {}
        parameters = list(sig.parameters.values())
        
        if not parameters:
            raise ValueError("Command callback must accept a Context instance.")
            
        args.append(context)
        
        # Pull parameter tokens
        passed_args = list(context.arguments)
        passed_flags = dict(context.flags)
        
        for param in parameters[1:]:
            param_name = param.name
            param_type = param.annotation
            
            if param_type == inspect.Parameter.empty and hasattr(command, "args"):
                for arg_spec in command.args:
                    if getattr(arg_spec, "name", None) == param_name:
                        param_type = getattr(arg_spec, "type", inspect.Parameter.empty)
                        break
            
            if param_name in passed_flags:
                raw_val = passed_flags.pop(param_name)
                if param_type != inspect.Parameter.empty:
                    val = Converter.convert(str(raw_val), param_type)
                else:
                    val = raw_val
                kwargs[param_name] = val
            elif len(passed_args) > 0:
                raw_val = passed_args.pop(0)
                if param_type != inspect.Parameter.empty:
                    val = Converter.convert(str(raw_val), param_type)
                else:
                    val = raw_val
                if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                    args.append(val)
                else:
                    kwargs[param_name] = val
            else:
                if param.default != inspect.Parameter.empty:
                    kwargs[param_name] = param.default
                elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                    pass
                else:
                    raise ValueError(f"Missing required parameter: {param_name}")

        # Run async/sync command callback
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)

    @staticmethod
    async def run(callback: Any) -> Any:
        """Compatibility helper to run arbitrary callback."""
        if inspect.iscoroutinefunction(callback):
            return await callback()
        return callback()
