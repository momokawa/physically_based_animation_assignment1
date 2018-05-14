import copy
import numpy as np

class Particle2D:
    """ A Particle class for 2D """

    def __init__(self, position, velocity, force, mass, time_step):
        self.position = position
        self.velocity = velocity
        self.force = force
        self.previous_position = position
        # self.previous_position = Vector2D(position.x - time_step*velocity.x, position.y - time_step*velocity.y) # for initial previous_position in case using verlet integration
        self.mass = mass # kg
        self.time_step = time_step # sec

    def update_euler(self):
        """ update velocity and position using Euler method """
        # position update
        self.position.x = self.position.x + self.time_step*self.velocity.x
        self.position.y = self.position.y + self.time_step*self.velocity.y

        # velocity update
        self.velocity.x = self.velocity.x + (self.time_step)*(self.force.x)/(self.mass)
        self.velocity.y = self.velocity.y + (self.time_step)*(self.force.y)/(self.mass)

    def update_verlet(self): # TODO check here to know the reason why previous_position is changed after one iteration
        """ update position using Verlet integration """
        # keep current value and previous value
        current_position = copy.deepcopy(self.position)
        previous_position = copy.deepcopy(self.previous_position)
        print('b_', previous_position.y, current_position.y)

        # substitute current_position to self.previous_position
        self.previous_position = current_position

        # update
        new_position_x =  2*current_position.x - previous_position.x + (self.time_step**2)*(self.force.x/self.mass)
        new_position_y =  2*current_position.y - previous_position.y + (self.time_step**2)*(self.force.y/self.mass)

        self.position.x = new_position_x
        self.position.y = new_position_y

        print('A_', current_position.y, new_position_y, '\n')


    def update_based_on_wire(self, radius, center_pos):
        """ update position assuming the ball is bead on a wire """

        distance = center_pos.distance(self.position) # calc distance between center and current position
        # update position considering wire
        self.position = center_pos + (radius/distance)*(self.position - center_pos)

class Vector2D:
    """ Define 2D vector """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __rmul__(self, value):
        # if the value is scaler
        # TODO will create error in case value is not scaler
        # 左側がスカラーで右がベクトルの場合の定義
        self.x =  self.x*value
        self.y =  self.y*value
        return self

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = dx**2 + dy**2
        return np.sqrt(dist)
