import numbers
import math


class Vector3f:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.arr = [x, y, z]

    def __getitem__(self, item):
        return self.arr[item]

    def __add__(self, other):
        return Vector3f(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Vector3f(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, numbers.Real):
            return Vector3f(self.x * other, self.y * other, self.z * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return f'Vector3f({self.x},{self.y},{self.z})'

    def normalize(self):
        return normalize(self)

    def length(self):
        return math.sqrt(dot_product(self, self))


def dot_product(u, v):
    _v = u * v
    return _v.x + _v.y + _v.z


def length(u):
    return math.sqrt(dot_product(u, u))


def normalize(u):
    return (1 / length(u)) * u


def cross(u, v):
    x1, y1, z1 = u.x, u.y, u.z
    x2, y2, z2 = v.x, v.y, v.z
    return Vector3f(y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2)
