import os
import config

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Safely reads a file within a permitted working directory, returning up to MAX_CHARS of content and reporting errors or truncation when necessary.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:

    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.join(working_dir_abs, file_path)
    valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) 

    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot read "{target_path}" as it is outside the permitted working directory'

    if os.path.isfile(target_path):
        open_content = open(target_path)
        content = open_content.read(config.MAX_CHARS)
        if open_content.read(1):
            content += f'[...File "{target_path}" truncated at {config.MAX_CHARS} characters]'
        return content
    else:
        return f'Error: File not found or is not a regular file: "{target_path}"'
