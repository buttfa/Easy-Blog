import os           # Use 'os' to determine whether the virtual environment folder exists
import subprocess   # Use 'subprocess' to execute shell commands
import sys          # Use 'sys' to obtain command-line parameters


# The path of the python virtual environment folder.
venv_folder_path = 'backend/venv'


def build_environment() -> bool:
    """Build the python virtual environment.

    Returns:
        bool: Return True when succeed to build the environment, otherwise return False.
    """
    # Check if the python virtual environment exists.
    if os.path.exists(venv_folder_path) and os.path.isdir(venv_folder_path):
        print("[Easy-Blog:build]: The virtual environment already exists.")
        return False
    
    # If not, create it and install the dependencies.
    if subprocess.run(f"python3 -m venv {venv_folder_path}", shell=True).returncode != 0:
        print("[Easy-Blog:build]: Fail to create the virtual environment.")
        return False
    if subprocess.run(f"source {venv_folder_path}/bin/activate && pip install -r backend/requirements.txt && deactivate", shell=True).returncode != 0:
        print("[Easy-Blog:build]: Fail to install the dependencies.")
        return False
    
    return True


def destroy_environment() -> bool:
    """Destroy the python virtual environment.

    Returns:
        bool: Return True when succeed to destrory the environment, otherwise return False.
    """
    if subprocess.run(f"rm -rf {venv_folder_path}", shell=True).returncode != 0:
        print("[Easy-Blog:destroy]: Fail to destroy the virtual environment.")
        return False
    
    return True

def run_blog() -> bool:
    """Run the blog.

    Returns:
        bool: Return False when fail to run the blog.
    """
    if subprocess.run(f"source {venv_folder_path}/bin/activate && export FLASK_APP=backend/app && export FLASK_ENV=development && flask run --debug && deactivate", shell=True).returncode != 0:
        print("[Easy-Blog:run]: Fail to run the Flask server.")
        return False

    return True

def main():
    """The main function.
    """


    # Check if the command is valid.
    if len(sys.argv) > 2:
        print("[Easy-Blog]: Invalid command.")
        return
    

    # If the command is build, build the virtual environment.
    if sys.argv[1] == "build":
        print("[Easy-Blog]: Building the virtual environment...")
        if build_environment():
            print("[Easy-Blog]: Succeed to build the virtual environment.")
            print("[Easy-Blog]: You can run the blog by typing 'python3 eblog.py run'.")
        else:
            print("[Easy-Blog]: Fail to build the virtual environment.")

    
    # If the command is destroy, destroy the virtual environment.
    elif sys.argv[1] == "destrory":
        print("[Easy-Blog]: Destroying the environment...")
        if destroy_environment():
            print("[Easy-Blog]: Succeed to destroy the environment.")
        else:
            print("[Easy-Blog]: Fail to destroy the environment.")
    
    # If the command is run, run the blog.
    elif sys.argv[1] == "run":
        print("[Easy-Blog]: Running the blog...")
        if run_blog():
            print("[Easy-Blog]: Succeed to run the blog.")
        else:
            print("[Easy-Blog]: Fail to run the blog.")

    
    # If the command is invalid, print an error message.
    else:
        print("[Easy-Blog]: Invalid command.")


if __name__ == "__main__":
    main()