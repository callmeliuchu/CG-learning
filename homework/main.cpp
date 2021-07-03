#include "color.hpp"
#include "ray.hpp"
#include "Vector.hpp"
#include "Sphere.hpp"
#include "hittable_list.h"
#include "camera.hpp"

#include <iostream>


Vector3f ray_color(const ray& r, const hittable_list& world,int depth){
    if(depth <= 0){
        return Vector3f(0.1,0.1,0.1);
    }
    hit_record rec;
    if(world.hit(r,0.001,infinity,rec)){
        Vector3f target = rec.p + rec.normal + random_in_unit_sphere();
        // Vector3f n = target-rec.p;
        // return 0.5 * (rec.normal + Vector3f(1,1,1));
        // std::cout<<"ray orig:   "<<r.orig<<std::endl;
        // std::cout<<"ray direction:"<<r.direction()<<std::endl;
        // std::cout<<"front_face: "<<rec.front_face<<std::endl;
        // std::cout<<"p       : "<<rec.p.x<<' '<<rec.p.y<<' '<<rec.p.z<<std::endl;
        // std::cout<<"p.normal: "<<rec.normal.x<<' '<<rec.normal.y<<' '<<rec.normal.z<<std::endl;
        // Vector3f center1 = rec.p - rec.normal*0.5;
        // Vector3f center2 = rec.p + rec.normal*0.5;
        // std::cout<<"center1  : "<<center1.x<<' '<<center1.y<<' '<<center1.z<<std::endl;
        // std::cout<<"center2  : "<<center2.x<<' '<<center2.y<<' '<<center2.z<<std::endl;
        // std::cout<<"target  : "<<target.x<<' '<<target.y<<' '<<target.z<<std::endl;
        // std::cout<<"----------------------------------"<<std::endl;
        return 0.5*ray_color(ray(rec.p,target-rec.p),world,depth-1);
    }
    Vector3f unit_direction = normalize(r.direction());
    auto t = 0.5*(unit_direction.y + 1.0);
    return (1.0-t)*Vector3f(1.0,1.0,1.0) + t*Vector3f(0.5,0.7,1.0);
}

int main() {

    // Image

    const auto aspect_ratio = 16.0 / 9.0;
    const int image_width = 400;
    const int image_height = int(image_width / aspect_ratio);
    const int samples_per_pixel = 100;
    const int max_depth = 50;


    //world

    hittable_list world;
    world.add(make_shared<Sphere>(Vector3f(0,0,-1),0.5));
    world.add(make_shared<Sphere>(Vector3f(0,-100.5,-1), 100));


    //camera
    camera cam;

    // Render

    std::cout << "P3\n" << image_width << ' ' << image_height << "\n255\n";

    for (int j = image_height-1; j >= 0; --j) {
        std::cerr << "\rScanlines remaining: " << j << ' ' << std::flush;
        for (int i = 0; i < image_width; ++i) {
            Vector3f pixel_color(0,0,0);
            for(int s=0;s<samples_per_pixel;s++){
                auto u = (double(i) + random_double())/ (image_width-1);
                auto v = (double(j) + random_double()) / (image_height-1);
                ray r = cam.get_ray(u,v);
                pixel_color += ray_color(r,world,max_depth);
            }
            write_color(std::cout, pixel_color,samples_per_pixel);
        }
    }

    std::cerr << "\nDone.\n";
}
