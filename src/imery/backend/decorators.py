

_pending_device_managers = []

def device_manager(obj):
    _pending_device_managers.append(obj)
    return obj
