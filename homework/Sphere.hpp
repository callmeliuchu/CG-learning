#pragma once
#include "hittable.hpp"
#include "Vector.hpp"

class Sphere : public hittable
{
public:
    Sphere() {};
    Sphere(const Vector3f& c, const float& r)
        : center(c)
        , radius(r)
        , radius2(r * r)
    {};
    Sphere(const Vector3f& c, const float& r,shared_ptr<material>m)
        : center(c)
        , radius(r)
        , radius2(r * r)
        , mat_ptr(m)
    {};
    virtual bool hit(const ray& r,double t_min, double t_max, hit_record& rec)const override;

    Vector3f center;
    float radius, radius2;
    shared_ptr<material> mat_ptr;

private:
    static void get_sphere_uv(const Vector3f& p,double& u,double& v){
        auto theta = acos(-p.y);
        auto phi = atan2(-p.z,p.x) + pi;
        u = phi / (2*pi);
        v = theta / pi;
    }
};


bool Sphere::hit(const ray& r,double t_min,double t_max,hit_record& rec) const {
    // Vector3f d = r.direction();
    // Vector3f o1 = r.origin();
    // Vector3f o2 = center;
    // float a = dotProduct(d,d);
    // float b = 4*dotProduct(o1,d) - 2*dotProduct(d,o2);
    // float c = dotProduct(o2,o2) + 4*dotProduct(o1,o1) - 4*dotProduct(o1,o2) - radius2;
    // float delta = b*b - 4*a*c;
    // if(delta < 0){
    //     return false;
    // }
    // float root = (-b-sqrtf(delta))/(2*a);
    // if (root < t_min || t_max < root) {
    //     root = (-b+sqrtf(delta))/(2*a);
    //     if (root < t_min || t_max < root)
    //         return false;
    // }
    Vector3f oc = r.origin() - center;
    auto a = dotProduct(r.direction(),r.direction());
    auto half_b = dotProduct(oc, r.direction());
    auto c = dotProduct(oc,oc) - radius*radius;

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
    Vector3f outward_normal = (rec.p - center)/radius;
    rec.set_face_normal(r,outward_normal);
    get_sphere_uv(outward_normal,rec.u,rec.v);
    rec.mat_ptr = mat_ptr;
    return true;
}
