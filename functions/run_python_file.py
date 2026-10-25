import os
from os.path import isfile
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Safely executes a python program within a permitted working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python program.",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])
    
    if args is None:
        args = []
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if os.path.isfile(target_dir) != True:
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if target_dir.endswith('.py') == False:
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python3", os.path.abspath(target_dir)] + args
        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30) 
        com_proc_output = ""
        if completed_process.returncode != 0:
            com_proc_output += f"Process exited with code {completed_process.returncode}."
        if not completed_process.stdout and not completed_process.stderr:
            com_proc_output += "No output produced."
        else:
            com_proc_output += f"STDOUT: {completed_process.stdout}"
            com_proc_output += f"STDERR: {completed_process.stderr}"
        return com_proc_output

    except Exception as e:
        return f"Error encountered: {e}"


