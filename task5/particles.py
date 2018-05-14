""" Here difines each particle in the sysytem with gravitational field """

class ParticleGravi:

    def __init__(self, mass, radius, center_pos, forces, velocity):
        self.mass = mass
        self.radius = radius
        self.center_pos = center_pos
        self.total_force = forces # 2D Array
        self.velocity = velocity # 2D array

    def update_euler(self, time_step):
        """
        Update positio and velocity using euler method
        """
        self.velocity = self.velocity + time_step*(self.total_force)/self.mass
        self.center_pos = self.center_pos + time_step*(self.velocity)
