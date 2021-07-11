#include "color.hpp"
#include "ray.hpp"
#include "Vector.hpp"
#include "Sphere.hpp"
#include "hittable_list.h"
#include "camera.hpp"
#include "material.hpp"
#include "hittable.hpp"
#include "moving_sphere.hpp"
#include "texture.hpp"
#include <iostream>
#include "aarec.hpp"


Vector3f ray_color(const ray& r,const Vector3f& background, const hittable_list& world,int depth){
    if(depth <= 0){
        return Vector3f(0.1,0.1,0.1);
    }
    hit_record rec;
    if(!world.hit(r,0.001,infinity,rec)){
        return background;
    }
    ray scattered;
    Vector3f attenuation;
    Vector3f emitted = rec.mat_ptr->emitted(rec.u,rec.v,rec.p);
    if(!rec.mat_ptr->scatter(r,rec,attenuation,scattered)){
        return emitted;
    }
    return emitted +  attenuation * ray_color(scattered,background,world,depth-1);
}


hittable_list two_perlin_spheres(){
    hittable_list objects;
    auto pertext = make_shared<noise_texture>();
    objects.add(make_shared<Sphere>(Vector3f(0,-1000,0),1000,make_shared<lambertian>(pertext)));
    objects.add(make_shared<Sphere>(Vector3f(0,2,0),2,make_shared<lambertian>(pertext)));
    return objects;
}





hittable_list random_scene(){
    hittable_list world;
    auto ground_material = make_shared<lambertian>(Vector3f(0.5,0.5,0.5));
    auto checker = make_shared<checker_texture>(Vector3f(0.2,0.3,0.1),Vector3f(0.9,0.9,0.9));
    world.add(make_shared<Sphere>(Vector3f(0,-1000,0),1000,make_shared<lambertian>(checker)));
  
    for (int a = -11; a < 11; a++) {
        for (int b = -11; b < 11; b++) {
            auto choose_mat = random_double();
            Vector3f center(a + 0.9*random_double(), 0.2, b + 0.9*random_double());

            if ((center - Vector3f(4, 0.2, 0)).length() > 0.9) {
                shared_ptr<material> sphere_material;

                if (choose_mat < 0.8) {
                    // diffuse
                    auto albedo = random_v()*random_v();
                    sphere_material = make_shared<lambertian>(albedo);
                    auto center2 = center + Vector3f(0,random_double(0,0.5),0);
                    world.add(make_shared<moving_sphere>(center, center2,0.0,1.0,0.2, sphere_material));
                } else if (choose_mat < 0.95) {
                    // metal
                    auto albedo = random_double(0.5, 1);
                    auto fuzz = random_double(0, 0.5);
                    sphere_material = make_shared<metal>(albedo, fuzz);
                    world.add(make_shared<Sphere>(center, 0.2, sphere_material));
                } else {
                    // glass
                    sphere_material = make_shared<dielectric>(1.5);
                    world.add(make_shared<Sphere>(center, 0.2, sphere_material));
                }
            }
        }
    }

    auto material1 = make_shared<dielectric>(1.5);
    world.add(make_shared<Sphere>(Vector3f(0, 1, 0), 1.0, material1));

    auto material2 = make_shared<lambertian>(Vector3f(0.4, 0.2, 0.1));
    world.add(make_shared<Sphere>(Vector3f(4, 1, 0), 1.0, make_shared<lambertian>(checker)));

    // auto material3 = make_shared<metal>(Vector3f(0.7, 0.6, 0.5), 0.0);
    // world.add(make_shared<Sphere>(Vector3f(4, 1, 0), 1.0, material3));

    return world;
}

hittable_list simple_light(){
    hittable_list objects;
    auto pertext = make_shared<noise_texture>();
    objects.add(make_shared<Sphere>(Vector3f(0,-1000,0),1000,make_shared<lambertian>(pertext)));
    objects.add(make_shared<Sphere>(Vector3f(0,2,0),2,make_shared<lambertian>(pertext)));
    //     auto difflight = make_shared<diffuse_light>(color(4,4,4));
    
    // objects.add(make_shared<xy_rect>(3, 5, 1, 3, -2, difflight));
    auto difflight = make_shared<diffuse_light>(Vector3f(4,4,4));
    objects.add(make_shared<Sphere>(Vector3f(0,7,0), 2, difflight));
    objects.add(make_shared<xy_rec>(3,5,1,3,-5,difflight));
    return objects;
}


