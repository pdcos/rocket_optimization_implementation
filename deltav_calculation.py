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
        upper_mass = 0
        if self.upper_stage:
            upper_deltav, upper_mass = self.upper_stage.get_deltav()
            total_dry_mass = self.dry_mass + upper_mass
            total_wet_mass = total_dry_mass + self.fuel_mass + upper_mass
            deltav = deltav_formula(total_wet_mass, total_dry_mass, self.I_sp, self.g_0) + upper_deltav

        else:
            total_dry_mass = self.dry_mass
            total_wet_mass = total_dry_mass + self.fuel_mass
            deltav = deltav_formula(total_wet_mass, total_dry_mass, self.I_sp, self.g_0)
            return deltav, total_wet_mass
        
        return deltav

class Rocket():
    def __init__(self):
        self.stages = []

    def add_stage(self, stage:Stage):
        self.stages.append(stage)
    
    def get_deltav(self):
        total_upperstage_deltav = 0
        total_upperstage_mass = 0
        for stage in reversed(self.stages):
            stage_dry_mass = stage.dry_mass + total_upperstage_mass
            stage_wet_mass = stage_dry_mass + stage.fuel_mass
            stage_deltav = deltav_formula(stage_wet_mass, stage_dry_mass, stage.I_sp, stage.g_0)

            total_upperstage_deltav += stage_deltav
            total_upperstage_mass=stage_wet_mass
            #print(total_upperstage_deltav, total_upperstage_mass)
        return total_upperstage_deltav





    
    


if __name__ == "__main__":
    stage2 = Stage(2.1, 1, I_sp=345, g_0= 9.807)
    stage1 = Stage(0.8 , 2 , I_sp=345, g_0= 9.807)


    rocket = Rocket()
    rocket.add_stage(stage1)
    rocket.add_stage(stage2)
    #rocket.add_stage(stage3)
    #rocket.add_stage(stage4)
    rocket.get_deltav()

