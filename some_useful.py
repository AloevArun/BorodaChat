def square_trapecia_1(a=0, b=0, h=0):
    s = 0.5 * h * (a + b)
    return f'square = {s}'


def square_trapecia_2(**kwargs):
    a = kwargs.pop('a', 0)
    b = kwargs.pop('b', 0)
    h = kwargs.pop('h', 0)
    assert not kwargs, f'Unknown params {kwargs}'

    s = 0.5 * h * (a + b)
    return f'square = {s}'


print(square_trapecia_1())
print(square_trapecia_2())
