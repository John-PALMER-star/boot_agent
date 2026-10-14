import os
from os.path import isfile
import subprocess

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
        if completed_process.returncode > 0:
            com_proc_output += f"Process exited with code {completed_process.returncode}."
        if completed_process.stdout and completed_process.stderr == 0:
            com_proc_output += "No output produced."
        else:
            com_proc_output += f"STDOUT: {completed_process.stdout}"
            com_proc_output += f"STDERR: {completed_process.stderr}"
        return com_proc_output

    except Exception as e:
        return f"Error encountered: {e}"


