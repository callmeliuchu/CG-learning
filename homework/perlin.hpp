#pragma once

#include "rtweekend.hpp"


class perlin {
    public:
        perlin(){
            ranfloat = new double[point_count];
            for(int i=0;i<point_count;i++){
                ranfloat[i] = random_double();
            }
            perm_x = perlin_generate_perm();
            perm_y = perlin_generate_perm();
            perm_z = perlin_generate_perm();
        }

        ~perlin(){
            delete[] ranfloat;
            delete[] perm_x;
            delete[] perm_y;
            delete[] perm_z;
        }

        double noise(const Vector3f& p) const{
            auto i = int(4*p.x) & 255;
            auto j = int(4*p.y) & 255;
            auto k = int(4*p.z) & 255;
            return ranfloat[perm_x[i]^perm_y[j]^perm_z[k]];
        }

    private:
        static const int point_count = 256;
        double* ranfloat;
        int* perm_x;
        int* perm_y;
        int* perm_z;

        static int* perlin_generate_perm(){
            auto p = new int[point_count];
            for(int i=0;i<perlin::point_count;i++){
                p[i] = i;
            }
            permute(p,point_count);
            return p;
        }
        static void permute(int* p,int n){
            for(int i=n-1;i>0;i--){
                int target = random_int(0,i);
                int tmp = p[i];
                p[i] = p[target];
                p[target] = tmp;
            }
        }

};