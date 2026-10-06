import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None
    ) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)

        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

        #Will be True or False
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        completed = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30,)

        output: str = ""

        if completed.returncode != 0:
            output += f'Process exited with code {completed.returncode}\n'

        if not completed.stdout and not completed.stderr:
            output += 'No output produced\n'

        else:
            if completed.stdout:
                output += f'STDOUT: {completed.stdout}\n'

            if completed.stderr:
                output += f'STDERR: {completed.stderr}\n'
        
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
