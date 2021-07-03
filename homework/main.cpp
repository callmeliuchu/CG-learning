#include "color.hpp"
#include "ray.hpp"
#include "Vector.hpp"
#include "Sphere.hpp"
#include "hittable_list.h"
#include "camera.hpp"
#include "material.hpp"

#include <iostream>


Vector3f ray_color(const ray& r, const hittable_list& world,int depth){
    if(depth <= 0){
        return Vector3f(0.1,0.1,0.1);
    }
    hit_record rec;
    if(world.hit(r,0.001,infinity,rec)){
        ray scattered;
        Vector3f attenuation;
        if(rec.mat_ptr->scatter(r,rec,attenuation,scattered)){
            return attenuation * ray_color(scattered,world,depth-1);
        }

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

    auto material_ground = make_shared<lambertian>(Vector3f(0.8, 0.8, 0.0));
    auto material_center = make_shared<lambertian>(Vector3f(0.7, 0.3, 0.3));
    auto material_left   = make_shared<metal>(Vector3f(0.8, 0.8, 0.8));
    auto material_right  = make_shared<metal>(Vector3f(0.8, 0.6, 0.2));


    world.add(make_shared<Sphere>(Vector3f( 0.0, -100.5, -1.0), 100.0, material_ground));
    world.add(make_shared<Sphere>(Vector3f( 0.0,    0.0, -1.0),   0.5, material_center));
    world.add(make_shared<Sphere>(Vector3f(-1.0,    0.0, -1.0),   0.5, material_left));
    world.add(make_shared<Sphere>(Vector3f( 1.0,    0.0, -1.0),   0.5, material_right));


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
