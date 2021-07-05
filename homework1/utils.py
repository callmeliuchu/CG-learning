import random
from vector import Vector3f


def random_double():
    return random.random()


def random_unit_vector():
    return Vector3f(random_double(),random_double(),random_double()).normalize()
