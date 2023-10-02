

def cart_store(values, value):
    if len(values) == 0:
        values = value
    else:
        values.append(value)

    return values

print(cart_store([[1, 3], [3, 5]], [3,5]))