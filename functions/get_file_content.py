import os
import config

def get_file_content(working_directory: str, file_path: str) -> str:

    working_dir_abs = os.path.abspath(working_directory)
    #print(f"Working_dir_abs: {working_dir_abs}")
    target_path = os.path.join(working_dir_abs, file_path)
    #print(f"Target_path: {target_path}")
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) 
    #print(f"Valid_target_dir: {valid_target_dir}")

    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot read "{target_path}" as it is outside the permitted working directory'

    if os.path.isfile(target_path):
        open_content = open(target_path)
        #with open(target_path, "r") as f:
            #open_content = f.read(config.MAX_CHARS)
        content = open_content.read(config.MAX_CHARS)
        if open_content.read(1):
            content += f'[...File "{target_path}" truncated at {config.MAX_CHARS} characters]'
        return content
    else:
        return f'Error: File not found or is not a regular file: "{target_path}"'
