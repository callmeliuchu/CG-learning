#include "color.hpp"
#include "ray.hpp"
#include "Vector.hpp"
#include "Sphere.hpp"

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
Vector3f ray_color(const ray& r){
    Vector3f c = Vector3f(0,0,-1);
    auto t = hit_sphere(r,Sphere(c,0.5));
    if(t > 0){
        std::cout<<t<<std::endl;
        Vector3f point = r.at(t);
        Vector3f N = point - c;
        return 0.5*Vector3f(N.x+1,N.y+1,N.z+1);
    }
    Vector3f unit_direction = normalize(r.direction());
    t = 0.5*(unit_direction.y + 1.0);
    return (1-t)*Vector3f(1.0,1.0,1.0) + t*Vector3f(0.5,0.7,1.0);
}

int main() {

    // Image

    const auto aspect_ratio = 16.0 / 9.0;
    const int image_width = 400;
    const int image_height = int(image_width / aspect_ratio);


    //camera
    auto viewport_height = 2.0;
    auto viewport_width = aspect_ratio * viewport_height;
    auto focal_length = 1.0;

    auto origin = Vector3f(0,0,0);
    auto horizontal = Vector3f(viewport_width,0,0);
    auto vertical = Vector3f(0,viewport_height,0);
    auto lower_left_corner = origin - horizontal/2 
        - vertical / 2 - Vector3f(0,0,focal_length);
    

    // Render

    std::cout << "P3\n" << image_width << ' ' << image_height << "\n255\n";

    for (int j = image_height-1; j >= 0; --j) {
        std::cerr << "\rScanlines remaining: " << j << ' ' << std::flush;
        for (int i = 0; i < image_width; ++i) {
        auto u = double(i) / (image_width-1);
            auto v = double(j) / (image_height-1);
            ray r(origin, lower_left_corner + u*horizontal + v*vertical - origin);
            Vector3f pixel_color = ray_color(r);
            write_color(std::cout, pixel_color);
        }
    }

    std::cerr << "\nDone.\n";
}
