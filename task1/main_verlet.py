from particle import Particle2D, Vector2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# initial setup
initial_pos = Vector2D(0.0, 0.0) # [m]
initial_vel = Vector2D(1.0, 0.0) # [m/s]
mass = 1.0 # kg
force = Vector2D(0.0, mass*(-9.8) )# 9.8: 重力加速度
time_step = 0.1 # sec
duration = 10.0 # sec

# generate a particle
particle_1 = Particle2D(position=initial_pos, velocity=initial_vel, force = force, mass=mass, time_step=time_step)
iteration = int(duration/time_step)

fig = plt.figure()
ims = [] # array to store each image flame

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Mmoko'), bitrate=1800)

# calculate using euler method
for i in range(iteration):
    particle_1.update_verlet() # update position and velocity
    im = plt.plot(particle_1.position.x, particle_1.position.y, 'ro') # create new image
    ims.append(im) # add the new graph to ims array

# show the plot with 0.1 sec interval
ani = animation.ArtistAnimation(fig, ims, interval=100)
ani.save('task1_verlet_calc.mp4',writer=writer)
plt.show()
