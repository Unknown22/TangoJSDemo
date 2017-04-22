from system import check_system_compatibility
import subprocess
import urllib.request
import os


def _check_npm_version():
    npm_version_check = subprocess.Popen(['npm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = npm_version_check.communicate()
    npm_version = out.decode('utf-8')
    if err.decode() != '':
        return -1
    if npm_version == '':
        return 0
    return npm_version[0]


def upgrade_npm():
    try:
        print("Downloading nodejs/npm intallator")
        node_installator = 'node-v6.10.2-x64.msi'
        urllib.request.urlretrieve('https://nodejs.org/dist/v6.10.2/node-v6.10.2-x64.msi', node_installator)
        print("Running installation")
        subprocess.call('msiexec /i %s /qr' % node_installator, shell=True)
        return True
    except:
        print("Problem occured while installing nodejs")
        return False


def _check_npm():
    try:
        if int(_check_npm_version()) == -1:
            npm_install_answer = input("You don't have npm. Do you want to install it now? (y/N): ")
            if npm_install_answer.lower() == 'y':
                if not upgrade_npm():
                    return False

                if int(_check_npm_version()) == -1:
                    print(
                        'If you installed node you have to restart command line to reload envs and run this script again.')
                    exit(0)

        if int(_check_npm_version()) >= 3:
            return True
        else:
            return False
    except FileNotFoundError:
        npm_install_answer = input("You don't have npm. Do you want to install it now? (y/N): ")
        if npm_install_answer.lower() == 'y':
            upgrade_npm()

            if int(_check_npm_version()) == -1:
                if not upgrade_npm():
                    return False

            if int(_check_npm_version()) == -1:
                print(
                    'If you installed node you have to restart command line to reload envs. Then run this script again.')
                exit(0)

        if int(_check_npm_version()) >= 3:
            return True
        else:
            return False


def _check_node_version():
    node_version_check = subprocess.Popen(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = node_version_check.communicate()
    node_version = out.decode()
    if err.decode() != '':
        return -1
    if node_version == '':
        return 0
    return node_version[1]


def _check_node():
    try:
        node_version = _check_node_version()
        if int(node_version) < 6:
            print("Your node version is too low. Try to uninstall old one and run this script again.")
            exit(0)
        else:
            return True
    except:
        print("Something went wrong with node check")
        return False


def _check_firefox():
    pass


def _install_and_run():
    pass


def _check_requirements():
    requirements = []
    requirements.append(_check_npm())
    requirements.append(_check_node())
    requirements.append(_check_firefox())
    print(requirements)
    if False in requirements:
        return False
    return True


if __name__ == "__main__":
    if check_system_compatibility() and _check_requirements():
        print("OK")
        _install_and_run()
    else:
        print("You do not meet requirements.")
