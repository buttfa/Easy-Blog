import subprocess  # Use 'subprocess' to execute shell commands
import threading
from script.config import venv_folder_path

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
