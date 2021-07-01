#pragma once


#include <cmath>
#include <limits>
#include <memory>
#include "ray.hpp"
#include "Vector.hpp"


using std::shared_ptr;
using std::make_shared;
using std::sqrt;


const double infinity = std::numeric_limits<double>::infinity();
const double pi = 3.1415826235;


inline double degrees_to_radians(double degrees){
    return degrees * pi / 180.0;
}

inline double clamp(double x,double min,double max){
    if(x < min){
        return min;
    }
    if(x > max){
        return max;
    }
    return x;
}

inline double random_double() {
    // Returns a random real in [0,1).
    return rand() / (RAND_MAX + 1.0);
}

inline double random_double(double min, double max) {
    // Returns a random real in [min,max).
    return min + (max-min)*random_double();
}