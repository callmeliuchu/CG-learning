#pragma once
#include "rtweekend.hpp"
#include "ray.hpp"


class aabb{
    public:
       Vector3f minimum;
       Vector3f maximum;
       aabb(){}
       aabb(const Vector3f& a,const Vector3f& b){minimum=a;maximum=b;}
       Vector3f min() const {return minimum;}
       Vector3f max() const {return maximum;}

       bool hit(const ray& r,double t_min,double t_max)const{
           for(int a=0;a<3;a++){
              auto t0 = fmin((minimum.get(a) - r.origin().get(a)) / r.direction().get(a),
                               (maximum.get(a) - r.origin().get(a)) / r.direction().get(a));
                auto t1 = fmax((minimum.get(a) - r.origin().get(a)) / r.direction().get(a),
                               (maximum.get(a) - r.origin().get(a)) / r.direction().get(a));
                t_min = fmax(t0,t_min);
                t_max = fmin(t1,t_max);
                if(t_max <= t_min){
                    return false;
                }
           }
           return true;
       }
};

aabb surrounding_box(aabb box0,aabb box1){
    Vector3f small(fmin(box0.min().x, box1.min().x),
               fmin(box0.min().y, box1.min().y),
               fmin(box0.min().z, box1.min().z));

    Vector3f big(fmax(box0.max().x, box1.max().x),
               fmax(box0.max().y, box1.max().y),
               fmax(box0.max().z, box1.max().z));

    return aabb(small,big);
}