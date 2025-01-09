import subprocess  # Use 'subprocess' to execute shell commands
from script.config import venv_folder_path, db_folder_path

def destroy_environment() -> bool:
    """Destroy the Easy-Blog environment.

    Returns:
        bool: Return True when succeed to destroy the environment, otherwise return False.
    """
    if subprocess.run(f"rm -rf {venv_folder_path}", shell=True).returncode != 0:
        print("[Easy-Blog:destroy]: Fail to delete the virtual python environment.")
        return False

    if subprocess.run(f"rm -rf {db_folder_path}", shell=True).returncode != 0:
        print("[Easy-Blog:destroy]: Fail to delete the database.")
        return False

    return True