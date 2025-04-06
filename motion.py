import numpy as np

class Gravitation:
    def __init__(self):
        self.mass1 =  125
        self.mass2 = 10
        self.mass3 = 2
        self.G = 2
        self.dt = 0.005

    def force(self,state1 , state2,state3):
        # f = Gm1m2/r**2 G = 1 for simulation purpose
        pos1, vel1 = state1
        pos2, vel2 = state2
        pos3,vel3 =state3
        
        r_vec12 = pos2 - pos1
        r_mag12 = np.linalg.norm(r_vec12)
        r_hat12 = r_vec12 / r_mag12

        r_vec13 = pos3 - pos1
        r_mag13 = np.linalg.norm(r_vec13)
        r_hat13 = r_vec13 / r_mag13

        r_vec23 = pos3 - pos2
        r_mag23 = np.linalg.norm(r_vec23)
        r_hat23 = r_vec23 / r_mag23
        
        force_mag12 =  self.G*self.mass1 * self.mass2 / (r_mag12 ** 2 )
        force12 = force_mag12 * r_hat12
        
        force_mag13 =  self.G*self.mass1 * self.mass3 / (r_mag13 ** 2 )
        force13 = force_mag13 * r_hat13

        force_mag23 =  self.G*self.mass3 * self.mass2 / (r_mag23 ** 2 )
        force23 = force_mag23 * r_hat23

        acc1 = (force12 + force13) / self.mass1
        acc2 = (force23-force12) / self.mass2
        acc3 = -(force13+force23)/self.mass3

        vel1 += acc1 * self.dt
        vel2 += acc2 * self.dt
        vel3 += acc3 * self.dt

        pos1 += vel1 * self.dt
        pos2 += vel2 * self.dt
        pos3 += vel3 * self.dt

        return [pos1,vel1] ,[pos2,vel2],[pos3,vel3]
        