import os
import inspect

SOLUTION_NAME = "clarity-ext"


def get_package_abs_path():
    abspath = os.path.abspath(inspect.stack()[0][1])
    currentdir = os.path.dirname(abspath)
    path_head, _ = currentdir.split(SOLUTION_NAME, 1)
    return os.path.join(path_head, SOLUTION_NAME)
