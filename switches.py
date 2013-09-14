class case:
    def __init__(self, value, function):
        self.val=value
        self.func=function

def switch(target, *cases, default=None):
    """(target, *cases, default=None)"""
    for CASE in cases:
        if(target==CASE.val):
            return CASE.func()
    if(type(default)==type(switch)):
        return default()
    else:
        return default
