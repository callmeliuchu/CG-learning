#pragma once
#include "aarec.hpp"
#include "hittable.hpp"
#include "hittable_list.h"
#include "material.hpp"

class box : public hittable{
    public:
       box(){}
       virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rec)const override;
       virtual bool bounding_box(double time0,double time1,aabb& output_box)const override{
           output_box = aabb(box_min,box_max);
           return true;
       };
       box(const Vector3f& p_min,const Vector3f& p_max,const shared_ptr<material>m);
    
    public:
       hittable_list bbox;
       Vector3f box_min;
       Vector3f box_max;
};

bool box::hit(const ray& r,double t_min,double t_max,hit_record& rec)const{
    return bbox.hit(r,t_min,t_max,rec);
}

box::box(const Vector3f&  p_min,const Vector3f&  p_max,shared_ptr<material> m){
    box_min = p_min;
    box_max = p_max;
    bbox.add(make_shared<xy_rec>(p_min.x,p_max.x,p_min.y,p_max.y,p_min.z,m));
    bbox.add(make_shared<xy_rec>(p_min.x,p_max.x,p_min.y,p_max.y,p_max.z,m));
    bbox.add(make_shared<yz_rec>(p_min.y,p_max.y,p_min.z,p_max.z,p_min.x,m));
    bbox.add(make_shared<yz_rec>(p_min.y,p_max.y,p_min.z,p_max.z,p_max.x,m));
    bbox.add(make_shared<xz_rec>(p_min.x,p_max.x,p_min.z,p_max.z,p_min.y,m));
    bbox.add(make_shared<xz_rec>(p_min.x,p_max.x,p_min.z,p_max.z,p_max.y,m));
}
