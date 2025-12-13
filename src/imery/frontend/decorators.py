

_pending_widgets = []

def widget(obj):
    _pending_widgets.append(obj)
    return obj
