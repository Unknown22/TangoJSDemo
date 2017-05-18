import re
import subprocess
import urllib.request
import glob
import os
import sys

from modules.operational_system import OperationalSystem

FIREFOX_UBUNTU_CONFIG_FILE = "/home/*/.mozilla/firefox/*.default/"
FIREFOX_WINDOWS_CONFIG_FILE = '\\defaults\\pref\\firefox.js'
FIREFOX_CENTOS_CONFIG_FILE = '/home/*/.mozilla/firefox/*.default/'


def check_and_update_firefox(system=OperationalSystem.UBUNTU):
    try:
        if not _is_firefox_updated(system):
            firefox_update_answer = input(
                "Your Firefox version is too old or couldn't find it. Do you need to update/install it now? (y/N): ")
            if firefox_update_answer.lower() == 'y':
                _update_firefox(system)
                _is_firefox_updated(system)
            else:
                print("Script couldn't find firefox.")
                print("(maybe it is installed not in default location? if that so you can continue)")
                firefox_continue = input("Do you want to continue anyway? (y/N): ")
                if firefox_continue.lower() == 'y':
                    configure_firefox(system)
                    return True
        if not configure_firefox(system):
            continue_firefox = input("Couldn't configure firefox. Do you want to continue anyway? (y/N): ")
            if continue_firefox.lower() != 'y':
                return False
    except (KeyboardInterrupt, SystemExit):
        return False
    return _is_firefox_updated(system)


def _is_firefox_updated(system):
    firefox_ver = _get_firefox_version(system)
    if int(firefox_ver[0]) < 50:
        return False
    else:
        return True


