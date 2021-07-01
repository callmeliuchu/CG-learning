#pragma once
#include "ray.hpp"

struct hit_record {
    Vector3f p;
    Vector3f normal;
    double t;
};

class hittable{
    public:
       virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rec)const = 0;
};