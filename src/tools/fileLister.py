from agents.tool import FunctionTool
from pathlib import Path
import json

async def on_list_files(tool_context, params) -> str:
    if isinstance(params, str):
        params = json.loads(params)

    root = Path(params.get("root", "."))
    pattern = params.get("pattern", "**/*")

    files = [str(p.as_posix()) for p in root.glob(pattern) if p.is_file()]
    files.sort()
    return json.dumps(files)

list_files_tool = FunctionTool(
    name="list_files",
    description="List files under a directory using a glob pattern.",
    params_json_schema={
        "type": "object",
        "properties": {
            "root": {"type": "string"},
            "pattern": {"type": "string"}
        },
        "additionalProperties": False
    },
    on_invoke_tool=on_list_files
)
