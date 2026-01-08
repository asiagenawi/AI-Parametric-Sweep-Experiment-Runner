from agents.tool import FunctionTool
from pathlib import Path
from typing import Dict, Any
import json

async def on_write_file(tool_context, params) -> str:
    # params arrives as a JSON string
    if isinstance(params, str):
        params = json.loads(params)

    path = params["path"]
    content = params["content"]

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

    return f"Wrote file: {p.resolve()}"

write_file_tool = FunctionTool(
    name="write_file",
    description="Create or overwrite a file on disk with the given text content.",
    params_json_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": ["path", "content"],
    },
    on_invoke_tool=on_write_file,
)
