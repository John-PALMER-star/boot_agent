import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.join(working_dir_abs, file_path)
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) 

    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot write to "{target_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{target_path}" as it is a directory'

    parent_path = os.path.dirname(target_path)
    os.makedirs(parent_path, mode=0o777, exist_ok=True)

    try: 
        with open(target_path, "w") as t:
            t.write(content)
        return f'Successfully wrote to "{target_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
