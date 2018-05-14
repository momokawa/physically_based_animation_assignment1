"""
this program does collision circles program
- Assumption
1. the number of circles:
2. the velocity of circles: 0~10
3. the center position of circles: 0~10
4. the radius of circles: 0~5
5. No force to be added
6. background wall size 1000 x 1000
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
        for j in range(circle_num - 1, i, -1):
            if circles[i].is_collide_with_other_circle(circles[j]):
                # calculate k_vec
                k_vec = _calc_k_for_collide_with_other_circle(circles[i], circles[j])
                a_val = (1.0/circles[i].mass + 1.0 / circles[j].mass)* 2 * ( k_vec * ( circles[i].velocity - circles[j].velocity))

                # update Velocity
                    """
                        the calculation of Force-based response is like below
                        v1_after = v1_before - ( a/m1 )*k_vec
                        v2_after = v2_before - ( a/m2 )*k_vec
                    """
                circles[i].velocity = circles[i].velocity - ( a_val / circles[i].mass )* k_vec
                circles[j].velocity = circles[j].velocity - ( a_val / circles[j].mass )* k_vec

                # update center position
                    """
                        the calculation of center position is like below
                        center_pos_new = center_pos_now  +  time_step*velocity
                    """
                circles[i].center_pos = circles[i].center_pos + time_step*circles[i].velocity
                circles[j].center_pos = circles[j].center_pos + time_step*circles[j].velocity

def _calc_k_for_collide_with_other_circle(circle_1, circle_2):
    """ calc vector to be used for Force-based response when colliding with other circle """
    distance = circle_1.velocity.distance(circle_2)
    k_vec = (1.0 / distance ) * ( circle_1.velocity - circle_2.velocity)
    return k_vec


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
ims = [] # array to store each image flame
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=int(1.0/time_step), metadata=dict(artist='Mmoko'), bitrate=1800)

""" generate random circles """
for i in range(circle_num):
    # generate random velocity and position
    vel = Vector2D(np.random.randint(10), np.random.randint(10)) # generate 0~100 int randomly
    pos = Vector2D(np.random.randint(100), np.random.randint(100))
    radius = np.random.randint(20) # generate 0~20 int randomly for radius
    mass = 1.0 # [kg]
    circle = Circle(radius = radius, initial_center = pos, initial_velocity = vel, mass = mass) # setup
    circles.append(circle) # add one more circles

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
    """ 円の大きさを含めて表示するための編集　# TODO あとでやる
    drawing_circles = [] # the array to store Circle object
    for j in range(circle_num):
        xy = (circles[j].center_pos.x, circles[j].center_pos.y)
        drawing_circle =  plt.Circle(xy, radius = circles[j].radius, color='r')
        drawing_circles.append(drawing_circle)

    im = plt.imshow(drawing_circles)
    ims.append([im])
    """

    circle_center_x = []
    circle_center_y = []
    circle_radius = []
    for j in range(circle_num):
        circle_center_x.append(circles[j].center_pos.x)
        circle_center_y.append(circles[j].center_pos.y)
        circle_radius.append(circles[j].radius)

    # plot circles
    im = ax.scatter(circle_center_x, circle_center_y, s = circle_radius) # generate new image
    ims.append([im]) # add new image to ims array


# show the plot with 100 msec interval, bacause the time_step is 100msec
ani = animation.ArtistAnimation(fig, ims, interval=int(time_step*1000))
ani.save('task4.mp4',writer=writer)
plt.show()
