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
               auto t0 = fmin((get(minimum,a)-get(r.origin(),a))/get(r.direction(),a),
                              (get(minimum,a)-get(r.origin(),a))/get(r.direction(),a));
                auto t1 = fmax((get(minimum,a)-get(r.origin(),a))/get(r.direction(),a),
                              (get(minimum,a)-get(r.origin(),a))/get(r.direction(),a));
                t_min = fmax(t0,t_min);
                t_max = fmin(t1,t_max);
                if(t_max <= t_min){
                    return false;
                }
           }
           return true;
       }
       const static double get(Vector3f v, int i){
            if(i == 0){
                return v.x;
            }else if(i == 1){
                return v.y;
            }else{
                return v.z;
            }
        }
};

aabb surrounding_box(aabb box0,aabb box1){
    Vector3f small(fmin(box0.min().x,box0.min().x),
                   fmin(box0.min().y,box0.min().y),
                   fmin(box0.min().z,box0.min().z)
                   );
    Vector3f big( fmax(box0.min().x,box0.min().x),
                   fmax(box0.min().y,box0.min().y),
                   fmax(box0.min().z,box0.min().z)
                   );
    return aabb(small,big);
}