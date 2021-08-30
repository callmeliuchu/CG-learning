import taichi as ti
import math
import numpy as np
import random
import time

ti.init(arch=ti.cpu)

# 画布
s_ww = 1000
s_hh = 1000
screen = ti.Vector(3, dt=ti.f32, shape=(s_ww,s_hh))


fov = 90
w_h_ratio = s_ww / s_hh
height = math.tan(math.radians(fov/2))*2
width = height*w_h_ratio


look_from = ti.Vector([1.0,3.0,2.0],dt=ti.f32)
look_at = ti.Vector([0.0,0.0,0.0],dt=ti.f32)
v_up = ti.Vector([0.0,1.0,0.0],dt=ti.f32)
ww = look_from - look_at
ww = ww.normalized()
uu = ti.Vector(np.cross(v_up,ww))
uu = uu.normalized()
vv = ti.Vector(np.cross(ww,uu))
vv = vv.normalized()
uu = uu*width
vv = vv*height
origin = look_from
# origin = ti.Vector([0.0,0.0,0.0])
# uu = ti.Vector([1.0,0.0,0.0])
# vv = ti.Vector([0.0,1.0,0.0])
# ww = ti.Vector([0.0,0.0,1.0])
# uu = uu*width
# vv = vv*height


lower_left = origin - vv/2 - uu/2 - ww
# [0,1,2]球心坐标，[3]球半径 [4]1漫反射2反射3折射 [5,6,7]材质
sphere1 = ti.Vector([0,0,-1,0.5,3,1.8,0,0],dt=ti.f32)
sphere2 = ti.Vector([0,-1000.5,-1,1000,1,0.5,0.5,0.5],dt=ti.f32)
sphere3 = ti.Vector([1,0,-1,0.3,2,0.2,0.8,0.8],dt=ti.f32)

print(ww)
print(uu)
print(vv)
print(lower_left)


spheres = ti.Vector(8,dt=ti.f32,shape=1000)
k = 0
spheres[k] = sphere2
for i in range(-11,11):
    for j in range(-11,11):
        if (i+j) % 3 == 0:
            sphere1 = ti.Vector([i, 0, j, 0.5, 3, 1.8, 0, 0], dt=ti.f32)
        elif (i+j) % 3 == 1:
            sphere1 = ti.Vector([i, 0, j, 0.3, 2, 0.2, 0.8, 0.8], dt=ti.f32)
        elif (i + j) % 3 == 2:
            sphere1 = ti.Vector([i, 0, j, 0.4, 1, ti.abs(0.1*j/11), ti.abs(0.3*j/11+0.2),
                                 ti.abs(0.7*i/11)], dt=ti.f32)
        k += 1
        spheres[k] = sphere1



@ti.func
def refractor(u,n,inta):
    n = n.normalized()
    u_paraller = u - (u.dot(n))*n
    u_paraller = u_paraller.normalized()
    u_vertical = -n
    cos_a = u.normalized().dot(u_vertical)
    sin_a = ti.sqrt(1.0-cos_a*cos_a)
    sin_b = sin_a / inta
    rst = False
    ret = ti.Vector([0.0,0.0,0.0],dt=ti.f32)
    if sin_b < 1.0:
        cos_b = ti.sqrt(1-sin_b*sin_b)
        rst = True
        ret = sin_b*u_paraller + cos_b*u_vertical
        ret = ret.normalized()
    return rst,ret

# @ti.func
# def refractor(v, n, ni_over_nt):
#     dt = v.dot(n)
#     #小于0时是全反射
#     discriminant = 1.0 - ni_over_nt * ni_over_nt * ( 1.0 - dt * dt)
#     succ = False
#     refracted = ti.Vector([0.0, 0.0, 0.0])
#     if discriminant > 0:
#         refracted = ni_over_nt * (v - n * dt) - n * ti.sqrt(discriminant)
#         succ = True
#     return succ, refracted






@ti.func
def get_ray(i,j):
    pos = lower_left + i * uu + j * vv
    return origin,pos-origin

@ti.func
def shoot(ray_origin,ray_direct,sphere,t_min,t_max):
    center = ti.Vector([sphere[0], sphere[1], sphere[2]])
    radius = sphere[3]
    oc = ray_origin - center
    a = ray_direct.dot(ray_direct)
    b = 2.0 * oc.dot(ray_direct)
    c = oc.dot(oc) - radius * radius
    delta = b * b - 4.0 * a * c
    rst = False
    t = 0.0
    p = ti.Vector([0.0,0.0,0.0])
    n = ti.Vector([0.0,0.0,0.0])
    if delta > 0:
        r = (-b-ti.sqrt(delta))
        t = r/(2.0*a)
        if t_min <= t < t_max:
            p = ray_origin + ray_direct*t
            n = p - center
            n = n / radius
            rst = True
        else:
            t = (-b+ti.sqrt(delta))/(2.0*a)
            if t_min <= t < t_max:
                p = ray_origin + ray_direct * t
                n = p - center
                n = n / radius
                rst = True
    return rst,t,p,n


