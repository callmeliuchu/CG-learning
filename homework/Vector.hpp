#pragma once

#include <cmath>
#include <iostream>
#include "rtweekend.hpp"

class Vector3f
{
public:
    Vector3f()
        : x(0)
        , y(0)
        , z(0)
    {}
    Vector3f(float xx)
        : x(xx)
        , y(xx)
        , z(xx)
    {}
    Vector3f(float xx, float yy, float zz)
        : x(xx)
        , y(yy)
        , z(zz)
    {
        arr[0]=x;
        arr[1]=y;
        arr[2]=z;
    }
    double get(int i)const{
        if(i == 0){
            return x;
        }else if(i == 1){
            return y;
        }else{
            return z;
        }
    }
    double operator[](int i)const{
        return arr[i];
    }
    double& operator[](int i) { 
        return arr[i]; 
    }
    bool near_zero() const{
        const auto s = 1e-8;
        return (fabs(x<s)) && (fabs(y<s)) && (fabs(z<s));
    }
    Vector3f operator*(const float& r) const
    {
        return Vector3f(x * r, y * r, z * r);
    }
    Vector3f operator/(const float& r) const
    {
        return Vector3f(x / r, y / r, z / r);
    }

    Vector3f operator*(const Vector3f& v) const
    {
        return Vector3f(x * v.x, y * v.y, z * v.z);
    }
    Vector3f operator-(const Vector3f& v) const
    {
        return Vector3f(x - v.x, y - v.y, z - v.z);
    }
    Vector3f operator+(const Vector3f& v) const
    {
        return Vector3f(x + v.x, y + v.y, z + v.z);
    }
    Vector3f operator-() const
    {
        return Vector3f(-x, -y, -z);
    }
    Vector3f& operator+=(const Vector3f& v)
    {
        x += v.x, y += v.y, z += v.z;
        return *this;
    }
    friend Vector3f operator*(const float& r, const Vector3f& v)
    {
        return Vector3f(v.x * r, v.y * r, v.z * r);
    }
    friend std::ostream& operator<<(std::ostream& os, const Vector3f& v)
    {
        return os << v.x << ", " << v.y << ", " << v.z;
    }
    double length(){
        return sqrt(x*x+y*y+z*z);
    }
    float x, y, z;
    double arr[3];
};

class Vector2f
{
public:
    Vector2f()
        : x(0)
        , y(0)
    {}
    Vector2f(float xx)
        : x(xx)
        , y(xx)
    {}
    Vector2f(float xx, float yy)
        : x(xx)
        , y(yy)
    {}
    Vector2f operator*(const float& r) const
    {
        return Vector2f(x * r, y * r);
    }
    Vector2f operator+(const Vector2f& v) const
    {
        return Vector2f(x + v.x, y + v.y);
    }
    float x, y;
};

inline Vector3f lerp(const Vector3f& a, const Vector3f& b, const float& t)
{
    return a * (1 - t) + b * t;
}

inline Vector3f normalize(const Vector3f& v)
{
    float mag2 = v.x * v.x + v.y * v.y + v.z * v.z;
    if (mag2 > 0)
    {
        float invMag = 1 / sqrtf(mag2);
        return Vector3f(v.x * invMag, v.y * invMag, v.z * invMag);
    }

    return v;
}

inline float dotProduct(const Vector3f& a, const Vector3f& b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

inline Vector3f crossProduct(const Vector3f& a, const Vector3f& b)
{
    return Vector3f(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}

inline static Vector3f random_v(){
    return Vector3f(random_double(),random_double(),random_double());
}

inline static Vector3f random_v(double min,double max){
    return Vector3f(random_double(min,max),random_double(min,max),random_double(min,max));
}

Vector3f random_in_unit_sphere(){
    while(true){
        auto p = random_v(-1,1);
        if(dotProduct(p,p) >= 1)continue;
        return p;
    }
}

Vector3f random_in_unit_vector(){
    return normalize(random_in_unit_sphere());
}

Vector3f reflect(const Vector3f& v,const Vector3f& n){
    return v - 2*dotProduct(v,n)*n;
}

Vector3f refract(const Vector3f& uv,const Vector3f& n,double etai_over_etat){
    auto cos_theta = fmin(dotProduct(-uv,n),1);
    Vector3f r_out_perp = etai_over_etat*(uv + cos_theta*n);
    Vector3f r_out_parallel = -sqrt(fabs(1.0-dotProduct(r_out_perp,r_out_perp)))*n;
    return r_out_perp + r_out_parallel;
}


Vector3f random_in_unit_disk(){
    while(true){
        auto p = Vector3f(random_double(-1,1),random_double(-1,1),0);
        if(dotProduct(p,p) >= 1){
            continue;
        }
        return p;
    }
}