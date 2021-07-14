from vector import Vector3f


class AABB:

    def __init__(self,point_min,point_max):
        self.point_min = point_min
        self.point_max = point_max

    def hit(self,ray,start,end,hit_record):
        direction = ray.direction
        orig = ray.orig
        for a in range(3):
            a = (self.point_min[a]-orig[a]) / direction[a],
            b = (self.point_max[a]-orig[a]) / direction[a]
            t0 = min(a,b)
            t1 = max(a,b)
            start = max(t0,start)
            end = min(t1,end)
            if start >= end:
                return False
        return True


def surrounding_box(aabb1,aabb2):
    p0 = Vector3f(min(aabb1.point_min.x,aabb2.point_min.x),
                  min(aabb1.point_min.y, aabb2.point_min.y),
                  min(aabb1.point_min.z, aabb2.point_min.z)
                  )
    p1 = Vector3f(max(aabb1.point_max.x,aabb2.point_max.x),
                  max(aabb1.point_max.y, aabb2.point_max.y),
                  max(aabb1.point_max.z, aabb2.point_max.z)
                  )
    return AABB(p0,p1)