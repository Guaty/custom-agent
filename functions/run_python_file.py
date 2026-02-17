import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]
        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True, 
            text=True, 
            timeout=30
        )

        output_str = []
        if completed_process.returncode != 0:
            output_str.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout is None and completed_process.stderr is None:
            output_str.append("No output produced")
        else:
            if completed_process.stdout:
                output_str.append(f"STDOUT: {completed_process.stdout}")
            if completed_process.stderr:
                output_str.append(f"STDERR: {completed_process.stderr}")
        
        return "\n".join(output_str)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Exceute the given Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file execute, relative to working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Arguments to pass to the file, optional"
            ),
        },
        required=["file_path"]
    ),
)
