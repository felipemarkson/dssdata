def pf_tools(func):
    def wrapper(distSys, *args, **kwds):
        if distSys.dss.Circuit.Name() != distSys.get_name():
            distSys.init_sys()
            # distSys.dss.Circuit.Enable(distSys.get_name())
        return func(distSys, *args, **kwds)

    return wrapper
