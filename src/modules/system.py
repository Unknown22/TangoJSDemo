import platform
import re
import subprocess

from modules.operational_system import OperationalSystem


def get_local_os():
    if platform.system() == "Windows" and platform.release() == '10':
        return OperationalSystem.WINDOWS
    elif platform.system() == "Linux":
        try:
            check_system_process = subprocess.Popen(['lsb_release', '-ir'], stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
            out, err = check_system_process.communicate()
            return OperationalSystem.UBUNTU
        except FileNotFoundError:
            check_system_process = subprocess.Popen(['cat', '/etc/redhat-release'], stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
            out, err = check_system_process.communicate()
            return OperationalSystem.CENTOS


def check_system_compatibility():
    if platform.system() == "Windows" and (platform.release() == '10' or platform.release() == '8'):
        return True
    else:
        print("This script doesn't support your system. Check README")
        return False


def _get_version_main_number(result):
    return int(result.groups()[3].split('.')[0])


if __name__ == "__main__":
    print(check_system_compatibility())