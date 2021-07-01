#include "color.hpp"
#include "ray.hpp"
#include "Vector.hpp"
#include "Sphere.hpp"
#include "hittable_list.h"
#include "camera.hpp"

#include <iostream>

float hit_sphere(const ray& r,const Sphere& sphere){
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
Vector3f ray_color(const ray& r, const hittable_list& world,int depth){
    if(depth <= 0){
        return Vector3f(0,0,0);
    }
    hit_record rec;
    if(world.hit(r,0,1000,rec)){
        Vector3f target = rec.p + rec.normal + random_in_unit_sphere();
        return 0.5*ray_color(ray(rec.p,target-rec.p),world,depth-1);
    }
    Vector3f unit_direction = normalize(r.direction());
    auto t = 0.5*(unit_direction.y + 1.0);
    return (1-t)*Vector3f(1.0,1.0,1.0) + t*Vector3f(0.5,0.7,1.0);
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
    world.add(make_shared<Sphere>(Vector3f(0.5,0.5,-1),0.3));

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
