import subprocess
import re

FIREFOX_CONFIG_FILE = "/etc/firefox/syspref.js"


def check_and_update_firefox():
    if not _is_firefox_updated():
        firefox_update_answer = input("Your Firefox version is too old. Do you need to update it now? (y/N): ")
        if firefox_update_answer.lower() == 'y':
            _update_firefox()
    return _is_firefox_updated()


def _is_firefox_updated():
    firefox_ver = _get_firefox_version()
    if int(firefox_ver[0]) < 51:
        return False
    else:
        return True


def _update_firefox():
    firefox_ppa = subprocess.Popen(['sudo', 'add-apt-repository', 'ppa:mozillateam/firefox-next'])
    firefox_ppa.communicate()
    apt_update = subprocess.Popen(['sudo', 'apt-get', 'update'])
    apt_update.communicate()
    firefox_update = subprocess.Popen(['sudo', 'apt-get', 'install', 'firefox'])
    firefox_update.communicate()


def _get_firefox_version():
    check_firefox = subprocess.Popen(['firefox', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = check_firefox.communicate()
    version_pattern = r"\d+\.*\d*\.*\d*"
    version_regex = re.search(version_pattern, out.decode())
    firefox_ver = version_regex.group().split('.')
    return firefox_ver


def configure_firefox(config_file=FIREFOX_CONFIG_FILE):
    with open(config_file, 'r') as content_file:
        content = content_file.read()
        option_1 = re.search(r"pref\(\"dom\.webcomponents\.enabled\",true\);", content)
        if option_1 is None:
            add_option_1 = subprocess.Popen(
                'echo \'pref("dom.webcomponents.enabled",true);\' | sudo tee -a ' + config_file,
                shell=True)
            add_option_1.communicate()
        option_2 = re.search(r"pref\(\"layout\.css\.grid\.enabled\",true\);", content)
        if option_2 is None:
            add_option_2 = subprocess.Popen(
                'echo \'pref("layout.css.grid.enabled",true);\' | sudo tee -a ' + config_file,
                shell=True)
            add_option_2.communicate()


if __name__ == "__main__":
    check_and_update_firefox()
    configure_firefox()
