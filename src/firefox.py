import subprocess
import re
import urllib.request
from operational_system import OperationalSystem

FIREFOX_UBUNTU_CONFIG_FILE = "/etc/firefox/syspref.js"
FIREFOX_WINDOWS_CONFIG_FILE = '\\defaults\\pref\\firefox.js'


def check_and_update_firefox(system=OperationalSystem.UBUNTU):
    if not _is_firefox_updated(system):
        firefox_update_answer = input("Your Firefox version is too old or couldn't find it. Do you need to update/install it now? (y/N): ")
        if firefox_update_answer.lower() == 'y':
            _update_firefox(system)
            _is_firefox_updated(system)
        else:
            print("Script couldn't find firefox.")
            print("(maybe it is installed not in default location? if that so you can continue)")
            firefox_continue = input("Do you want to continue anyway? (y/N)")
            if firefox_continue.lower() == 'y':
                configure_firefox(system)
                return True
    configure_firefox(system)
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


def _get_firefox_version(system=OperationalSystem.UBUNTU):
    global FIREFOX_WINDOWS_CONFIG_FILE
    if system == OperationalSystem.UBUNTU:
        check_firefox = subprocess.Popen(['firefox', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = check_firefox.communicate()
        version_pattern = r"\d+\.*\d*\.*\d*"
        version_regex = re.search(version_pattern, out.decode())
        firefox_ver = version_regex.group().split('.')
        return firefox_ver
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
                    firefox_version_check = subprocess.Popen([check_path, '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
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
        with open(FIREFOX_UBUNTU_CONFIG_FILE, 'r') as content_file:
            content = content_file.read()
            option_1 = re.search(r"pref\(\"dom\.webcomponents\.enabled\",true\);", content)
            if option_1 is None:
                add_option_1 = subprocess.Popen(
                    'echo \'pref("dom.webcomponents.enabled",true);\' | sudo tee -a ' + FIREFOX_UBUNTU_CONFIG_FILE,
                    shell=True)
                add_option_1.communicate()
            option_2 = re.search(r"pref\(\"layout\.css\.grid\.enabled\",true\);", content)
            if option_2 is None:
                add_option_2 = subprocess.Popen(
                    'echo \'pref("layout.css.grid.enabled",true);\' | sudo tee -a ' + FIREFOX_UBUNTU_CONFIG_FILE,
                    shell=True)
                add_option_2.communicate()
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
            except PermissionError:
                print("Script have not permission to change firefox settings. Run this script again with administrator privilages or follow 'firefox.txt' in readme folder in this project")
            except FileNotFoundError:
                print(
                    "Couldn't find firefox settings file. If you have already Firefox installed follow 'firefox.txt' in readme folder in this project.")
