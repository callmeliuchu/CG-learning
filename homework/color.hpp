#pragma once
#include "Vector.hpp"
#include "rtweekend.hpp"
#include <iostream>


void write_color(std::ostream &out, Vector3f pixel_color,int sample_per_pix) {
    // Write the translated [0,255] value of each color component.

    auto r = pixel_color.x;
    auto g = pixel_color.y;
    auto b = pixel_color.z;
    auto scale = 1.0 / sample_per_pix;
    r *= scale;
    g *= scale;
    b *= scale;


    out << static_cast<int>(255.999 * clamp(r,0,0.9999)) << ' '
        << static_cast<int>(255.999 * clamp(g,0,0.9999)) << ' '
        << static_cast<int>(255.999 * clamp(b,0,0.9999)) << '\n';
}