""" This program solves task 5: implement a particle system with gravitational field """
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches
from particles import ParticleGravi

""" setup for physical parameter """
# settings
particle_num = 10
time_step = 0.1 # sec
duration = 25.0

""" setup for animation """
fig, ax = plt.subplots()
ax.set_aspect('equal')
ims = [] # array to store each image flame
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=int(1.0/time_step), metadata=dict(artist='Momoko'), bitrate=1800)

""" function used """

def calc_all_forces(particles, particle_num):
    """
    -particle_num x particle_num のarrayを作る
    -あとで合計のForceを計算するときに用いる
    -forces_array[i,j]: the forces from i to j
    """
    # generate empty forces_array
    array = [[np.zeros(2)]*particle_num]*particle_num
    forces_array = np.array(array)

    for i in range(particle_num):
        for j in range(i+1, particle_num):
            force = _calc_force(particles[i], particles[j]) # from i to j gravitational force
            forces_array[i, j] = force
            forces_array[j, i] = -1*force # jからiに対しては逆ベクトル

    return forces_array # 各粒子間のforceをまとめたarray

def _calc_force(particle_1, particle_2):
    """
    calculate forces between two particle
    force from particle_1 to particle_2 direction
    1から2に作用する力(2に対する力)
    """
    G = 6.674e-11 # Gravitational Constant
    dist = np.linalg.norm(particle_1.center_pos - particle_2.center_pos)
    force = G*particle_1.mass*particle_2.mass*(particle_2.center_pos - particle_1.center_pos) / dist**3
    return force # numpy vector

def generate_particles_system(particle_num):
    """ Generate all particles """
    particles = []
    mass = 1.0e10 # [kg] いつかはランダム　# # TODO:
    radius = 2.0 # [m] いつかはランダム
    center_pos = [] # center positions # いつかはランダム

    # 二段になるように配置する
    for i in range(1,3):
        for j in range(1, int(particle_num/2) + 1):
            position = np.array([10.0*i, 10.0*j])
            center_pos.append(position)

    # Generate ParticleGravi object array
    for i in range(particle_num):
        initial_force = np.array([0,0]) # 初期値はゼロ
        initial_velocity = np.array([0,0]) # 初期値はゼロ
        particle = ParticleGravi(mass=mass, radius=radius, \
            center_pos=center_pos[i],forces=initial_force, velocity=initial_velocity)
        particles.append(particle)

    return particles

def update_all_forces(particles, forces_array, particle_num):
    """ sum forces from the other particles """

    sum_forces = np.sum(forces_array, axis=1) # 列方向に足し合わせる
    for i in range(particle_num):
        particles[i].total_force = sum_forces[i] # 合計のforcesを各粒子に代入する

def update_all_particle_position(particles, particle_num, time_step):
    """ update location and velocity of all partiles """
    for i in range(particle_num):
        particles[i].update_euler(time_step)

""" ====== THIS IS MAIN PART ====== """

particles = generate_particles_system(particle_num)

for i in range(int(duration/time_step)):
    forces_array = calc_all_forces(particles, particle_num) # generate forces array from current location
    update_all_forces(particles, forces_array, particle_num) # substitute generated force to each particle
    update_all_particle_position(particles, particle_num, time_step) # move location

    # Add images
    particles_center_x = []
    particles_center_y = []
    particles_radius = []
    for j in range(particle_num):
        particles_center_x.append(particles[j].center_pos[0])
        particles_center_y.append(particles[j].center_pos[1])
        particles_radius.append(particles[j].radius)

    # plot circles
    im = ax.scatter(particles_center_x, particles_center_y, s = particles_radius) # generate new image
    ims.append([im])

# show the plot with 100 msec interval, bacause the time_step is 100msec
ani = animation.ArtistAnimation(fig, ims, interval=int(time_step*1000))
ani.save('task5.mp4',writer=writer)
plt.show()
