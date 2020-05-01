from functools import wraps


def pf_tools(func: callable):
    """[summary]

    :param func: [description]
    :type func: callable
    """

    @wraps(func)
    def wrapper(distSys, *args, **kwds):
        if distSys.dss.Circuit.Name() != distSys.get_name():
            distSys.init_sys()
            # distSys.dss.Circuit.Enable(distSys.get_name())
        return func(distSys, *args, **kwds)

    return wrapper
