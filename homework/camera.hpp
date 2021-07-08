#pragma once
#include "ray.hpp"
#include "rtweekend.hpp"


class camera {
    public:
        camera(
            Vector3f lookfrom,
            Vector3f lookat,
            Vector3f vup,
            double vfov, 
            double aspect_ratio,
            double aperture,
            double focus_dist,
            double _time0 = 0,
            double _time1 = 0
            ){
            auto theta = degrees_to_radians(vfov);
            auto h = tan(theta/2);
            auto viewport_height=2*h;
            auto viewport_width=viewport_height*aspect_ratio;


            w = normalize(lookfrom-lookat);
            u = normalize(crossProduct(vup,w));
            v = crossProduct(w,u);


            orig = lookfrom;
            horizon = focus_dist*viewport_width * u;
            vertical = focus_dist*viewport_height * v;
            lower_left = orig - 0.5*vertical - 0.5*horizon - focus_dist*w;
            
            lens_radius = aperture / 2;
            time0 = _time0;
            time1 = _time1;
        }
        ray get_ray(float u,float v){
            Vector3f rd = lens_radius * random_in_unit_disk();
            Vector3f offset = u * rd.x + v * rd.y;
            return ray(orig + offset,lower_left + u*horizon + v*vertical - orig - offset,
                      random_double(time0,time1));
        }
    private:
        Vector3f vertical;
        Vector3f horizon;
        Vector3f orig;
        Vector3f focal;
        Vector3f lower_left;
        Vector3f u,v,w;
        double lens_radius;
        double time0;
        double time1;
};
