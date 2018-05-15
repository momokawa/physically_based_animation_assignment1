""" The particle moves along with the straigt wire """

import sys, os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from particle import Particle

""" initial setup """
radius = 0.3 # [m]
initial_pos = Vector2D(radius, 0.0) # [m]
initial_vel = Vector2D(0.0, 0.0) # [m/s] # free fall
mass = 1.0 # kg
force = Vector2D(0.0, mass*(-9.8) )# 9.8: 重力加速度
time_step = 0.1 # sec # 100msdc
duration = 15.0 # sec
center_pos = Vector2D(0.0, 0.0)

""" setup for movie """
# generate a particle
particle_1 = Particle2D(position=initial_pos, velocity=initial_vel, force = force, mass=mass, time_step=time_step)
iteration = int(duration/time_step)

fig = plt.figure()
ims = [] # array to store each image flame

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=int(1/time_step), metadata=dict(artist='Momoko'), bitrate=1800)


for i in range(iteration):
    particle_1.update_euler() # move particle based on force and previous position
    particle_1.update_based_on_wire(radius = radius, center_pos = center_pos) # move particle cconsiering wire
    im = plt.plot(particle_1.position.x, particle_1.position.y, 'ro') # generate new image
    ims.append(im) # add new image to ims array

# show the plot with 100 msec interval, bacause the time_step is 100msec
ani = animation.ArtistAnimation(fig, ims, interval=int(time_step*1000))
ani.save('task3.mp4',writer=writer)
plt.show()
