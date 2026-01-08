from agents.tool import FunctionTool
from typing import List
import subprocess
import json

async def on_execute_command(tool_context, params) -> str:
    if isinstance(params, str):
        params = json.loads(params)

    command = params["command"]

    if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
        raise ValueError("command must be a list of strings")

    result = subprocess.run(command, check=False)

    return f"Command executed: {command} (return code {result.returncode})"


execute_command_tool = FunctionTool(
    name="execute_command",
    description="Execute a command represented as an argv list using subprocess.run(shell=False).",
    params_json_schema={
        "type": "object",
        "properties": {
            "command": {
                "type": "array",
                "items": {"type": "string"},
                "description": "argv list: executable followed by arguments"
            }
        },
        "required": ["command"],
        "additionalProperties": False,
    },
    on_invoke_tool=on_execute_command,
)
