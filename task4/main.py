"""
this program does collision circles program
- Assumption
1. the number of circles:
2. the velocity of circles: ~
3. the center position of circles: ~
4. the radius of circles: ~
5. No force to be added
6. background wall size 100 x 100
7. perfect elastic collision
"""

from circles import Circle, Vector2D, Wall
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches

""" functions to be used """
def move_all_circles(circles, circle_num, time_step):
    """ update all circles """
    for i in range(circle_num):
        circles[i].update_euler(time_step)

def wall_collide_check_and_move(circles, circle_num, wall):
    """" check whether each cercle collide with wall, and if true, move it """
    for i in range(circle_num):
        if circles[i].is_collide_with_right_wall(wall):
            circles[i].center_pos.x = wall.width - circles[i].radius
            circles[i].velocity.x = -1*circles[i].velocity.x # elastic collision

        elif circles[i].is_collide_with_left_wall(wall):
            circles[i].center_pos.x = circles[i].radius
            circles[i].velocity.x = -1*circles[i].velocity.x

        elif circles[i].is_collide_with_bottom_wall(wall):
            circles[i].center_pos.y = circles[i].radius
            circles[i].velocity.y = -1*circles[i].velocity.y

        elif circles[i].is_collide_with_top_wall(wall):
            circles[i].center_pos.y = wall.height - circles[i].radius
            circles[i].velocity.y = -1*circles[i].velocity.y

def circles_collide_check_and_move(circles, circle_num, time_step):
    """ check whether each circle collide with other circles, and if true, bound them """
    for i in range(circle_num):
        for j in range(i+1, circle_num):
            if circles[i].is_collide_with_other_circle(circles[j]):
                """ if there is collision, update velocity """
                distance = circles[i].velocity.distance(circles[j].velocity)
                n_x = ( circles[j].velocity.x - circles[i].velocity.x) / (distance + 1e-7)
                n_y =  ( circles[j].velocity.y - circles[i].velocity.y) / (distance + 1e-7)
                p = 2.0 * ( circles[i].velocity.x * n_x + circles[i].velocity.y * n_y - circles[j].velocity.x * n_x - circles[j].velocity.y * n_y ) / ( circles[i].mass + circles[j].mass)

                # update Velocity
                circles[i].velocity.x = circles[i].velocity.x - p * circles[i].mass * n_x
                circles[i].velocity.y = circles[i].velocity.y - p * circles[i].mass * n_y
                circles[j].velocity.x = circles[j].velocity.x + p * circles[j].mass * n_x
                circles[j].velocity.y = circles[j].velocity.y + p * circles[j].mass * n_y


""" setup """
# settings
circle_num = 10
circles = []
mass = 1.0
force = Vector2D(0.0, 0.0)
time_step = 0.1 # sec
duration = 30.0
wall = Wall(width = 100, height= 100)

""" setup for movie images """
fig, ax = plt.subplots()
ax.set_xlim([0,100]) # axis setting
ax.set_ylim([0,100])
plt.rcParams["legend.markerscale"] = 0.3 # scale the marker
ims = [] # array to store each image flame
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=int(1.0/time_step), metadata=dict(artist='Momoko'), bitrate=1800)

""" generate random circles """
for i in range(circle_num):
    # generate random velocity and position
    vel = Vector2D(np.random.randint(1,50), np.random.randint(1,50)) # generate 10~50 int randomly
    pos = Vector2D(np.random.randint(10, 100), np.random.randint(10, 100))
    radius = 10.0
    mass = 1.0 # [kg]
    circle = Circle(radius = radius, initial_center = pos, initial_velocity = vel, mass = mass) # setup
    circles.append(circle) # add one more circles


"""" ============ THIS PART IS MAIN PART ============ """

""" Move circles """
for i in range(int(duration/time_step)):
    # move circles
    move_all_circles(circles, circle_num, time_step)

    # wall collision check
    # If collisiong with wall, bound back the circle assuming perfect elastic collision
    wall_collide_check_and_move(circles, circle_num, wall)

    # Check if it collides with other circles's and move
    # others_collide_check_and_move(circles, circle_num)
    circles_collide_check_and_move(circles, circle_num, time_step)

    # create array to sotre circles center_pos and radius
    circle_center_x = []
    circle_center_y = []
    circle_radius = []
    for j in range(circle_num):
        circle_center_x.append(circles[j].center_pos.x)
        circle_center_y.append(circles[j].center_pos.y)
        circle_radius.append(circles[j].radius)

    # plot circles
    im = ax.scatter(circle_center_x, circle_center_y, s = circle_radius*10) # generate new image
    ims.append([im]) # add new image to ims array


# show the plot with 100 msec interval, bacause the time_step is 100msec
ani = animation.ArtistAnimation(fig, ims, interval=int(time_step*1000))
ani.save('task4.mp4',writer=writer)
plt.show()
