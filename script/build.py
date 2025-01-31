import subprocess  # Use 'subprocess' to execute shell commands
from script.config import venv_folder_path, db_folder_path
import os  # Use 'os' to determine whether the virtual environment folder exists
from sqlite3 import connect
from getpass import getpass
from hashlib import sha256

# System dependencies
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
    conn_db = connect(db_folder_path+"/blog.db")
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

