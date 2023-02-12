import math
from rocketcea.cea_obj_w_units import CEA_Obj
from proptools import nozzle  
import numpy as np

class EngineProp:
    def __init__(self,
                 fuelName:str,
                 oxName:str,
                 MR:float,
                 Pc:float,
                 eps:float,
                 nozzleDiam = None,
                 At=None,
                 verbose=True):
        """
        fuel_name: 
        ox_name (oxidizer name):
        mr (mixture ratio):
        nozzle_diam (nozzle throat diameter):
        esp (nozzle expansion ratio)
        At (Area - throat)
        """
        
        self.fuelName = fuelName
        self.oxName = oxName
        self.MR = MR
        self.Pc = Pc
        self.nozzleDiam = nozzleDiam
        self.eps = eps
        self.At = At
        self.verbose = verbose

        # Podemos escolher informar o diametro do throat ou a area
        if ((self.At == None) and (self.nozzleDiam != None)):
            self.At = np.pi * ((self.nozzleDiam/2) ** 2)
        elif ((self.At == None) and (self.nozzleDiam == None)):
            raise("Informar At ou nozzleDiam")
        elif ((self.At != None) and (self.nozzleDiam != None)):
            raise("Informar apenas 1: At ou nozzleDiam")

        # Pressao precisa estar em MPa apesar e dados precisam ser fornecidos na ordem de 1e6
        self.ceaObj = CEA_Obj( oxName=oxName, fuelName=fuelName, pressure_units='MPa', cstar_units='m/s', temperature_units='K')

    def calcGasProperties(self):
        # mw -> Molecular weight
        # Cstar -> Characteristc velocity (Isp * g0 / Cf)
        IspVac, Cstar, Tc, mw, gamma = self.ceaObj.get_IvacCstrTc_ChmMwGam(Pc=self.Pc, MR=self.MR, eps=self.eps)
        return
    
    def calcEngineProperties(self):
        IspVac, Cstar, Tc, mw, gamma = self.ceaObj.get_IvacCstrTc_ChmMwGam(Pc=self.Pc, MR=self.MR, eps=self.eps)
        m_molar = mw/1000
        IspSea = self.ceaObj.estimate_Ambient_Isp(Pc=self.Pc, MR=self.MR, eps=self.eps, Pamb=1e5)
        Pc = self.Pc 


        Pe = Pc * nozzle.pressure_from_er(self.eps, gamma)
        # Empuxo no vacuo (N)
        thrustVac = nozzle.thrust(A_t = self.At,
                                  p_c = Pc,
                                  p_e = Pe,
                                  p_a = 0,
                                  gamma=gamma,
                                  er = self.eps)
        # Empuxo no nivel do mar (N)
        thrustSea = nozzle.thrust(A_t = self.At,
                                  p_c = Pc,
                                  p_e = Pe,
                                  p_a = 1e5,
                                  gamma=gamma,
                                  er = self.eps)
        # Fluxo de mass (kg/s)
        massFlow = nozzle.mass_flow(A_t = self.At,
                                     p_c = Pc,
                                     T_c = Tc,
                                     gamma = gamma,
                                     m_molar = m_molar
                                     )   
        if self.verbose:
            print("Isp Vac (s): " + str(IspVac))
            print("Isp Sea (s): " + str(IspSea))
            print("Mass flow (kg/s): " + str(massFlow))
            print("Thrust Vac (kN): " + str(thrustVac/1000))
            print("Thrust Sea (kN): " + str(thrustSea/1000))

        self.IspVac = IspVac
        self.IspSea = IspSea
        self.massFlow = massFlow
        self.thrustVac = thrustVac
        self.thrustSea = thrustSea

    def estimate_engine_mass(self):
        """
        Estima a massa do motor
        
        :param proppelantType: Tipo de propelente - pode ser "Cryogenic-Cryogenic" ou "Cryogenic-Storable"
        :param thrustVac: Empuxo do motor no váculo em Newtons
        :return massTvc: Massa estimada do TVC em kg 
        """
        if self.fuelName == "RP-1":
            propellantType = "Cryogenic-Storable"
        else:
            propellantType = "Cryogenic-Cryogenic"

        if propellantType == "Cryogenic-Cryogenic":
            self.engineMass = 7.54354 * (1e-3) * (self.thrustVac ** (8.85635 * (1e-1))) + 2.02881 * (1e1)
        elif propellantType == "Cryogenic-Storable":
            self.engineMass = 3.75407 * (1e3) * (self.thrustVac ** (7.05627 * (1e-2))) - 8.84790 * (1e3)
        else:
            raise Exception("Selecione um tipo de propelente válido!")
        if self.verbose:
            print(f"Engine Mass: {self.engineMass} [kg]")
        return self.engineMass

    def estimate_tvc_mass(self):
        """
        Estima a massa do Thrust Vector Control System (TVC)
        
        :param thrustVac: Empuxo do motor no váculo em Newtons
        :return massTvc: Massa estimada do TVC em kg 
        """
        self.massTvc = 0.1078 * (self.thrustVac/1e3) + 43.702
        if self.verbose:
            print(f"Engine Mass: {self.massTvc} [kg]")
        return self.massTvc

    def get_total_mass(self):
        self.totalMass = self.massTvc + self.engineMass

    def estimate_all(self):
        self.calcEngineProperties()
        self.estimate_engine_mass()
        self.estimate_tvc_mass()
        self.get_total_mass()
        return



if __name__ == "__main__":

    engine = EngineProp(fuelName="RP-1", 
                    oxName="LOX",
                    MR=2.36,
                    Pc=9.7*1e6 ,
                    At=0.042,
                    eps=21.4)

    engine.estimate_all()