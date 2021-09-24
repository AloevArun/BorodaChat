"""
lst = [i**2 for i in range(10)]
gen = (i**2 for i in range(10))


def square(n):
    for i in range(1, n + 1):
        yield i**2


g = square(10)
print(iter(g))
"""


# 1. Exceptions
# Polymorphism
# magic methods 2-3 pcs

class FuelNotEnoughException(Exception):
    def __init__(self, ex, name):
        self.ex = ex
        self.name = name


class Car:
    grad = '10C'

    def __init__(self, vendor: str, model: str, fuel: int = 0, fuel_per_dist: int = 0):
        self.vendor = vendor
        self._model = model
        self.fuel = fuel
        self.fuel_per_dist = fuel_per_dist

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def weather(cls):
        return cls.grad

    @property
    def max_distance(self):
        return self.fuel / self.fuel_per_dist

    def dist_check(self, distance: int):
        if self.max_distance > distance:
            raise FuelNotEnoughException('Does not enough fuel', name="Fuel")


class BMW(Car):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(args)


if __name__ == '__main__':
    bmw = BMW('BMW', 'x5', 500, fuel_per_dist=10)
    print(Car.weather())
