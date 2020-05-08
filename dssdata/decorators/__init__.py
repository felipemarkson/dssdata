from functools import wraps
from typing import Callable


def tools(func: Callable) -> Callable:
    """
    See [Creating your first tool](/tutorial/#creating-your-first-tool).

    Args:
        func:  A tool function

    Returns:
        The return of the tool function
    """

    @wraps(func)
    def wrapper(distSys, *args, **kwds):
        if distSys.dss.Circuit.Name() != distSys.name:
            distSys.init_sys()
        data = func(distSys, *args, **kwds)
        return data

    return wrapper


def actions(func: Callable) -> Callable:
    """
    See [Creating your first action](/tutorial/#creating-your-first-action).

    Args:
        func:  A action function
    """

    @wraps(func)
    def wrapper(distSys, *args, **kwds):
        if distSys.dss.Circuit.Name() != distSys.name:
            distSys.init_sys()
        func(distSys, *args, **kwds)

    return wrapper


def mode(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(distSys, *args, **kwds):
        if distSys.dss.Circuit.Name() != distSys.name:
            distSys.init_sys()
        data = func(distSys, *args, **kwds)
        distSys.init_sys()
        return data

    return wrapper
