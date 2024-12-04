import os  # Use 'os' to determine whether the virtual environment folder exists
import subprocess  # Use 'subprocess' to execute shell commands
import sys  # Use 'sys' to obtain command-line parameters
import threading


# The path of the python virtual environment folder.
venv_folder_path = "backend/venv"
# The path of the database folder.
db_folder_path = "backend/db"
# system_de
system_dependencies = {"centos": {"node.js": "sudo yum -y install nodejs", "gcc": "sudo yum -y install gcc", "python3-devel":"sudo yum -y install python3-devel"}}


def build_system_dependencies(linux_release_name: str) -> bool:
    """Build the system dependencies.

    Args:
        linux_release_name (str): Current Linux system release name.

    Returns:
        bool: Return True indicates a successful build, while return False indicates a failed build.
    """
    for dependencies_name, dependencies_cmd in system_dependencies[
        linux_release_name
    ].items():
        if subprocess.run(dependencies_cmd, shell=True).returncode != 0:
            print(f"[Easy-Blog:build]: Fail to install {dependencies_name}")
            return False

    return True


def build_fronted() -> bool:
    """Build the frontend of the blog.

    Returns:
        bool: Return True indicates a successful build, while return False indicates a failed build.
    """
    # Install the dependencies of the frontend.
    if subprocess.run("cd frontend && npm install", shell=True).returncode != 0:
        print("[Easy-Blog:build]: Fail to install the dependencies of the frontend.")
        return False

    return True


def build_backend() -> bool:
    """Build the backend of the blog.

    Returns:
        bool: Return True indicates a successful build, while return False indicates a failed build.
    """

    # Create the database folder.
    if os.path.exists(db_folder_path) and os.path.isdir(db_folder_path):
        print("[Easy-Blog:build]: The database folder already exists.")
        return False
    os.mkdir(db_folder_path)

    # Check if the python virtual environment exists.
    if os.path.exists(venv_folder_path) and os.path.isdir(venv_folder_path):
        print("[Easy-Blog:build]: The virtual python environment already exists.")
        return False

    # If not, create it and install the dependencies.
    if (
        subprocess.run(f"python3 -m venv {venv_folder_path}", shell=True).returncode
        != 0
    ):
        print("[Easy-Blog:build]: Fail to create the virtual python environment.")
        return False
    if (
        subprocess.run(
            f"bash -c 'source {venv_folder_path}/bin/activate && pip install -r backend/requirements.txt && deactivate'",
            shell=True,
        ).returncode
        != 0
    ):
        print("[Easy-Blog:build]: Fail to install the python dependencies.")
        return False

    return True


def build_environment(linux_release_name: str) -> bool:
    """Build the Easy-Blog environment.

    Args:
        linux_release_name (str): Current Linux system release name.

    Returns:
        bool: Return True when succeed to build the environment, otherwise return False.
    """

    if not build_system_dependencies(linux_release_name):
        return False

    if not build_fronted():
        return False

    if not build_backend():
        return False

    return True


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


def run_frontend():
    """Run the frontend."""
    subprocess.run("cd frontend && npx vite --port=5173", shell=True)


def run_backend():
    """Run the backend."""
    subprocess.run(
        f"bash -c 'source {venv_folder_path}/bin/activate && export FLASK_APP=backend/blog && export FLASK_ENV=development && flask run --debug && deactivate'",
        shell=True,
    )


def run_blog() -> bool:
    """Run the blog.

    Returns:
        bool: Return False when fail to run the blog.
    """

    thread_frontend = threading.Thread(target=run_frontend)
    thread_backend = threading.Thread(target=run_backend)

    thread_frontend.start()
    thread_backend.start()

    thread_frontend.join()
    thread_backend.join()

    return True


def main():
    """The main function."""

    # If the command is build, build the virtual environment.
    if len(sys.argv) == 3 and sys.argv[1] == "build":
        print("[Easy-Blog]: Building the Easy-Blog environment...")
        linux_release_name = sys.argv[2]
        if build_environment(linux_release_name):
            print("[Easy-Blog]: Succeed to build the Easy-Blog environment.")
            print("[Easy-Blog]: You can run the blog by typing 'python eblog.py run'.")
        else:
            print("[Easy-Blog]: Fail to build the Easy-Blog environment.")

    # If the command is destroy, destroy the virtual environment.
    elif len(sys.argv) == 2 and sys.argv[1] == "destroy":
        print("[Easy-Blog]: Destroying the Easy-Blog environment...")
        if destroy_environment():
            print("[Easy-Blog]: Succeed to destroy the Easy-Blog environment.")
        else:
            print("[Easy-Blog]: Fail to destroy the Easy-Blog environment.")

    # If the command is run, run the blog.
    elif len(sys.argv) == 2 and sys.argv[1] == "run":
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
