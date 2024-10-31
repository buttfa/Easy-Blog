# Used here to determine whether the virtual environment folder exists
import os
# Used here to execute shell commands
import subprocess
# Used here to obtain command-line parameters
import sys

venv_folder_path = 'venv'
def build_environment():
    # Check if the python virtual environment exists.
    if os.path.exists(venv_folder_path) and os.path.isdir(venv_folder_path):
        print("[Easy-Blog]: The virtual environment already exists.")
        return
    
    # If not, create it and install the dependencies.
    subprocess.run(f"python3 -m venv {venv_folder_path}", shell=True)
    subprocess.run(f"source {venv_folder_path}/bin/activate && pip install -r requirements.txt && deactivate", shell=True)

def destroy_environment():
    subprocess.run(f"rm -rf {venv_folder_path}", shell=True)

def run_blog():
    subprocess.run(f"source {venv_folder_path}/bin/activate && export FLASK_APP=app && export FLASK_ENV=development && flask run && deactivate", shell=True)

def main():

    if len(sys.argv) > 1:
        print("[Easy-Blog]: Invalid command.")
        return
    
    if sys.argv[0] == "build":
        print("[Easy-Blog]: Building the virtual environment...")
        build_environment()
    elif sys.argv[0] == "destroy":
        print("[Easy-Blog]: Destroying the virtual environment...")
        destroy_environment()
    elif sys.argv[0] == "run":
        print("[Easy-Blog]: Running the blog...")
    else:
        print("[Easy-Blog]: Invalid command.")


if __name__ == "__main__":
    main()