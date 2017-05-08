import subprocess
import urllib.request
from time import sleep
import re

from modules.firefox import check_and_update_firefox
from modules.operational_system import OperationalSystem
from modules.system import check_system_compatibility


def git(*args):
    out, err = subprocess.Popen(['git'] + list(args), shell=True).communicate()


def npm(*args, folder=None, read_std=False):
    if read_std:
        npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder, shell=True)
    return npm_process


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
    return check_and_update_firefox(OperationalSystem.WINDOWS)


def _install_and_run():
    git("clone", "git://github.com/tangojs/tangojs-webapp-template")
    npm("install", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-core", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-connector-local", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-web-components", folder="tangojs-webapp-template").communicate()
    server_process = npm("run", "server", folder="tangojs-webapp-template", read_std=True)
    address_pattern = r'(http://\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:)(\d{2,4})'
    is_firefox_running = False
    while True:
        line = server_process.stdout.readline()
        if line != '':
            message = line.lstrip().decode()
            address_regex = re.search(address_pattern, message)
            try:
                address = address_regex.groups()
                print("Starting up http-server, serving ./")
                print("Available on:")
                print("    " + address[0] + address[1])
                print("Hit CTRL-C to stop the server")
                if not is_firefox_running:
                    is_firefox_running = run_browser(address)
            except (KeyboardInterrupt, SystemExit):
                print("\nShutting down server")
                break
            except:
                continue
    run_browser(address)


def run_browser(address):
    browser_running = False
    paths = [
        '%s:\\Program Files (x86)\\Mozilla Firefox',
        '%s:\\Program Files\\Mozilla Firefox'
    ]
    disks = ('C', 'D', 'E', 'F')
    for disk in disks:
        for path in paths:
            check_path = (path + '\\firefox.exe') % disk
            try:
                firefox_version_check = subprocess.Popen([check_path, address[0] + address[1]], stdout=subprocess.PIPE,
                                                         stderr=subprocess.PIPE,
                                                         shell=False)
                out, err = firefox_version_check.communicate()
                browser_running = True
            except:
                continue
    if not browser_running:
        print("Couldn't find Firefox. If you already have Firefox installed open address given above from server [default: 127.0.0.1:8080]")


def _check_requirements_windows():
    requirements = []
    requirements.append(_check_npm())
    requirements.append(_check_node())
    requirements.append(_check_firefox())
    if False in requirements:
        return False
    return True


def run_tangojsdemo_windows():
    if check_system_compatibility() and _check_requirements_windows():
        print("OK")
        _install_and_run()
    else:
        print("You do not meet requirements.")

if __name__ == "__main__":
    run_tangojsdemo_windows()
