

class Ray:

    def __init__(self,orig,direction):
        self.orig = orig
        self.direction = direction

    def at(self,t):
        return self.orig + t*self.direction
