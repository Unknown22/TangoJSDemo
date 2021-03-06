#!/usr/bin/env python3

import subprocess
import re
import sys

from .modules.firefox import check_and_update_firefox
from .modules.operational_system import OperationalSystem
from .modules.system import check_system_compatibility, get_local_os
from .modules.windows_runner import run_tangojsdemo_windows
from .modules.fixed_index_html import index_file_source, javascript_file_source


def git(*args, folder=None):
    return subprocess.Popen(['git'] + list(args), cwd=folder).communicate()


def npm(*args, folder=None, read_std=False):
    if read_std:
        npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        npm_process = subprocess.Popen(['npm'] + list(args), cwd=folder)
    return npm_process


def _install_and_run():
    out, err = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not 'tangojs-webapp-template' in out.decode():
        git("clone", "git://github.com/tangojs/tangojs-webapp-template")
        out, err = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not 'tangojs-webapp-template' in out.decode():
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
        except (KeyboardInterrupt, SystemExit):
            break
        message = line.lstrip().decode()
        print(message)
        address_regex = re.search(address_pattern, message)
        try:
            address = address_regex.groups()
            if not is_firefox_running:
                is_firefox_running = run_browser(address)
        except AttributeError:
            continue

def run_browser(address):
    try:
        subprocess.Popen(['firefox'] + [address[0] + address[1]] + [address[0] + address[1] + "/javascript.html"])
    except Exception:
        return False
    return True


def _check_requirements():
    requirements = []
    try:
        requirements.append(_check_npm())
    except FileNotFoundError:
        print("Couldn't find npm")
        return False
    try:
        requirements.append(_check_node())
    except FileNotFoundError:
        print("Couldn't find node")
        return False
    try:
        requirements.append(_check_firefox())
    except FileNotFoundError:
        print("Couldn't find firefox")
        return False
    if False in requirements:
        return False
    return True


def _check_firefox():
    return check_and_update_firefox(get_local_os())


def _check_node():
    try:
        node_version = _check_node_version()
        if int(node_version) < 6:
            if get_local_os() == OperationalSystem.UBUNTU or get_local_os() == OperationalSystem.CENTOS:
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
            else:
                return False
    except (KeyboardInterrupt, SystemExit):
        sys.exit(5)
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
        try:
            npm_install_answer = input("You don't have npm. Do you want to install it now? (y/N): ")
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)
        if npm_install_answer.lower() == 'y':
            try:
                if get_local_os() == OperationalSystem.UBUNTU:
                    npm_install = subprocess.Popen(['sudo', 'apt-get', 'install', 'npm'])
                    out, err = npm_install.communicate()
                elif get_local_os() == OperationalSystem.CENTOS:
                    download_npm = subprocess.Popen(['curl -s -L https://rpm.nodesource.com/setup_6.x'], shell=True)
                    out, err = download_npm.communicate()
                    npm_install = subprocess.Popen(['sudo', 'yum', '-y', 'install', 'nodejs'])
                    out, err = npm_install.communicate()
            except (KeyboardInterrupt, SystemExit):
                sys.exit(1)

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
    try:
        update_npm_answer = input("Do you want to do it now? (y/N): ")
        if update_npm_answer.lower() == 'y':
            print("npm update start")
            # npm_update = subprocess.Popen(['sudo', 'npm', 'install', '-g', 'npm'])
            npm_update = subprocess.Popen(['curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -'], shell=True)
            out, err = npm_update.communicate()
            npm_update_2 = subprocess.Popen(['sudo', 'apt-get', 'install', '-y', 'nodejs'])
            out, err = npm_update_2.communicate()
            if int(_check_npm_version()) >= 0:
                return True
            else:
                print("Something went wrong with upgrade.")
                return False
        else:
            return False
    except (KeyboardInterrupt, SystemExit):
        sys.exit(3)


def _fix_npm_symlink():
    try:
        symlink_answer = input("Path for node changed after upgrade. Do you want to fix it with symlink? (y/N) :")
        if symlink_answer.lower() == 'y':
            symlink_process = subprocess.Popen(['sudo', 'ln', '-s', '/usr/bin/nodejs', '/usr/bin/node'])
            out, err = symlink_process.communicate()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(4)


def _check_npm_version():
    npm_version_check = subprocess.Popen(['npm', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = npm_version_check.communicate()
    npm_version = out.decode('utf-8')
    if npm_version == '':
        return 0
    return npm_version[0]

def main():
    if get_local_os() == OperationalSystem.WINDOWS:
        run_tangojsdemo_windows()
    else:
        if check_system_compatibility() and _check_requirements():
            print("Compatibility and requirements: OK")
            try:
                _install_and_run()
            except (KeyboardInterrupt, SystemExit):
                sys.exit(6)
        else:
            print("You do not meet requirements.")

if __name__ == "__main__":
    main()
