from importlib import import_module


def is_package_installed(package):
    """ return true if all packages in "package" are installed """
    if isinstance(package, (list, tuple)):
        installed = [p for p in package if is_package_installed(p)]
        return len(installed) == len(package)
    try:
        import_module(package)
        return True
    except ImportError:
        return False
