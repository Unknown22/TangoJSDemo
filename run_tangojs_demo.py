import subprocess
from time import sleep


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def npm(*args, folder=None):
    npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder)
    return npm_process


if __name__ == "__main__":
    git("clone", "git://github.com/tangojs/tangojs-webapp-template")
    npm("install", folder="tangojs-webapp-template").communicate()

    npm("install", "--save", "tangojs-core", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-connector-local", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-web-components", folder="tangojs-webapp-template").communicate()

    server_process = npm("run", "server", folder="tangojs-webapp-template")
    sleep(3)
    browser = subprocess.Popen(['firefox'] + ['127.0.0.1:8081'])