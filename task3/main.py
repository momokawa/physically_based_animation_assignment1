""" The particle moves along with the straigt wire """

"""
Assumption
- only gravity as force
- point: time_stepは細かくとらないといけない
"""

import sys, os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from particle import Particle
import numpy as np
import copy

""" initial setup """
radius = 0.3 # [m]
theta = np.pi / 4.0 # 45 degree
end_point_left = np.array([0.0,0.0]) # left end point [m]
end_point_right = np.array([1.0,1.0]) # right end point [m]
initial_pos = end_point_right # start from end_point_right
mass = 1.0 # kg
force = np.array([0.0, mass*(-9.8)]) # 9.8: 重力加速度
time_step = 0.05 # sec # 100msdc
duration = 15.0 # sec


""" setup for movie """
fig, ax = plt.subplots()
ax.set_xlim([-1,2])
ax.set_ylim([-1,2])
ims = [] # array to store each image flame

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=int(1.0/time_step), metadata=dict(artist='Momoko'), bitrate=1800)

""" Functions used """
def bound_left(particle, end_point_left):
    """ 左端にきたときのバウンドの仕方 """
    """ 今回は傾き45度で計算しているので、逆ベクトルを返すように計算 """
    particle.previous_position = -1*particle.previous_position + particle.position
    particle.position = end_point_left

def bound_right(particle, end_point_right):
    """ 右端にきたときのバウンドの仕方 """
    """ 今回は傾き45度の壁があると想定しているので、同じ向きにかえるように計算 """
    particle.previous_position = end_point_right
    particle.position = end_point_right

""" ==== THIS IS MAIN PART ==== """
# generate a particle
particle = Particle(position=initial_pos, mass = mass, force = force)

for i in range(int(duration/time_step)):
    particle.update_verlet(time_step) # update position
    # move back to wire
    particle.go_to_wire(theta)

    # if it collides with end_point_left:
    if particle.is_reach_left_end(end_point_left):
        # bound
        bound_left(particle, end_point_left)
    # if it collides with end_point_right:
    elif particle.is_reach_right_end(end_point_right):
        bound_right(particle, end_point_right)

    im = plt.plot(np.linspace(0,1), np.linspace(0, 1))
    im = plt.plot(particle.position[0], particle.position[1], 'ro') # plot
    ims.append(im) # add to movie

# show the plot with 100 msec interval, bacause the time_step is 100msec
ani = animation.ArtistAnimation(fig, ims, interval=int(time_step*1000))
ani.save('task3.mp4',writer=writer)
plt.show()
