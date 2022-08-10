from matplotlib.pyplot import connect
import numpy as np
from math import exp, log


def deltav_formula(m_0, m_f, I_sp, g_0):
    delta_v = log(m_0/ m_f) * I_sp * g_0
    return delta_v


class Stage:
    def __init__(self, dry_mass, fuel_mass, connects_to=False, I_sp=False, g_0=9.81):
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.upper_stage=connects_to
        self.I_sp = I_sp
        self.g_0 = g_0

    def get_deltav(self):
        upper_deltav = 0
        if self.upper_stage:
            upper_deltav = self.upper_stage.get_deltav()
        else:
            total_dry_mass = self.dry_mass + upper_deltav
            total_wet_mass = total_dry_mass + self.fuel_mass
            deltav = deltav_formula(total_wet_mass, total_dry_mass, self.I_sp, self.g_0)
            return deltav


    
    






if __name__ == "__main__":
    stage2 = Stage(0.0898133201 , 1.03285318 , I_sp=305, g_0= 9.807, connects_to=False)
    stage1 = Stage(0.190643726, 2.19240285, I_sp=305, g_0= 9.807, connects_to=stage2)

    deltav_stage1 = stage1.get_deltav()
    deltav_stage2 = stage2.get_deltav()
    print(deltav_stage1, deltav_stage2)
