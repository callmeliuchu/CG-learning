from vector import dot_product


class HitRecord:
    def __init__(self,hit_point=None,ray_direct=None,dist=None,material=None,tm=None):
        self.hit_point = hit_point
        self.ray_direct = ray_direct
        self.dist = dist
        self.material = material
        self.front = True
        self.normal = None
        self.out_light_dir = None
        self.attenuation = None
        self.tm = tm

    def set_normal(self,normal):
        self.front = dot_product(normal,self.ray_direct) < 0
        self.normal = normal if self.front else -normal

    def set_attenuation(self,attenuation):
        self.attenuation = attenuation

    def can_scatter(self):
        return self.normal * self.out_light_dir

    @property
    def is_hit(self):
        return self.hit_point is not None

    def set_out_light_dir(self,out_light_dir):
        self.out_light_dir = out_light_dir
