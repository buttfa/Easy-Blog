import os           # Use 'os' to determine whether the virtual environment folder exists
import subprocess   # Use 'subprocess' to execute shell commands
import sys          # Use 'sys' to obtain command-line parameters


# The path of the python virtual environment folder.
venv_folder_path = 'venv'

def build_environment():
    """Build the python virtual environment.
    """
    # Check if the python virtual environment exists.
    if os.path.exists(venv_folder_path) and os.path.isdir(venv_folder_path):
        print("[Easy-Blog]: The virtual environment already exists.")
        return
    
    # If not, create it and install the dependencies.
    subprocess.run(f"python3 -m venv {venv_folder_path}", shell=True)
    subprocess.run(f"source {venv_folder_path}/bin/activate && pip install -r requirements.txt && deactivate", shell=True)

def destroy_environment():
    """Destroy the python virtual environment.
    """
    subprocess.run(f"rm -rf {venv_folder_path}", shell=True)

def run_blog():
    """Run the blog.
    """
    subprocess.run(f"source {venv_folder_path}/bin/activate && export FLASK_APP=app && export FLASK_ENV=development && flask run && deactivate", shell=True)

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
        build_environment()
        print("[Easy-Blog]: Virtual environment built successfully.")
    # If the command is destroy, destroy the virtual environment.
    elif sys.argv[1] == "destrory":
        print("[Easy-Blog]: Destroying the virtual environment...")
        destroy_environment()
        print("[Easy-Blog]: Virtual environment destroyed successfully.")
    # If the command is run, run the blog.
    elif sys.argv[1] == "run":
        print("[Easy-Blog]: Running the blog...")
        run_blog()
    # If the command is invalid, print an error message.
    else:
        print("[Easy-Blog]: Invalid command.")


if __name__ == "__main__":
    main()