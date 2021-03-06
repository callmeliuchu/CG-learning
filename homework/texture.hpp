#pragma once


#include "rtweekend.hpp"
#include  <iostream>
#include "perlin.hpp"

class texture{
    public:
        virtual Vector3f value(double u,double v,const Vector3f& p) const = 0;
};


class solid_color : public texture{
    public:
        solid_color() {}
        solid_color(Vector3f c) : color_value(c){}
        solid_color(double red,double green,double blue) : solid_color(Vector3f(red,green,blue)){
        }
        virtual Vector3f value(double u,double v,const Vector3f& p)const override {
            return color_value;
        }
    
    private:
        Vector3f color_value;

};


class checker_texture : public texture {
    public:
        checker_texture() {}
        checker_texture(shared_ptr<texture>_even,shared_ptr<texture>_odd):
        even(_even),odd(_odd){}
        
        checker_texture(Vector3f c1,Vector3f c2) : even(make_shared<solid_color>(c1)),
        odd(make_shared<solid_color>(c2)){
        }

        virtual Vector3f value(double u,double v,const Vector3f& p)const override{
            auto sines = sin(10*p.x)*sin(10*p.y)*sin(10*p.z);
            if(sines < 0){
                return odd->value(u,v,p);
            }else{
                return even->value(u,v,p);
            }
        }
    

    public:
        shared_ptr<texture> odd;
        shared_ptr<texture> even;

};


class noise_texture : public texture{
    public:
        noise_texture() {}
        virtual Vector3f value(double u,double v,const Vector3f& p) const override{
            return Vector3f(1,1,1)*noise.noise(p);
        }
    
    public:
        perlin noise;
};


class image_texture : public texture{
    public:
        const static int bytes_per_pixel = 3;
        image_texture() : data(nullptr),width(0),height(0),bytes_per_scanline(0){}
        image_texture(const char* filename){
            auto componets_per_pixel = bytes_per_pixel;
        }
    

    private:
       unsigned char *data;
       int width,height;
       int bytes_per_scanline;
};