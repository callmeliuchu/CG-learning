#pragma once
#define MATERIAL_H

#include "rtweekend.hpp"
#include "ray.hpp"
#include "hittable.hpp" 


class material{
    public:
        virtual bool scatter(
            const ray& r_in, const hit_record& rec, Vector3f& attenuation, ray& sacttered
        )const=0;
};


class lambertian : public material {
    public:
        lambertian(const Vector3f& a): albedo(a){}
        virtual bool scatter(
            const ray& r_in, const hit_record& rec, Vector3f& attenuation, ray& sacttered
        ) const override{
            auto scatter_direction = rec.normal + random_in_unit_vector();
            if(scatter_direction.near_zero()){
                scatter_direction = rec.normal;
            }
            sacttered = ray(rec.p,scatter_direction);
            attenuation = albedo;
            return true;
        }

    public:
        Vector3f albedo;

};

class metal : public material {
    public:
        metal(const Vector3f& a) : albedo(a) {}
        virtual bool scatter(
            const ray& r_in, const hit_record& rec, Vector3f& attenuation, ray& scattered
        )const override{
            Vector3f reflected = reflect(normalize(r_in.direction()),rec.normal);
            scattered = ray(rec.p,reflected);
            attenuation = albedo;
            return (dotProduct(scattered.direction(),rec.normal) > 0);
        }

    public:
        Vector3f albedo;
};