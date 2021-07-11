#pragma once

#include "rtweekend.hpp"
#include "hittable.hpp"



class moving_sphere : public hittable{
    public:
        moving_sphere() {}
        moving_sphere(
            Vector3f cen0,Vector3f cen1,double _time0,double _time1,double r,shared_ptr<material> m
        ) : center0(cen0),center1(cen1),time0(_time0),time1(_time1),radius(r),mat_ptr(m){};
        virtual bool hit(
            const ray& r,double t_min,double t_max,hit_record& rec
        )const override;
        virtual bool bounding_box(double time0,double time1,aabb& output_box)const override;
        Vector3f center(double time) const;
    public:
        Vector3f center0, center1;
        double time0,time1;
        double radius;
        shared_ptr<material> mat_ptr;
};


Vector3f moving_sphere::center(double time) const {
    return center0 + ((time - time0) / (time1-time0))*(center1 - center0);
}


bool moving_sphere::hit(const ray& r, double t_min, double t_max, hit_record& rec) const {
    Vector3f oc = r.origin() - center(r.time());
    auto a = dotProduct(r.direction(),r.direction());
    auto half_b = dotProduct(oc, r.direction());
    auto c = dotProduct(oc,oc)- radius*radius;

    auto discriminant = half_b*half_b - a*c;
    if (discriminant < 0) return false;
    auto sqrtd = sqrt(discriminant);

    // Find the nearest root that lies in the acceptable range.
    auto root = (-half_b - sqrtd) / a;
    if (root < t_min || t_max < root) {
        root = (-half_b + sqrtd) / a;
        if (root < t_min || t_max < root)
            return false;
    }

    rec.t = root;
    rec.p = r.at(rec.t);
    auto outward_normal = (rec.p - center(r.time())) / radius;
    rec.set_face_normal(r, outward_normal);
    rec.mat_ptr = mat_ptr;

    return true;
}

bool moving_sphere::bounding_box(double time0,double time1,aabb& output_box)const{
    aabb box0(
        center(time0) - Vector3f(radius,radius,radius),
        center(time0) + Vector3f(radius,radius,radius)
    );
    aabb box1(
        center(time1) - Vector3f(radius,radius,radius),
        center(time1) + Vector3f(radius,radius,radius)
    );
    output_box = surrounding_box(box0,box1);
    return true;
}