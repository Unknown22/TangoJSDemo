import subprocess


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def npm(*args, folder=None):
    print(folder)
    npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder)
    return npm_process.communicate()


if __name__ == "__main__":
    git("clone", "git://github.com/tangojs/tangojs-webapp-template")
    npm("install", "--save", "tangojs-core", folder="tangojs-webapp-template")
    npm("install", "--save", "tangojs-connector-local", folder="tangojs-webapp-template")
    npm("install", "--save", "tangojs-web-components", folder="tangojs-webapp-template")