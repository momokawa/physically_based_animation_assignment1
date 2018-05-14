import sys, os
sys.path.append(os.pardir)
from task1.particle import Particle2D, Vector2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

""" Used verlet integration """

# initial setup
initial_pos = Vector2D(0.0, 10.0) # [m]
initial_vel = Vector2D(0.0, 0.0) # [m/s] # free fall
mass = 1.0 # kg
force = Vector2D(0.0, mass*(-9.8) )# 9.8: 重力加速度
time_step = 0.1 # sec # 100msdc
duration = 15.0 # sec

# generate a particle
particle_1 = Particle2D(position=initial_pos, velocity=initial_vel, force = force, mass=mass, time_step=time_step)
iteration = int(duration/time_step)

fig = plt.figure()
ims = [] # array to store each image flame

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=int(1/time_step), metadata=dict(artist='Momoko'), bitrate=1800)

# wall
wall_height_y = 0.0 # [m]

# Assume the wall won't move(Velocity of wall = 0) and the coefficient of resituation
# is e.
# In this case, I'm using e = 1.(完全弾性衝突)
# Assume "Free Fall"

# Calculate position using verlet integration
for i in range(iteration):
    particle_1.update_verlet() # update position

    if particle_1.position.y < wall_height_y and particle_1.previous_position.y > wall_height_y: # if ball is below wall
        particle_1.previous_position.y = -1*particle_1.previous_position.y + particle_1.position.y # move previous position inside the wall
        particle_1.position.y = 0 # move to the surface of wall


    im = plt.plot(particle_1.position.x, particle_1.position.y, 'ro') # generate new image
    ims.append(im) # add new image to ims array


# show the plot with 100 msec interval, bacause the time_step is 100msec
ani = animation.ArtistAnimation(fig, ims, interval=int(time_step*1000))
ani.save('task2.mp4',writer=writer)
plt.show()
