#pragma once

#include "rtweekend.hpp"
#include "hittable.hpp"


class xy_rec : public hittable{
    public:
        xy_rec() {}
        xy_rec(double _x0,double _x1,double _y0,double _y1,double _k,shared_ptr<material> mat)
        : x0(_x0),x1(_x1),y0(_y0),y1(_y1),k(_k),mp(mat){
        };

        virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rex)
        const override;

        virtual bool bounding_box(double time0,double time1,aabb& output_box)const override{
            output_box = aabb(Vector3f(x0,y0,k-0.0001),Vector3f(x1,y1,k+0.0001));
            return true;
        }
    
    public:
        shared_ptr<material> mp;
        double x0,x1,y0,y1,k;
};



bool xy_rec::hit(const ray& r,double t_min,double t_max,hit_record& rec) const{
    auto t = (k - r.origin().z) / r.direction().z;
    if(t < t_min || t > t_max){
        return false;
    }
    auto x = r.origin().x + t*r.direction().x;
    auto y = r.origin().y + t*r.direction().y;
    if(x < x0 || x > x1 || y < y0 || y > y1){
        return false;
    }
    rec.u = (x-x0) / (x1-x0);
    rec.v = (y-y0) / (y1-y0);
    rec.t = t;
    auto outward_normal = Vector3f(0,0,1);
    rec.set_face_normal(r,outward_normal);
    rec.mat_ptr = mp;
    rec.p = r.at(t);
    return true;
}


class xz_rec : public hittable{
    public:
        xz_rec() {}
        xz_rec(double _x0,double _x1,double _z0,double _z1,double _k,shared_ptr<material> mat)
        : x0(_x0),x1(_x1),z0(_z0),z1(_z1),k(_k),mp(mat){
        };

        virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rex)
        const override;

        virtual bool bounding_box(double time0,double time1,aabb& output_box)const override{
            output_box = aabb(Vector3f(x0,k-0.0001,z0),Vector3f(x1,k+0.0001,z1));
            return true;
        }
    
    public:
        shared_ptr<material> mp;
        double x0,x1,z0,z1,k;
};



bool xz_rec::hit(const ray& r,double t_min,double t_max,hit_record& rec) const{
    auto t = (k - r.origin().y) / r.direction().y;
    if(t < t_min || t > t_max){
        return false;
    }
    auto x = r.origin().x + t*r.direction().x;
    auto z = r.origin().z + t*r.direction().z;
    if(x < x0 || x > x1 ||  z < z0 || z > z1){
        return false;
    }
    rec.u = (x-x0) / (x1-x0);
    rec.v = (z-z0) / (z1-z0);
    rec.t = t;
    auto outward_normal = Vector3f(0,1,0);
    rec.set_face_normal(r,outward_normal);
    rec.mat_ptr = mp;
    rec.p = r.at(t);
    return true;
}


class yz_rec : public hittable{
    public:
        yz_rec() {}
        yz_rec(double _y0,double _y1,double _z0,double _z1,double _k,shared_ptr<material> mat)
        : y0(_y0),y1(_y1),z0(_z0),z1(_z1),k(_k),mp(mat){
        };

        virtual bool hit(const ray& r,double t_min,double t_max,hit_record& rex)
        const override;

        virtual bool bounding_box(double time0,double time1,aabb& output_box)const override{
            output_box = aabb(Vector3f(k-0.0001,y0,z0),Vector3f(k+0.0001,y1,z1));
            return true;
        }
    
    public:
        shared_ptr<material> mp;
        double y0,y1,z0,z1,k;
};



bool yz_rec::hit(const ray& r,double t_min,double t_max,hit_record& rec) const{
    auto t = (k - r.origin().x) / r.direction().x;
    if(t < t_min || t > t_max){
        return false;
    }
    auto z = r.origin().z + t*r.direction().z;
    auto y = r.origin().y + t*r.direction().y;
    if(z < z0 || z > z1 || y < y0 || y > y1){
        return false;
    }
    rec.u = (y-y0) / (y1-y0);
    rec.v = (z-z0) / (z1-z0);
    rec.t = t;
    auto outward_normal = Vector3f(1,0,0);
    rec.set_face_normal(r,outward_normal);
    rec.mat_ptr = mp;
    rec.p = r.at(t);
    return true;
}