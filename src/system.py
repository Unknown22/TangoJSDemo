import os
import platform
import subprocess
import re


def check_system_compatibility():
    if platform.system() == "Windows" and platform.release() == '10':
        return True
    elif platform.system() == "Linux":
        check_system_process = subprocess.Popen(['lsb_release', '-ir'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = check_system_process.communicate()
        result = re.search(r'(Distributor ID:\s*)(\S*)\s(Release:\s*)(\d*\.*\d*)', out.decode())
        if result.groups()[1] == "Ubuntu" and _get_version_main_number(result) < 12:
            print("Your system can't run it. You should consider update for your system.")
            return False
        elif result.groups()[1] == "Ubuntu" and _get_version_main_number(result) >= 12:
            return True
        else:
            return False
    else:
        print("This script doesn't support your system.")
        return False


def _get_version_main_number(result):
    return int(result.groups()[3].split('.')[0])


if __name__ == "__main__":
    print(check_system_compatibility())