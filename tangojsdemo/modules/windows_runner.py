import subprocess
import urllib.request
import re
import sys

from .firefox import check_and_update_firefox
from .operational_system import OperationalSystem
from .system import check_system_compatibility
from .fixed_index_html import index_file_source, javascript_file_source


def git(*args, folder=None):
    subprocess.Popen(['git'] + list(args), shell=True, cwd=folder).communicate()


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
    out, err = subprocess.Popen(['dir'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    if not b'tangojs-webapp-template' in out:
        git("clone", "git://github.com/tangojs/tangojs-webapp-template")
        out, err = subprocess.Popen(['dir'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if not b'tangojs-webapp-template' in out:
            print("Couldn't clone tangojs-webapp-template folder. Do you have internet connection?")
            return
    npm("install", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-core", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-connector-local", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-web-components", folder="tangojs-webapp-template").communicate()
    index_file = open('tangojs-webapp-template/index.html', 'w')
    index_file.write(index_file_source)
    index_file.close()
    js_file = open('tangojs-webapp-template/javascript.html', 'w')
    js_file.write(javascript_file_source)
    js_file.close()
    server_process = npm("run", "server", folder="tangojs-webapp-template", read_std=True)
    address_pattern = r'(http://\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:)(\d{2,4})'
    is_firefox_running = False
    while True:
        try:
            line = server_process.stdout.readline()
            if line != '':
                message = line.lstrip().decode()
                print(message)
                address_regex = re.search(address_pattern, message)
                address = address_regex.groups()
                if not is_firefox_running:
                    is_firefox_running = run_browser(address)
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            continue


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
                firefox_version_check = subprocess.Popen([check_path,
                                                          address[0] + address[1],
                                                          address[0] + address[1] + "/javascript.html"],
                                                         stdout=subprocess.PIPE,
                                                         stderr=subprocess.PIPE,
                                                         shell=False)
                browser_running = True
                return True
            except:
                continue
    if not browser_running:
        print("Couldn't find Firefox. If you already have Firefox installed open address given above [default: 127.0.0.1:8080]")
    return True


def _check_requirements_windows():
    requirements = []
    try:
        requirements.append(_check_npm())
        requirements.append(_check_node())
        requirements.append(_check_firefox())
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    if False in requirements:
        return False
    return True


def run_tangojsdemo_windows():
    if check_system_compatibility() and _check_requirements_windows():
        print("Compatibility and requirements: OK")
        try:
            _install_and_run()
        except (KeyboardInterrupt, SystemExit):
            sys.exit(2)
    else:
        print("You do not meet requirements.")

if __name__ == "__main__":
    run_tangojsdemo_windows()
