import os  # Use 'os' to determine whether the virtual environment folder exists
import subprocess  # Use 'subprocess' to execute shell commands
import sys  # Use 'sys' to obtain command-line parameters
import threading
from sqlite3 import connect
from getpass import getpass
from hashlib import sha256

# The path of the python virtual environment folder.
venv_folder_path = "backend/venv"
# The path of the database folder.
db_folder_path = "backend/db"
# system_de
system_dependencies = {
    "centos": {
        "node.js": "sudo yum -y install nodejs",
        "gcc": "sudo yum -y install gcc",
        "python3-devel": "sudo yum -y install python3-devel",
    }
}


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


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_db():
    # Connect to the database.
    conn_db = connect("backend/db/blog.db")
    conn_db.row_factory = (
        dict_factory  # Set the cursor to return the result as a dictionary.
    )
    cursor_db = conn_db.cursor()

    # Create tables.
    cursor_db.execute("""
        create table if not exists user (
            user_id integer primary key autoincrement,
            role text not null,

            name text not null,
                      
            email text not null unique,
            password text not null,
                      
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor_db.execute("""
        create table if not exists post (
            post_id integer primary key autoincrement,
            
            title text not null,
            author text not null,
            content text not null,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor_db.execute("""
        create table if not exists comment (
            comment_id integer primary key autoincrement,
            
            user_id integer not null,
            post_id integer not null,
            content text not null,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      
            foreign key(user_id) references user(user_id),
            foreign key(post_id) references post(post_id)
        )
    """)

    # Check if there is blogger information in the user table.
    cursor_db.execute("SELECT * FROM user WHERE role='blogger'")
    blogger_info = cursor_db.fetchone()
    if blogger_info is None:
        print(
            "[Easy-Blog:build]: There is no blogger information in the user table. Please write the blogger information."
        )

        # Get blogger's name
        blogger_user_name = input("Please input the name: ")

        # Get blogger's email
        blogger_user_email = input("Please input the email: ")

        # Get blogger's password
        blogger_user_password_first = getpass("Please input the password: ")
        blogger_user_password_second = getpass("Please input the password again: ")
        while blogger_user_password_first != blogger_user_password_second:
            blogger_user_password_first = getpass(
                "The passwords do not match. Please input the password again: "
            )
            blogger_user_password_second = getpass("Please input the password again: ")
        blogger_user_password = blogger_user_password_first

        # Write the blogger information into the user table.
        cursor_db.execute(
            f"insert into user(role, name, email, password) values('blogger', '{blogger_user_name}', '{blogger_user_email}', '{sha256(blogger_user_password.encode()).hexdigest()}')"
        )
        conn_db.commit()
        print("[Easy-Blog:build]: Succeed to write the blogger information.")


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

    init_db()

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


def replace_line_with_prefix(file_path, old_prefix, new_line):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if line.startswith(old_prefix):
            modified_lines.append(new_line + "\n")
        else:
            modified_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(modified_lines)


def configure_proxy(api_url):
    replace_line_with_prefix(
        "frontend/vite.config.js", "        target", f"        target: '{api_url}',"
    )


def run_frontend():
    """Run the frontend."""

    subprocess.run(
        f"cd frontend && npx vite --host",
        shell=True,
    )


def run_backend():
    """Run the backend."""
    subprocess.run(
        f"bash -c 'source {venv_folder_path}/bin/activate && export FLASK_APP=backend/blog && export FLASK_ENV=development && flask run --debug --host='0.0.0.0' && deactivate'",
        shell=True,
    )


def run_blog(pos: str, mode: str) -> bool:
    """Run the blog.

    Returns:
        bool: Return False when fail to run the blog.
    """

    # If running locally, configure the proxy IP to 127.0.0.1.
    if pos == "local":
        configure_proxy("http://127.0.0.1:5000")

    # If it is running remotely, configure the proxy IP as a public IP.
    elif pos == "remote":
        process = subprocess.Popen(
            "curl ifconfig.me",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        server_ip, stderr = process.communicate()

        with open("frontend/.env", "w") as env_dev:
            env_dev.write(f"VITE_EBLOG_API_URL=/api")

        configure_proxy(f"http://{server_ip}:5000")

    else:
        print("[Easy-Blog]: The position is not supported.")
        return False

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
    elif len(sys.argv) >= 2 and sys.argv[1] == "run":

        # The default target_pos and target_made.
        target_pos = "local"
        target_mode = "development"

        # Update target_pos and target_made based on command-line parameters.
        for arg in sys.argv[2:]:
            if arg == "--local":
                target_pos = "local"
            elif arg == "--remote":
                target_pos = "remote"
            else:
                print("[Easy-Blog]: Unknown command-line parameter: " + arg + ".")
                exit(1)

        print("[Easy-Blog]: Running the blog...")
        run_blog(target_pos, target_mode)

    # If the command is invalid, print an error message.
    else:
        print("[Easy-Blog]: Invalid command.")


if __name__ == "__main__":
    main()
