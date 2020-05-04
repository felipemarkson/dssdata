from functools import wraps


def pf_tools(func: callable) -> callable:
    """
    See [Create your tools](../gettingstart/createtools.md).

    Args:
        func:  A tool function

    Returns:
        The return of the tool function
    """

    @wraps(func)
    def wrapper(distSys, *args, **kwds):
        if distSys.dss.Circuit.Name() != distSys.name:
            distSys.init_sys()
            # distSys.dss.Circuit.Enable(distSys.get_name())
        return func(distSys, *args, **kwds)

    return wrapper
