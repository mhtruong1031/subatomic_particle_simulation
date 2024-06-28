import numpy as np
from math import sqrt

k_constant = 8.987e9

class Particle:
    def __init__(self, pos: tuple = (0,0,0), vel: tuple = (0,0,0), accel: tuple = (0,0,0)) -> None:
        # Position-based vectors
        self.pos   = np.array(pos).astype(float)    # Position
        self.vel   = np.array(vel).astype(float)    # Velocity
        self.accel = np.array(accel).astype(float)  # Acceleration

        self.x, self.y, self.z = self.pos

        self.q    = 0.0 # default charge
        self.mass = 0.0 # default mass
        self.tme  = 0.0 # default total mechanical energy

        self.kine = 0.0 # default kinetic energy
        self.pote = 0.0 # default kinetic energy

    # Update position-based vectors
    def update(self, dt: float, particles: list) -> None:
        '''self.kine = 0.5 * self.mass * np.linalg.norm(self.vel)**2
        self.pote = self.get_current_pote(particles)

        if (self.kine + self.pote) != self.tme and np.linalg.norm(self.vel) != 0:
            if (self.kine + self.pote) < self.tme:
                scalar = sqrt( (2 * (self.tme - self.pote)) / self.mass) / np.linalg.norm(self.vel)
                self.vel *= scalar
            else:
                tme_correction = 0 # TO DO'''

        self.pos   += self.vel * dt
        self.vel   += self.accel * dt
        self.accel = np.array((0.0, 0.0, 0.0)) # reset for next force application

    # Adjusts the particle's acceleration according to the properties of another acting particle {a_p}
    def apply_force(self, a_p, force_scalar) -> None:
        displacement = self.pos - a_p.pos
        dist = np.linalg.norm(displacement)

        if dist < 1: # prevents division by 0
            self.accel += np.array((0,0,0)).astype(float)
            return
        
        force = k_constant * (self.q * a_p.q) / (dist)**2 # coulombs law
        force *= force_scalar

        r_hat = displacement / dist

        f = force * r_hat

        self.accel += f / self.mass
    
    # Returns total potential energy of the system
    def get_current_pote(self, particles: list) -> None:
        total_part = set(particles.copy()) - set([self])

        pote = 0.0
        for p in total_part:
            displacement = self.pos - p.pos
            dist = np.linalg.norm(displacement)
            pote += k_constant * (self.q * p.q) / dist

        return pote
    
    # Set current energy values as the total mechanical energy in the system
    def set_tme(self, particles: list) -> None:
        self.tme = self.get_current_pote(particles)
        self.tme += 0.5 * self.mass * np.linalg.norm(self.vel)**2

    # Return position
    def get_pos(self) -> np.array:
        return self.pos

    

class Nucleus(Particle):
    def __init__(self, protons: int, neutrons: int = None, pos: tuple = (0,0,0), vel: tuple = (0,0,0), accel: tuple = (0,0,0)) -> None:
        super().__init__(pos, vel, accel)

        # Default to stable isotope; neutrons = protons
        if neutrons == None:
            neutrons = protons
        
        # Constants
        self.protons = protons
        self.mass = (self.protons * 1.67262192e-27) + (neutrons * 1.67492749804e-27)   # Mass of nucelus
        self.q    = 1.602176634e-19 * self.protons                                     # Charge of proton in coulombs

    # Returns the number of protons in the nucleus
    def get_protons(self) -> int:
        return self.protons


class Electron(Particle):
    def __init__(self, pos: tuple = (0,0,0), vel: tuple = (0,0,0), accel: tuple = (0,0,0)) -> None:
        super().__init__(pos, vel, accel)

        # Constants
        self.mass = 9.1093837e-31     # Mass of e- in kilograms
        self.q    = -1.602176634e-19  # Charge of e- in coulombs
