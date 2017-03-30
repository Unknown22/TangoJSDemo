import subprocess
from time import sleep


def git(*args):
    return subprocess.check_call(['git'] + list(args))


def npm(*args, folder=None):
    npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder)
    return npm_process


def _install_and_run():
    git("clone", "git://github.com/tangojs/tangojs-webapp-template")
    npm("install", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-core", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-connector-local", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-web-components", folder="tangojs-webapp-template").communicate()
    server_process = npm("run", "server", folder="tangojs-webapp-template")
    sleep(3)
    browser = subprocess.Popen(['firefox'] + ['127.0.0.1:8081'])


def _check_requirements():
    requirements = []
    requirements.append(_check_npm())
    if False in requirements:
        return False
    return True


def _check_npm():
    npm_version = _check_npm_version()
    if int(npm_version[0]) < 4:
        print("You must upgrade npm and nodejs.")
        update_npm_answer = input("Do you want to do it now? (y/N): ")
        if update_npm_answer.lower() == 'y':
            print("npm update start")
            npm_update = subprocess.Popen(['sudo', 'npm', 'install', '-g', 'npm'])
            out, err = npm_update.communicate()
            if int(_check_npm_version()[0]) >= 4:
                return True
            else:
                print("Something went wrong with upgrade.")
    return False


def _check_npm_version():
    npm_version_check = subprocess.Popen(['npm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = npm_version_check.communicate()
    npm_version = out.decode('utf-8')
    return npm_version


if __name__ == "__main__":
    if _check_requirements():
        print("OK")
        pass
    else:
        print("You do not meet requirements.")
        # _install_and_run()