#pragma once
#define MATERIAL_H

#include "rtweekend.hpp"
#include "ray.hpp"


struct hit_record;

class material{
    public:
        virtual bool scatter(
            const ray& r_in,const hit_record& rec,Vector3f& sacttered
        )const=0;
};
