def add(a, b):
    return a + b

def complex_logic(x):
    # This function has a bug
    if x > 10:
        return x * 2
    else:
        return x / 0  # Potential error

