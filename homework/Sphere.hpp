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
    virtual bool hit(const ray& r,double t_min, double t_max, hit_record& rec)const override;

    Vector3f center;
    float radius, radius2;
};


bool Sphere::hit(const ray& r,double t_min,double t_max,hit_record& rec) const {
    Vector3f d = r.direction();
    Vector3f o1 = r.origin();
    Vector3f o2 = sphere.center;
    float a = dotProduct(d,d);
    float b = 4*dotProduct(o1,d) - 2*dotProduct(d,o2);
    float c = dotProduct(o2,o2) + 4*dotProduct(o1,o1) - 4*dotProduct(o1,o2) - sphere.radius2;
    float delta = b*b - 4*a*c;
    if(delta < 0){
        return -1.0;
    }
    return (-b-sqrt(delta))/(2*a);
}