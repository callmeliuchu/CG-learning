import numbers
import math


class Vector2f:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arr = [x, y]

    def __getitem__(self, item):
        return self.arr[item]

    def __add__(self, other):
        return Vector2f(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Vector2f(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Vector2f):
            return Vector2f(self.x * other.x, self.y * other.y)
        elif isinstance(other, numbers.Real):
            return Vector2f(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return f'Vector3f({self.x},{self.y})'

    def normalize(self):
        return normalize(self)

    def length(self):
        return math.sqrt(dot_product(self, self))


def dot_product(u, v):
    _v = u * v
    return _v.x + _v.y


def length(u):
    return math.sqrt(dot_product(u, u))


def normalize(u):
    return (1 / length(u)) * u
