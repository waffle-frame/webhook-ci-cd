from dotenv import dotenv_values
from flask import Flask, Response
from subprocess import PIPE, run

app = Flask(__name__)
config = dotenv_values(".env")


def build_clone_url() -> str:
    # Get index of "github.com" in the url
    index = config["TARGET_REPOSITORY"].find("github.com")

    url = "git clone " +\
        config["TARGET_REPOSITORY"][:index] + \
        config["YOUR_GITHUB_USERNAME"] + ":" + config["YOUR_GITHUB_TOKEN"] +\
        "@" + config["TARGET_REPOSITORY"][index:]

    # Example:
    #
    # git clone https://waffle-frame:ghp_trc..AFI@github.com/waffle-frame/clean-architecture-template

    return url


@app.route("/")
def webhook():
    # Use the system password to escalate privileges
    password = f'echo {config["SYSTEM_PASSWORD"]} | '

    # Change the directory and branch to the target ones
    cd_checkout = f'cd {config["TARGET_DIRECTORY"]} &&' + \
        password + f'sudo -S git checkout {config["TARGET_BRANCH"]} && '

    # Let's try to clone the repository to the target directory
    #
    # Additionally, we use superuser mode in case you need to perform an action
    # outside the home directory
    clone = run(
        password +
        # Clone the repository into the target folder
        f'sudo -S {build_clone_url()} {config["TARGET_DIRECTORY"]}',

        shell=True, stderr=PIPE, stdout=PIPE
    )
    print("Clone: ", clone.stderr.decode())

    # Pull changes from the target branch if such a folder already exists
    if "already exists" in clone.stderr.decode():
        # In this case, we do not need to add a token to the request, since the token
        # is already in the origin
        pull = run(
            cd_checkout +
            # Get updates
            f'sudo -S git pull origin {config["TARGET_BRANCH"]}',

            shell=True, stderr=PIPE, stdout=PIPE
        )
        print("Pull: ", pull.stderr.decode())

    # Start the build process
    build = run(
        cd_checkout +
        # Build!
        f'{config["BUILD_CMD"]}',

        shell=True, stderr=PIPE, stdout=PIPE
    )
    print("Build: ", build.stderr.decode())

    return Response(status=200)


if __name__ == '__main__':
    app.run(host="localhost", port=config["PORT"])
