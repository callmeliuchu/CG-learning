from utils import random_unit_vector,reflect
from vector import dot_product

class Material:

    def scatter(self,hit_record):
        pass


class Lambertian(Material):

    def __init__(self,color):
        self.albedo = color

    def scatter(self,hit_record):
        normal = hit_record.normal
        out_out_light_dir = normal + random_unit_vector()
        hit_record.set_out_light_dir(out_out_light_dir)
        hit_record.set_attenuation(self.albedo)
        return True


class Metal(Material):

    def __init__(self,color,fuzz):
        self.albedo = color
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self,hit_record):
        ray_in = hit_record.ray_direct
        normal = hit_record.normal.normalize()
        out_out_light_dir = reflect(ray_in,normal) + self.fuzz*random_unit_vector()
        hit_record.set_out_light_dir(out_out_light_dir)
        hit_record.set_attenuation(self.albedo)
        return True