from glob import glob
from os.path import basename, dirname, isfile

from DumprXBot import LOGGER


def list_all_modules():
    mod_paths = glob(f"{dirname(__file__)}/*.py")
    all_modules = [
        basename(files)[:-3]
        for files in mod_paths
        if isfile(files) and files.endswith(".py") and not files.endswith("__init__.py")
    ]
    return all_modules


ALL_MODULES = list_all_modules()
LOGGER.info(f"Modules to load: {str(ALL_MODULES)}")
