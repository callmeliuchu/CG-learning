#pragma once

#include "rtweekend.hpp"


class camera {
    public:
        camera(){
            auto aspect_ratio = 16.0 / 9.0;
            auto viewport_height=2;
            auto viewport_width=viewport_height*aspect_ratio;
            auto focal_length=1;
            orig = Vector3f(0,0,0);
            horizon = Vector3f(viewport_width,0,0);
            vertical = Vector3f(0,viewport_height,0);
            focal = Vector3f(0,0,1);
            lower_left = orig - 0.5*vertical - 0.5*horizon - focal;
        }
        ray get_ray(float u,float v){
            return ray(orig,lower_left + u*horizon + v*vertical - orig);
            
        }
    private:
        Vector3f vertical;
        Vector3f horizon;
        Vector3f orig;
        Vector3f focal;
        Vector3f lower_left;

};
