def str2float(x, default=None):
    try:
        return float(x)
    except:
        return default


def str2int(x, default=None):
    try:
        return int(x)
    except:
        return default
