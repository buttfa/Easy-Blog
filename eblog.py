import sys  # Use 'sys' to obtain command-line parameters
from script.build import build_environment
from script.run import run_blog
from script.destroy import destroy_environment

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
