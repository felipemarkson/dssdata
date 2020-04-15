def pf_tools(func):
    def wrapper(distSys, *args):
        if distSys.dss.Circuit.Name() != distSys.get_name():
            distSys.compile()
            # distSys.dss.Circuit.Enable(distSys.get_name())
        return func(distSys, *args)
    return wrapper
