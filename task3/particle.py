""" This defines particle of task3 """

class Particle:

    def __init__(self, position, previous_pos, mass, force):
        """
        pos: center position of particle
        previous_pos: previous center position of particle
        mass: mass of particle
        force: forces applied to the particle
        """
        self.center_pos = center_pos
        self.previous_pos = previous_pos
        self.mass = mass
        self.force = force

    def update_verlet(self):
        current_position = copy.deepcopy(self.position)
        previous_position = copy.deepcopy(self.previous_position)
