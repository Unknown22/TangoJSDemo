import platform
import re
import subprocess

from modules.operational_system import OperationalSystem


def get_local_os():
    if platform.system() == "Windows" and platform.release() == '10':
        return OperationalSystem.WINDOWS
    elif platform.system() == "Linux":
        if _check_ubuntu_compatibility():
            return OperationalSystem.UBUNTU
        elif _check_centos_compatibility():
            return OperationalSystem.CENTOS


def check_system_compatibility():
    if platform.system() == "Windows" and (platform.release() == '10' or platform.release() == '8'):
        return True
    elif platform.system() == "Linux":
        if _check_ubuntu_compatibility() or _check_centos_compatibility():
            return True
    else:
        print("This script doesn't support your system. Check README")
        return False


def _check_centos_compatibility():
    try:
        check_system_process = subprocess.Popen(['rpm', '-q', 'centos-release'], stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
        out, err = check_system_process.communicate()
        result_system = re.search(r'centos', out.decode())
        result_version = re.search(r'el7', out.decode())
        if result_system is None or result_version is None:
            return False
        if result_system.group() == "centos" and result_version.group() == 'el7':
            return True
    except Exception:
        return False


def _check_ubuntu_compatibility():
    try:
        check_system_process = subprocess.Popen(['lsb_release', '-ir'], stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
        out, err = check_system_process.communicate()
        result = re.search(r'(Distributor ID:\s*)(\S*)\s(Release:\s*)(\d*\.*\d*)', out.decode())
        if result is None:
            return False
        if result.groups()[1] == "Ubuntu" and _get_version_main_number(result) < 12:
            print("Your system can't run it. You should consider update for your system.")
            return False
        elif result.groups()[1] == "Ubuntu" and _get_version_main_number(result) >= 12:
            return True
        else:
            return False
    except Exception:
        return False


def _get_version_main_number(result):
    return int(result.groups()[3].split('.')[0])


if __name__ == "__main__":
    print(check_system_compatibility())