""" This defines particle of task3 """
import copy
import numpy as np

class Particle:

    def __init__(self, position, mass, force):
        """
        position: center position of particle. numpy array
        previous_pos: previous center position of particle. numpy array
        mass: mass of particle
        force: forces applied to the particle. numpy array
        """
        self.position = position
        self.previous_position = position
        self.mass = mass
        self.force = force

    def update_verlet(self, time_step):
        """ Update position using verlet integration( position-based) """
        # save this for later
        current_position = copy.deepcopy(self.position)
        previous_position = copy.deepcopy(self.previous_position)

        # update
        new_position =  2*current_position - previous_position + (time_step**2)*(self.force/self.mass)
        self.position = new_position
        self.previous_position = current_position

    def go_to_wire(self, theta):
        """
        theta: the line angle from horizontal
        this function moves the particle back to wire
        """
        # get delta y
        d_y = self.position[1] - self.previous_position[1]

        # update x direction and y direction to move back to wire
        """
        x_n = x_n - d_y*sin(theta)*cos(theta)
        y_n = y_n - d_y*sin(theta)*sin(theta)
        """
        # x_n
        self.position[0] = self.previous_position[0] + d_y*np.cos(theta)*np.cos(theta)
        # y_n
        self.position[1] = self.previous_position[1] + d_y *np.sin(theta)*np.cos(theta)

    def is_reach_left_end(self, end_point_left):
        """ x座標の値で端にきているか確認 """
        if self.position[0] < end_point_left[0] and self.previous_position[0] >= end_point_left[0]:
            return True
        else:
            return False

    def is_reach_right_end(self, end_point_right):
        """ x座標の値で端にきているか確認 """
        if self.position[0] > end_point_right[0] and self.previous_position[0] < end_point_right[0]:
            return True
        else:
            return False
