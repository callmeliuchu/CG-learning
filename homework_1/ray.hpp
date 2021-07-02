#pragma once

#include "Vector.hpp"

class ray{
    public:
        Vector3f orig;
        Vector3f dir;
    public:
        ray() {}
        ray(const Vector3f& origin,const Vector3f& direction) : orig(origin),dir(direction){}
        Vector3f origin() const {return orig;}
        Vector3f direction() const{return dir;}

        Vector3f at(double t) const {
            return orig + t*dir;
        }
};


