#!/usr/bin/env python3

import subprocess
import re

from modules.firefox import check_and_update_firefox
from modules.operational_system import OperationalSystem
from modules.system import check_system_compatibility, get_local_os
from modules.windows_runner import run_tangojsdemo_windows


def git(*args, folder=None):
    subprocess.Popen(['git'] + list(args), cwd=folder).communicate()


def npm(*args, folder=None, read_std=False):
    if get_local_os() == OperationalSystem.UBUNTU:
        if read_std:
            npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder)
    elif get_local_os() == OperationalSystem.CENTOS:
        command = "su root -c 'npm " + str(' '.join(args) + "'")
        if read_std:
            npm_process = subprocess.Popen([command], cwd=folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            npm_process = subprocess.Popen([command], cwd=folder, shell=True)
    return npm_process


def _install_and_run():
    out, err = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not 'tangojs-webapp-template' in out.decode():
        git("clone", "git://github.com/tangojs/tangojs-webapp-template")
    npm("install", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-core", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-connector-local", folder="tangojs-webapp-template").communicate()
    npm("install", "--save", "tangojs-web-components", folder="tangojs-webapp-template").communicate()
    server_process = npm("run", "server", folder="tangojs-webapp-template", read_std=True)
    address_pattern = r'(http://\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:)(\d{2,4})'
    is_firefox_running = False
    while True:
        try:
            line = server_process.stdout.readline()
            if line != '':
                message = line.lstrip().decode()
                address_regex = re.search(address_pattern, message)
                address = address_regex.groups()
                print("Starting up http-server, serving ./")
                print("Available on:")
                print("    " + address[0] + address[1])
                print("Hit CTRL-C to stop the server")
                if not is_firefox_running:
                    is_firefox_running = run_browser(address)
        except (KeyboardInterrupt, SystemExit):
            print("\nShutting down server and browser")
            break
        except Exception:
            continue


def run_browser(address):
    subprocess.Popen(['firefox'] + [address[0] + address[1]])
    return True


def _check_requirements():
    requirements = []
    requirements.append(_check_npm())
    requirements.append(_check_node())
    requirements.append(_check_firefox())
    if False in requirements:
        return False
    return True


def _check_firefox():
    return check_and_update_firefox(get_local_os())


def _check_node():
    try:
        node_version = _check_node_version()
        if int(node_version) < 6:
            if get_local_os() == OperationalSystem.UBUNTU:
                node_update_answer = input("You need update node. Do you want to do it now? (y/N): ")
                if node_update_answer.lower() == 'y':
                    n_install_process = subprocess.Popen(['sudo', 'npm', 'install', '-g', 'n'])
                    out, err = n_install_process.communicate()
                    node_update_process = subprocess.Popen(['sudo', 'n', 'stable'])
                    out, err = node_update_process.communicate()
                    node_version = _check_node_version()
                    if int(node_version) < 6:
                        print("Something went wrong with node update. Try to do it manually and run this script again.")
                        return False
                    return True
            elif get_local_os() == OperationalSystem.CENTOS:
                node_update_answer = input("You need update node. Do you want to do it now? (y/N): ")
                if node_update_answer.lower() == 'y':
                    n_install_process = subprocess.Popen(['su root -c "npm install -g n"'], shell=True)
                    out, err = n_install_process.communicate()
                    node_update_process = subprocess.Popen(['su root -c"n stable"'], shell=True)
                    out, err = node_update_process.communicate()
                    node_version = _check_node_version()
                    if int(node_version) < 6:
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
        if 0 < int(_check_npm_version()) < 3:
            if not upgrade_npm():
                return False

        if int(_check_npm_version()) == 0:
            _fix_npm_symlink()

        if int(_check_npm_version()) >= 3:
            return True
    except FileNotFoundError:
        npm_install_answer = input("You don't have npm. Do you want to install it now? (y/N): ")
        if npm_install_answer.lower() == 'y':
            if get_local_os() == OperationalSystem.UBUNTU:
                npm_install = subprocess.Popen(['sudo', 'apt-get', 'install', 'npm'])
            elif get_local_os() == OperationalSystem.CENTOS:
                download_npm = subprocess.Popen(['curl -s -L https://rpm.nodesource.com/setup_6.x'], shell=True)
                out, err = download_npm.communicate()
                npm_install = subprocess.Popen(['su root -c "yum -y install nodejs"'], shell=True)
            out, err = npm_install.communicate()

            if 0 < int(_check_npm_version()) < 3:
                if not upgrade_npm():
                    return False

            if int(_check_npm_version()) == 0:
                _fix_npm_symlink()

            if int(_check_npm_version()) >= 3:
                return True
            else:
                return False
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
    if get_local_os() == OperationalSystem.WINDOWS:
        run_tangojsdemo_windows()
    else:
        if check_system_compatibility() and _check_requirements():
            print("Compatibility and requirements: OK")
            _install_and_run()
        else:
            print("You do not meet requirements.")