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
        self.uv = (0.1,0.2)
        self.p = None
        self.emitted = None

    def can_emitte(self):
        return self.emitted is not None


    def set_normal(self,normal):
        self.front = dot_product(normal,self.ray_direct) < 0
        self.normal = normal if self.front else -normal

    def set_attenuation(self,attenuation):
        self.attenuation = attenuation

    def set_emitted(self,emitted):
        self.emitted = emitted

    def can_scatter(self):
        if self.normal is not None and self.out_light_dir is not None:
            return dot_product(self.normal,self.out_light_dir) > 0
        return False

    @property
    def is_hit(self):
        return self.hit_point is not None

    def set_out_light_dir(self,out_light_dir):
        self.out_light_dir = out_light_dir
