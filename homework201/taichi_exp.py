import taichi as ti
import math
import random
import time

ti.init(arch=ti.cpu)

# 画布
s_ww = 800
s_hh = 600
screen = ti.Vector(3, dt=ti.f32, shape=(s_ww,s_hh))

fov = 90
w_h_ratio = s_ww / s_hh
height = math.tan(math.radians(fov/2))*2
width = height*w_h_ratio


origin = ti.Vector([0.0,0.0,0.0],dt=ti.f32)
uu = ti.Vector([1.0,0.0,0.0],dt=ti.f32)
uu = uu*width
vv = ti.Vector([0.0,1.0,0.0],dt=ti.f32)
vv = vv*height
ww = ti.Vector([0,0,1.0],dt=ti.f32)


lower_left = origin - vv/2 - uu/2 - ww

sphere1 = ti.Vector([0,0,-1,0.5],dt=ti.f32)
sphere2 = ti.Vector([0,-100.5,-1,100],dt=ti.f32)
sphere3 = ti.Vector([1,0,1,0.3],dt=ti.f32)


spheres = ti.Vector(4,dt=ti.f32,shape=3)
spheres[0] = sphere1
spheres[1] = sphere2
# spheres[2] = sphere3



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
        if t_min < t < t_max:
            p = ray_origin + ray_direct*t
            n = p - center
            n = n / radius
            rst = True
        else:
            t = (-b+ti.sqrt(delta))/(2.0*a)
            if t_min < t < t_max:
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
    for i in range(len(objects)):
        is_hit,t,p,n = shoot(ray_origin,ray_direct,objects[i],t_min,t_max)
        if is_hit and t_max > t:
            t_max = t
            res_t = t
            res_is_hit = True
            res_p = p
            res_n = n
    return  res_is_hit,  res_t,   res_p, res_n


def clamp(c):
    if c < 0:
        return 0
    if c > 1:
        return 1
    return c


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
def color(ray_origin,ray_direct,spheres):
    t_min = 0.000001
    t_max = 10000000000.0
    depth = 50
    ret = ti.Vector([1.0,1.0,1.0])
    for _ in range(depth):
        is_hit,t,p,n = shoot_objects(ray_origin,ray_direct,spheres,t_min,t_max)
        if is_hit:
            # ti.Vector([1, t, p[0], p[1], p[2], n[0], n[1], n[2]])
            ray_origin = p
            ray_direct = n + random_in_unit_sphere()
            if n.dot(ray_direct) <= 0:
                ret = ti.Vector([0.0,0.0,0.0])
                break
            ret = 0.5 * ret
        else:
            ret = ret*light(ray_direct)
            break
    return ret




@ti.kernel
def draw():
    for j in range(s_hh):
        for i in range(s_ww):
            nums = 20
            c_random = ti.Vector([0.0,0.0,0.0])
            for k in range(nums):
                xx = (i + ti.random()) / s_ww
                yy = (j + ti.random()) / s_hh
                ray_orig, ray_direct = get_ray(xx, yy)
                v = color(ray_orig,ray_direct,spheres)
                c_random = c_random + v
            c_random = c_random / nums
            screen[i,j] = c_random





gui = ti.GUI("screen", (s_ww,s_hh))

for _ in range(10000):
    draw()
    gui.set_image(screen.to_numpy())
    gui.show()
