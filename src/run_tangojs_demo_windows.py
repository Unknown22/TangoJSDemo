from system import check_system_compatibility


def _check_npm():
    pass


def _check_node():
    pass


def _check_firefox():
    pass


def _install_and_run():
    pass


def _check_requirements():
    requirements = []
    requirements.append(_check_npm())
    requirements.append(_check_node())
    requirements.append(_check_firefox())
    if False in requirements:
        return False
    return True

if __name__ == "__main__":
    if check_system_compatibility() and _check_requirements():
        print("OK")
        _install_and_run()
    else:
        print("You do not meet requirements.")