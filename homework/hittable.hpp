#pragma once
#include "ray.hpp"

class material;


struct hit_record {
    Vector3f p;
    Vector3f normal;
    shared_ptr<material>mat_ptr;
    double t;
    double u;
    double v;
    bool front_face;
    inline void set_face_normal(const ray& r,const Vector3f& outward_normal){
        front_face = dotProduct(r.direction(),outward_normal) < 0;
        normal = front_face ? outward_normal : -outward_normal;
    }
};

class hittable{
    public:
       virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rec)const = 0;
};