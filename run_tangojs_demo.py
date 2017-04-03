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
    node_version_check = subprocess.Popen(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = node_version_check.communicate()
    node_version = out.decode('utf-8')
    if node_version == '':
        return 0
    return node_version[1]


def _check_npm():
    try:
        if 0 < int(_check_npm_version()) < 4:
            if not upgrade_npm():
                return False

        if int(_check_npm_version()) == 0:
            _fix_npm_symlink()

        if int(_check_npm_version()) >= 4:
            return True
    except FileNotFoundError:
        npm_install_answer = input("You don't have npm. Do you want to install it now? (y/N): ")
        if npm_install_answer.lower() == 'y':
            npm_install = subprocess.Popen(['sudo', 'apt-get', 'install', 'npm'])
            out, err = npm_install.communicate()

            if 0 < int(_check_npm_version()) < 4:
                if not upgrade_npm():
                    return False

            if int(_check_npm_version()) == 0:
                _fix_npm_symlink()

            if int(_check_npm_version()) >= 4:
                return True
            else:
                return False


def upgrade_npm():
    print("You must upgrade npm")
    update_npm_answer = input("Do you want to do it now? (y/N): ")
    if update_npm_answer.lower() == 'y':
        print("npm update start")
        npm_update = subprocess.Popen(['sudo', 'npm', 'install', '-g', 'npm'])
        out, err = npm_update.communicate()
        if int(_check_npm_version()) >= 0:
            return True
        else:
            print("Something went wrong with upgrade.")
            return False
    else:
        return False


def _fix_npm_symlink():
    symlink_answer = input("Path for node changed after upgrade. Do you want to fix it with symlink? (y/N) :")
    if symlink_answer.lower() == 'y':
        symlink_process = subprocess.Popen(['sudo', 'ln', '-s', '/usr/bin/nodejs', '/usr/bin/node'])
        out, err = symlink_process.communicate()


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