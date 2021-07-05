from vector import dot_product
from utils import random_unit_vector

class HitRecord:

    def __init__(self,is_hit,hit_point=None,normal=None,closest_far=None,ray_dir=None):
        self.is_hit = is_hit
        self.hit_point = hit_point
        self.normal = normal
        self.closest_far = closest_far
        if is_hit:
            self.front = False
            if self.normal:
                self.front = dot_product(self.normal,ray_dir) < 0
                if not self.front:
                    self.normal = -self.normal
            self.reflect = self.normal + random_unit_vector()
