import subprocess
from time import sleep


def git(*args):
    out, err = subprocess.Popen(['git'] + list(args)).communicate()


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
    requirements.append(_check_node())
    if False in requirements:
        return False
    return True

def _check_node():
    try:
        node_version = _check_node_version()
        if int(node_version) < 7:
            node_update_answer = input("You need update node. Do you want to do it now? (y/N): ")
            if node_update_answer.lower() == 'y':
                n_install_process = subprocess.Popen(['sudo', 'npm', 'install', '-g', 'n'])
                out, err = n_install_process.communicate()
                node_update_process = subprocess.Popen(['sudo', 'n', 'stable'])
                out, err = node_update_process.communicate()
                node_version = _check_node_version()
                if int(node_version) < 7:
                    print("Something went wrong with node update. Try to do it manually and run this script again.")
                    return False
                return True
            else:
                return False
    except:
        print("Something went wrong with node check/update")
        return False


def _check_node_version():
    npm_version_check = subprocess.Popen(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = npm_version_check.communicate()
    npm_version = out.decode('utf-8')
    if npm_version == '':
        return 0
    return npm_version[1]


def _check_npm():
    npm_version = None

    try:
        npm_version = _check_npm_version()
    except FileNotFoundError:
        npm_install_answer = input("You don't have npm. Do you want to install it now? (y/N): ")
        if npm_install_answer.lower() == 'y':
            npm_install = subprocess.Popen(['sudo', 'apt-get', 'install', 'npm'])
            our, err = npm_install.communicate()

    if npm_version is None or npm_version == 0:
        try:
            npm_version = _check_npm_version()
            if npm_version == 0:
                symlink_answer = input("Path for node changed after upgrade. Do you want to fix it with symlink? (y/N) :")
                if symlink_answer.lower() == 'y':
                    symlink_process = subprocess.Popen(['sudo', 'ln', '-s', '/usr/bin/nodejs', '/usr/bin/node'])
                    out, err = symlink_process.communicate()
                    npm_version = _check_npm_version()
                else:
                    return False
        except FileNotFoundError:
            print("Something went wrong with npm install. Try to do it manually and run this script again.")
            return False

    if int(npm_version) < 4:
        print("You must upgrade npm and nodejs.")
        update_npm_answer = input("Do you want to do it now? (y/N): ")
        if update_npm_answer.lower() == 'y':
            print("npm update start")
            npm_update = subprocess.Popen(['sudo', 'npm', 'install', '-g', 'npm'])
            out, err = npm_update.communicate()
            if int(_check_npm_version()) >= 4:
                return True
            else:
                print("Something went wrong with upgrade.")
                return False
    else:
        return True


def _check_npm_version():
    npm_version_check = subprocess.Popen(['npm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = npm_version_check.communicate()
    npm_version = out.decode('utf-8')
    if npm_version == '':
        return 0
    return npm_version[0]


if __name__ == "__main__":
    if _check_requirements():
        print("OK")
        _install_and_run()
    else:
        print("You do not meet requirements.")