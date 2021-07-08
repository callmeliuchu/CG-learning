

class Ray:

    def __init__(self,orig,direction,tm):
        self.orig = orig
        self.direction = direction
        self.tm = tm

    def at(self,t):
        return self.orig + t*self.direction