def _update_firefox(system=OperationalSystem.UBUNTU):
    if system == OperationalSystem.UBUNTU:
        firefox_ppa = subprocess.Popen(['sudo', 'add-apt-repository', 'ppa:mozillateam/firefox-next'])
        firefox_ppa.communicate()
        apt_update = subprocess.Popen(['sudo', 'apt-get', 'update'])
        apt_update.communicate()
        firefox_update = subprocess.Popen(['sudo', 'apt-get', 'install', 'firefox'])
        firefox_update.communicate()
    elif system == OperationalSystem.WINDOWS:
        firefox_download_file = "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
        print("Downloading firefox installer")
        urllib.request.urlretrieve(firefox_download_file, "firefox-setup.exe")
        print("Running installation")
        firefox_installation = subprocess.Popen([r"firefox-setup.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        firefox_installation.communicate()
        return True
    elif system == OperationalSystem.CENTOS:
        status = 'not installed'
        try:
            firefox_update = subprocess.Popen(['sudo', 'yum', 'install', 'firefox'])
            out, err = firefox_update.communicate()
        except (KeyboardInterrupt, SystemExit):
            return False


def _get_firefox_version(system=OperationalSystem.UBUNTU):
    global FIREFOX_WINDOWS_CONFIG_FILE
    if system == OperationalSystem.UBUNTU or system == OperationalSystem.CENTOS:
        try:
            check_firefox = subprocess.Popen(['firefox', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = check_firefox.communicate()
            version_pattern = r"\d+\.*\d*\.*\d*"
            version_regex = re.search(version_pattern, out.decode())
            firefox_ver = version_regex.group().split('.')
            return firefox_ver
        except FileNotFoundError:
            return [0]

    elif system == OperationalSystem.WINDOWS:
        paths = [
            '%s:\\Program Files (x86)\\Mozilla Firefox',
            '%s:\\Program Files\\Mozilla Firefox'
        ]
        disks = ('C', 'D', 'E', 'F')
        for disk in disks:
            for path in paths:
                check_path = (path + '\\firefox.exe') % disk
                try:
                    firefox_version_check = subprocess.Popen([check_path, '-v'], stdout=subprocess.PIPE,
                                                             stderr=subprocess.PIPE,
                                                             shell=True)
                    out, err = firefox_version_check.communicate()
                    version_pattern = r"\d+\.*\d*\.*\d*"
                    version_regex = re.search(version_pattern, out.decode())
                    firefox_ver = version_regex.group().split('.')
                    FIREFOX_WINDOWS_CONFIG_FILE = (path + FIREFOX_WINDOWS_CONFIG_FILE) % disk
                    return firefox_ver
                except:
                    continue
        return [0]


def configure_firefox(system=OperationalSystem.UBUNTU):
    if system == OperationalSystem.UBUNTU:
        files = glob.glob(FIREFOX_UBUNTU_CONFIG_FILE)
        for file in files:
            firefox_config_file = file + 'user.js'
        with open(firefox_config_file, 'r') as content_file:
            content = content_file.read()
            option_1 = re.search(r"pref\(\"dom\.webcomponents\.enabled\",true\);", content)
            if option_1 is None:
                add_option_1 = subprocess.Popen(
                    'echo \'pref("dom.webcomponents.enabled",true);\' | tee -a ' + firefox_config_file,
                    shell=True)
                add_option_1.communicate()
            option_2 = re.search(r"pref\(\"layout\.css\.grid\.enabled\",true\);", content)
            if option_2 is None:
                add_option_2 = subprocess.Popen(
                    'echo \'pref("layout.css.grid.enabled",true);\' | tee -a ' + firefox_config_file,
                    shell=True)
                add_option_2.communicate()
        return True
    elif system == OperationalSystem.WINDOWS:
        option_1 = None
        option_2 = None
        try:
            with open(FIREFOX_WINDOWS_CONFIG_FILE, 'r') as content_file:
                content_file.seek(0)
                content = content_file.read()
                option_1 = re.search(r"pref\(\"dom\.webcomponents\.enabled\",true\);", content)
                option_2 = re.search(r"pref\(\"layout\.css\.grid\.enabled\",true\);", content)
        except FileNotFoundError:
            pass

        if option_1 is None or option_2 is None:
            try:
                with open(FIREFOX_WINDOWS_CONFIG_FILE, 'a+') as content_file:
                    if option_1 is None:
                        content_file.write('pref("dom.webcomponents.enabled",true);\n')
                    if option_2 is None:
                        content_file.write('pref("layout.css.grid.enabled",true);\n')
                return True
            except PermissionError:
                print(
                    "Script have not permission to change firefox settings. Run this script again with administrator privilages or follow 'firefox.txt' in readme folder in this project")
                return False
            except FileNotFoundError:
                print(
                    "Couldn't find firefox settings file. If you have already Firefox installed follow 'firefox.txt' in readme folder in this project.")
                return False
        else:
            return True
    elif system == OperationalSystem.CENTOS:
        option_1 = None
        option_2 = None
        files = glob.glob(FIREFOX_CENTOS_CONFIG_FILE)
        for file in files:
            firefox_config_file = file + 'user.js'
        try:
            with open(firefox_config_file, 'r') as content_file:
                content_file.seek(0)
                content = content_file.read()
                option_1 = re.search(r"pref\(\"dom\.webcomponents\.enabled\",true\);", content)
                option_2 = re.search(r"pref\(\"layout\.css\.grid\.enabled\",true\);", content)
        except FileNotFoundError:
            pass
        if option_1 is None or option_2 is None:
            try:
                with open(firefox_config_file, 'a+') as content_file:
                    if option_1 is None:
                        add_option_1 = subprocess.Popen(
                            'echo \'pref("dom.webcomponents.enabled",true);\' | tee -a "' + firefox_config_file + '"',
                            shell=True)
                        add_option_1.communicate()
                    if option_2 is None:
                        add_option_2 = subprocess.Popen(
                            'echo \'pref("layout.css.grid.enabled",true);\' | tee -a "' + firefox_config_file + '"',
                            shell=True)
                        add_option_2.communicate()
                return True
            except PermissionError:
                print(
                    "Script have not permission to change firefox settings. Run this script again with administrator privilages or follow 'firefox.txt' in readme folder in this project")
                return False
            except FileNotFoundError:
                print(
                    "Couldn't find firefox settings file. If you have already Firefox installed follow 'firefox.txt' in readme folder in this project.")
                return False
        else:
            return True
