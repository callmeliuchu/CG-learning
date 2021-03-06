import math

from utils import random_unit_vector, reflect, refract
from vector import Vector3f as Color
from vector import dot_product


class Material:

    def scatter(self, hit_record):
        pass

    def emitted(self, u, v, p):
        return Color(0, 0, 0)


class Lambertian(Material):

    def __init__(self, color_texture):
        self.color_texture = color_texture

    def scatter(self, hit_record):
        normal = hit_record.normal
        out_out_light_dir = normal + random_unit_vector()
        hit_record.set_out_light_dir(out_out_light_dir)
        u, v = hit_record.uv
        albedo = self.color_texture.value(u, v, hit_record.p)
        hit_record.set_attenuation(albedo)


class Metal(Material):

    def __init__(self, color, fuzz):
        self.albedo = color
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, hit_record):
        ray_in = hit_record.ray_direct
        normal = hit_record.normal.normalize()
        out_light_dir = reflect(ray_in, normal) + self.fuzz * random_unit_vector()
        hit_record.set_out_light_dir(out_light_dir)
        hit_record.set_attenuation(self.albedo)


class Dielectric(Material):

    def __init__(self, ir):
        self.ir = ir

    def scatter(self, hit_record):
        color = Color(1, 1, 1)
        theta = self.ir if hit_record.front else 1 / self.ir
        ray_in = hit_record.ray_direct
        normal = hit_record.normal.normalize()
        cos = min(dot_product(ray_in.normalize(), normal), 1)
        sin = math.sqrt(1 - cos * cos)
        cannot_refract = sin / theta > 1
        if cannot_refract:
            out_light_dir = reflect(ray_in, normal)
            hit_record.set_out_light_dir(out_light_dir)
        else:
            out_light_dir = refract(ray_in, normal, theta)
            hit_record.set_out_light_dir(out_light_dir)
        hit_record.set_attenuation(color)


class DiffuseLight(Material):

    def __init__(self, color_texture):
        self.color_texture = color_texture

    def scatter(self, hit_record):
        pass

    def emitted(self, u, v, p):
        return self.color_texture.value(u, v, p)