hittable_list cornell_box(){
    hittable_list objects;
    auto red = make_shared<lambertian>(Vector3f(0.65,0.05,0.05));
    auto white = make_shared<lambertian>(Vector3f(0.73,0.73,0.73));
    auto green = make_shared<lambertian>(Vector3f(0.12,0.45,0.15));
    auto light = make_shared<diffuse_light>(Vector3f(15,15,15));

    objects.add(make_shared<yz_rec>(0,555,0,555,555,green));
    objects.add(make_shared<yz_rec>(0, 555, 0, 555, 0, red));
    objects.add(make_shared<xz_rec>(213, 343, 227, 332, 554, light));
    objects.add(make_shared<xz_rec>(0, 555, 0, 555, 0, white));
    objects.add(make_shared<xz_rec>(0, 555, 0, 555, 555, white));
    objects.add(make_shared<xy_rec>(0, 555, 0, 555, 555, white));

    return objects;
}



int main() {

    // Image

    double aspect_ratio = 16.0 / 9.0;
    int image_width = 800.0;
    int image_height = int(image_width / aspect_ratio);
    
    int samples_per_pixel = 50;
    int max_depth = 40;



    //world
    // auto R = cos(pi/4);

    Vector3f lookfrom(5.6,5,3);
    Vector3f lookat(0,0,0);
    Vector3f vup(0,1,0);
    auto vfov = 20;
    auto dist_to_focus = 10;
    auto aperture = 0.1;
    auto world = random_scene();
    Vector3f background(0,0,0);

    switch (6)
    {
    case 2:
        /* code */
        break;
    
    case 3:
        world = two_perlin_spheres();
        lookfrom = Vector3f(13,2,3);
        lookat = Vector3f(0,0,0);
        background = Vector3f(0.7,0.8,1.0);
        vfov = 20.0;
        break;
    
    case 5:
        world = simple_light();
        samples_per_pixel = 400;
        background = Vector3f(0,0,0);
        lookfrom = Vector3f(26,3,6);
        lookat = Vector3f(0,2,0);
        vfov = 20.0;
        break;

    default:
    case 6:
        world = cornell_box();
        aspect_ratio = 1.0;
        image_width = 600;
        samples_per_pixel = 200;
        background = Vector3f(0,0,0);
        lookfrom = Vector3f(278,278,-800);
        lookat = Vector3f(278,278,0);
        vfov = 40.0;
        break;
    }
    
    // auto material_ground = make_shared<lambertian>(Vector3f(0.8, 0.8, 0.0));
    // auto material_center = make_shared<lambertian>(Vector3f(0.1, 0.2, 0.5));
    // auto material_left   = make_shared<dielectric>(1.5);
    // auto material_right  = make_shared<metal>(Vector3f(0.8, 0.6, 0.2), 0.0);

    // world.add(make_shared<Sphere>(Vector3f( 0.0, -100.5, -1.0), 100.0, material_ground));
    // world.add(make_shared<Sphere>(Vector3f( 0.0,    0.0, -1.0),   0.5, material_center));
    // world.add(make_shared<Sphere>(Vector3f(-1.0,    0.0, -1.0),   0.5, material_left));
    // world.add(make_shared<Sphere>(Vector3f(-1.0,    0.0, -1.0), -0.45, material_left));
    // world.add(make_shared<Sphere>(Vector3f( 1.0,    0.0, -1.0),   0.5, material_right));



    camera cam(lookfrom, lookat, vup, vfov, aspect_ratio, aperture, dist_to_focus,0.0,1.0);
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
                pixel_color += ray_color(r,background,world,max_depth);
            }
            write_color(std::cout, pixel_color,samples_per_pixel);
        }
    }

    std::cerr << "\nDone.\n";
}
