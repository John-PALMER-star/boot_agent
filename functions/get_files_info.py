import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) 
    
    if valid_target_dir != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'

    if os.path.isdir(target_dir):
        #return f"Success: '{target_dir}' is a valid directory."
        strings = []
        for file in os.listdir(target_dir):
            name = file
            size = os.path.getsize(os.path.join(target_dir, file))
            is_dir = os.path.isdir(os.path.join(target_dir, file))
            file_string = f"- {name}: file_size={size}bytes, is_dir={is_dir}"
            strings.append(file_string)
        return "\n".join(strings)

    else:
        return f"'{target_dir}' is not a directory (it might be a file or doesn't exist)."
