def merge(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    elif isinstance(a, dict) and isinstance(b, dict):
        for key in a:
            if not key in b:
                b[key] = a[key]
            else:
                b[key] = merge(a[key], b[key])
        return b
    else:
        return a


