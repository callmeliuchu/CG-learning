#pragma once
#include "ray.hpp"

struct hit_record {
    Vector3f p;
    Vector3f normal;
    double t;
    bool front_face;
    inline void set_face_normal(const ray& r,const Vector3f& outward_normal){
        front_face = dotProduct(r.direction(),outward_normal) < 0;
        // std::cout<<"+++++++"<<std::endl;
        // std::cout<<outward_normal.x<<" "<<outward_normal.y<<" "<<outward_normal.z<<std::endl;
        normal = front_face ? outward_normal : -outward_normal;
        // std::cout<<normal.x<<" "<<normal.y<<" "<<normal.z<<std::endl;
        // std::cout<<"+++++++++"<<std::endl;
    }
};

class hittable{
    public:
       virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rec)const = 0;
};