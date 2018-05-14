""" difinision for circle """
import numpy as np

class Circle:
        """ Circle class """

        def __init__(self, radius, initial_center, initial_velocity, mass):
            self.radius = radius
            self.center_pos = initial_center
            self.velocity = initial_velocity
            self.mass = mass

        def is_collide_with_other(self, other_circle): # standard way to calc collision checking
            distance = other_circle.center_pos.distance(self.center_pos) # calculate distance between each circle's center

            if distance <= other_circle.radius + self.radius: # if collide
                return True
            else:
                return False

        def is_collide_with_right_wall(self, wall):
            """ collide with right wall """
            if wall.width - self.center_pos.x < self.radius:
                return True
            else:
                return False

        def is_collide_with_left_wall(self, wall):
            """ collide with left wall """
            if self.center_pos.x < self.radius:
                return True
            else:
                return False

        def is_collide_with_bottom_wall(self, wall):
            """ colllide with buttom wall """
            if self.center_pos.y < self.radius:
                return True
            else:
                return False

        def is_collide_with_top_wall(self, wall):
            """ collide with top wall """
            if wall.height - self.center_pos.y < self.radius:
                return True
            else:
                return False

        def is_collide_with_other_circle(self, other):
            """  Check whether it is colliding with the other circle """
            distance_center = self.center_pos.distance(other.center_pos)
            radius_sum = self.radius + other.radius

            if distance_center <= radius_sum:
                return True
            else:
                return False

        def update_euler(self, time_step):
            """ Used euler method to find next position and velocity """
            """ I assume there is no force here """
            # position update
            self.center_pos.x = self.center_pos.x + time_step*self.velocity.x
            self.center_pos.y = self.center_pos.y + time_step*self.velocity.y

            # velocity update
            self.velocity.x = self.velocity.x
            self.velocity.y = self.velocity.y


class Vector2D:
    """ Define 2D vector """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        # 足し算
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        # 引き算
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

    def __mul__(self, other):
        # 内積定義
        temp1 = self.x * other.x
        temp2 = self.y * other.y
        return temp1 + temp2 # this is scaler

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = dx**2 + dy**2
        return np.sqrt(dist)

class Wall:
    """ Define background wall """
    def __init__(self, width, height):
        self.width = width
        self.height = height
