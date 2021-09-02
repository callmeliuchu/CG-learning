import taichi as ti
import random

ti.init(arch=ti.cpu)

max_num_particles = 1024
x = ti.Vector.field(2, dtype=ti.f32, shape=max_num_particles)
v = ti.Vector.field(2, dtype=ti.f32, shape=max_num_particles)
f = ti.Vector.field(2, dtype=ti.f32, shape=max_num_particles)
fixed = ti.field(dtype=ti.i32, shape=max_num_particles)
rest_length = ti.field(dtype=ti.f32, shape=(max_num_particles, max_num_particles))
particle_mass = 1.0
num_particles = ti.field(dtype=ti.i32, shape=())
dt = 1e-3
steps = 20
gui = ti.GUI('Explicit Mass Spring System',
             res=(512, 512),
             background_color=0xDDDDDD)


@ti.kernel
def substep():
    num = num_particles[None]

    for i in range(num):
        f[i] = ti.Vector([0, -9.8]) * particle_mass
        for j in range(num):
            if rest_length[i, j] != 0:
                x_ij = x[i] - x[j]
                d = x_ij.normalized()
                f[i] += -(x_ij.norm() - rest_length[i, j]) * d * 1000
                f[i] += -(v[i] - v[j]).dot(d) * d

    for i in range(num):

        v[i] = v[i] + f[i] / particle_mass * dt
        # v[i] *= ti.exp(-dt * 1)

        if fixed[i]:
            v[i] = [0.0, 0.0]
        x[i] = x[i] + v[i] * dt

        for j in ti.static(range(2)):
            if x[i][j] > 1:
                x[i][j] = 1
                v[i][j] = -v[i][j]

            if x[i][j] < 0:
                x[i][j] = 0
                v[i][j] = -v[i][j]

    for i in range(num):
        for j in range(num):
            if i != j:
                r = (x[j] - x[i]).norm()
                if r < 0.15:
                    rest_length[i, j] = 0.1
                    rest_length[j, i] = 0.1


@ti.kernel
def new_particle(pos_x: ti.f32, pos_y: ti.f32, fixed_: ti.i32):
    num = num_particles[None]
    x[num] = [pos_x, pos_y]
    v[num] = ti.Vector([random.random(), random.random()]) * 10
    fixed[num] = fixed_
    num_particles[None] += 1
    for i in range(num):
        r = (x[num] - x[i]).norm()
        if r < 0.15:
            rest_length[i, num] = 0.1
            rest_length[num, i] = 0.1


while True:
    for e in gui.get_events(ti.GUI.PRESS):
        if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT]:
            exit()
        elif e.key == ti.GUI.LMB:
            new_particle(e.pos[0], e.pos[1], int(gui.is_pressed(ti.GUI.SHIFT)))
    for step in range(steps):
        substep()
    num = num_particles[None]
    for i in range(num):
        c = 0xFF0000 if fixed[i] else 0x111111
        gui.circle(pos=x[i], color=c, radius=5)
    for i in range(num):
        for j in range(num):
            if rest_length[i, j] != 0:
                gui.line(x[i], x[j], color=0x444444)
    gui.show()