@ti.func
def shoot_objects(ray_origin,ray_direct,objects,t_min,t_max):
    res_is_hit = False
    res_t = 0
    res_p = ti.Vector([0.0,0.0,0.0])
    res_n = ti.Vector([0.0,0.0,0.0])
    idx = 0
    for i in range(k):
        is_hit,t,p,n = shoot(ray_origin,ray_direct,objects[i],t_min,t_max)
        if is_hit and t_max > t:
            t_max = t
            res_t = t
            res_is_hit = True
            res_p = p
            res_n = n
            idx = i
    return  res_is_hit,  res_t,   res_p, res_n, idx


def clamp(c):
    if c < 0:
        return 0
    if c > 1:
        return 1
    return c

@ti.func
def reflect(direct,n):
    return direct - 2*(direct.dot(n))*n


@ti.func
def light(direct):
    d = direct.normalized()
    t = 0.5*(d[1] + 1.0)
    return (1-t)*ti.Vector([1.0,1.0,1.0]) + t*ti.Vector([0.5,0.7,1.0])


@ti.func
def random_in_unit_sphere():
    eta1 = ti.random()*0.7
    eta2 = ti.random()*0.7
    eta3 = ti.random()*0.7
    return ti.Vector([eta1, eta2, eta3])



@ti.func
def unit_vector(v):
    k = 1 / (ti.sqrt(v.dot(v)))
    return k * v

@ti.func
def get_earth_material(pos):
    rst = ti.Vector([0.9,0.9,0.9])
    if ti.sin(5*pos[0])*ti.sin(5*pos[1])*ti.sin(5*pos[2]) > 0:
        rst =  ti.Vector([0.2, 0.3, 0.1])
    else:
        rst = ti.Vector([0.9, 0.9, 0.9])
    return rst

@ti.func
def color(ray_origin,ray_direct,spheres):
    t_min = 0.000001
    t_max = 10000000000.0
    depth = 80
    ret = ti.Vector([1.0,1.0,1.0])
    for _ in range(depth):
        is_hit,t,p,n,idx = shoot_objects(ray_origin,ray_direct,spheres,t_min,t_max)
        if is_hit:
            # ti.Vector([1, t, p[0], p[1], p[2], n[0], n[1], n[2]])
            # print(idx)
            # print(spheres[idx][4])
            r_type = spheres[idx][4]
            material = ti.Vector([spheres[idx][5],spheres[idx][6],spheres[idx][7]])
            if idx == 0:#地面
                material = get_earth_material(p)
            # r_type = 1
            if r_type == 1:#漫反射
                ray_origin = p
                ray_direct = n + random_in_unit_sphere()
                if n.dot(ray_direct) <= 0:
                    ret = ti.Vector([0.0,0.0,0.0])
                    break
                ret = material * ret
            elif r_type == 2:#反射
                ray_origin = p
                ray_direct = reflect(ray_direct,n)
                ret = ret*material
            elif r_type == 3:#折射
                val = material[0]
                if n.dot(ray_direct) > 0:
                    #内部往外部
                    val = 1/val
                    n = -n
                ray_origin = p
                suss,v = refractor(ray_direct,n,val)
                if suss:
                    ray_direct = v
                else:
                    ray_direct = reflect(ray_direct,n)
        else:
            ret = ret*light(ray_direct)
            break
    return ret




@ti.kernel
def draw():
    for i,j in screen:
        nums = 20
        c_random = ti.Vector([0.0,0.0,0.0])
        for k in range(nums):
            xx = (float(i) + ti.random()) / s_ww
            yy = (float(j) + ti.random()) / s_hh
            ray_orig, ray_direct = get_ray(xx, yy)
            v = color(ray_orig,ray_direct,spheres)
            c_random = c_random + v
        c_random = c_random / nums
        screen[i,j] = c_random


draw()
data = screen.to_numpy()


with open('res.ppm','w') as ff:
    ff.write("P3\n")
    ff.write(f'{s_ww} {s_hh}\n')
    ff.write("255\n")
    for j in range(s_hh-1,-1,-1):
        for i in range(s_ww):
            r,g,b = data[i,j]
            r = int(255*r) if r is not None else 0
            g = int(255*g) if g is not None else 0
            b = int(255*b) if b is not None else 0
            ff.write(f'{r} {g} {b}\n')