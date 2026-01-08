from agents.tool import FunctionTool
from pathlib import Path
import json

async def on_read_file(tool_context, params) -> str:
    if isinstance(params, str):
        params = json.loads(params)

    p = Path(params["path"])
    if not p.exists():
        raise FileNotFoundError(str(p))

    max_chars = int(params.get("max_chars", 200_000))
    return p.read_text(encoding="utf-8", errors="replace")[:max_chars]

read_file_tool = FunctionTool(
    name="read_file",
    description="Read a local text file and return its contents (optionally truncated).",
    params_json_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "max_chars": {"type": "integer"},
        },
        "required": ["path"],
        "additionalProperties": False,
    },
    on_invoke_tool=on_read_file,
)
