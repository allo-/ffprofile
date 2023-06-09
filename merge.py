# recursively merge a and b, if element exists in both the value from a is used.
def merge(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    elif isinstance(a, dict) and isinstance(b, dict):
        c = b|a
        for key in c:
            if key in a and key in b:
                c[key] = merge(a[key],b[key])
        return c
    return a

