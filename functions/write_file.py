import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_write_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_write_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_write_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_write_path), exist_ok=True)

        with open(target_write_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file {file_path}: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write (or overwrite) contents to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write to, relative to working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write"
            ),
        },
        required=["file_path", "content"]
    ),
)
