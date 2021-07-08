#pragma once

#include "Vector.hpp"

class ray{
    public:
        Vector3f orig;
        Vector3f dir;
        double tm;
    public:
        ray() {}
        ray(const Vector3f& origin,const Vector3f& direction,double tm = 0.0) : orig(origin),dir(direction),tm(tm){}
        Vector3f origin() const {return orig;}
        Vector3f direction() const{return dir;}
        double time() const{return tm;}


        Vector3f at(double t) const {
            return orig + t*dir;
        }
};


