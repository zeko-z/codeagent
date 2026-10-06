from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
import json

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads files for their content, returning them in a string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to attain content from the relevant file, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"]
        },
    },
}

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "runs the code with a .py file specified in the file_path parameter",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "items": {
                        "type": "string"
                    },
                    "description": "file path of the .py file to run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "description": "any additional data to run in the specified .py file"
                },
            },
            "required": ["file_path"]
        },
    },
}

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes to the specified files or creates new ones relative to the working directory, adding contents",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path for the code to write to, relative to the working directory (default is the working directory itself)",
                },
                "content":{
                    "type":"string",
                    "description":"the content to write to the specified file"
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    from collections.abc import Callable

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,

    }

    if function_name not in function_map:
        return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"Error: Unknown function: {function_name}",
    }

    function_args["working_directory"] = "./calculator"

    result = function_map[function_name](**function_args)

    return {
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": result,
}
