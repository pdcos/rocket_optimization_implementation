import numpy as np
import math

from structure.payload_bay_structure import PayloadBayStructure
from structure.stage_structure import interStageStructure
from engines.engine_modeling import EngineProp



class RocketModel():
    def __init__(self, upperEngineParams, firstEngineParams, payloadBayParams, upperStageStructureParams, firstStageStructureParams, deltaV_upperStage, deltaV_landing, deltaV_firstStage, nEnginesUpperStage, nEnignesFirstStage):
        self.upperEngineParams = upperEngineParams
        self.firsEngineParams = firstEngineParams
        self.payloadBayParams = payloadBayParams
        self.upperStageStructureParams = upperStageStructureParams
        self.firstStageStructureParams = firstStageStructureParams
        self.g0 = 9.81
        self.deltaV_upperStage = deltaV_upperStage
        self.upperStageEngine = None,
        self.deltaV_landing = deltaV_landing
        self.deltaV_firstStage = deltaV_firstStage
        self.nEnginesUpperStage = nEnginesUpperStage
        self.nEnginesFirstStage = nEnignesFirstStage
    

    def build_engines(self):
        self.upperStageEngine = EngineProp(fuelName = self.upperEngineParams["fuelName"],
                                           oxName = self.upperEngineParams["oxName"],
                                           Pc = self.upperEngineParams["combPressure"],
                                           MR = self.upperEngineParams["MR"],
                                           nozzleDiam = self.upperEngineParams["nozzleDiam"],
                                           eps = self.upperEngineParams["eps"],
                                           verbose=False)
        self.firstStageEngine = EngineProp(fuelName = self.firsEngineParams["fuelName"],
                                           oxName = self.firsEngineParams["oxName"],
                                           Pc = self.firsEngineParams["combPressure"],
                                           MR = self.firsEngineParams["MR"],
                                           nozzleDiam = self.firsEngineParams["nozzleDiam"],
                                           eps = self.firsEngineParams["eps"],
                                           verbose=False)
        
        self.upperStageEngine.estimate_all()
        self.firstStageEngine.estimate_all()

    def build_payload_bay(self):
        self.payloadBay = PayloadBayStructure(payloadRaidus=self.payloadBayParams["payloadRadius"],
                                              payloadHeight=self.payloadBayParams["payloadHeight"],
                                              payloadMass=self.payloadBayParams["payloadMass"],
                                              lowerSategeRadius=self.payloadBayParams["lowerStageRadius"],
                                              S_lower_rocket=0,
                                              verbose=False)        
        self.payloadBay.estimate_all()

    def build_upper_stage(self):
        coef_e2 = 0.06

        for i in range(50):

            m_fairing = self.payloadBay.totalPayloadFairingMass
            m_pl = self.payloadBay.totalMass
            Isp_vac = self.upperStageEngine.IspVac
            deltaV = self.deltaV_upperStage


            propellantMass = self.calculate_propellant_mass_upper_stage(coef_e2, m_pl, m_fairing, deltaV, self.g0, Isp_vac)
            self.upperStageStructure = interStageStructure(oxName=self.upperStageStructureParams["oxName"],
                                                        fuelName=self.upperStageStructureParams["fuelName"],
                                                        propellantMass=propellantMass,
                                                        MR=self.upperStageEngine.MR,
                                                        radius=upperStageStructureParams["radius"],
                                                        tankPressure=upperStageStructureParams["tankPressure"],
                                                        maxEngineThrust=self.upperStageEngine.thrustVac,
                                                        lowerRadius=False,
                                                        upperMass=m_pl,
                                                        verbose=False
                                                            )
            self.upperStageStructure.estimate_all()

            dryMass = self.upperStageStructure.totalMass + self.upperStageEngine.totalMass * self.nEnginesUpperStage
            coef_e2 = dryMass/(dryMass + propellantMass)

            self.payloadBay.S_rocket = self.upperStageStructure.totalSurfaceArea
            self.build_payload_bay()
        print(f"Coeficiente Estrutural: {coef_e2}, Massa de Propelente: {propellantMass}")

        self.m_0_2 = propellantMass + m_pl + dryMass
        self.coef_e2 = coef_e2
        self.m_p_2 = propellantMass

    def calculate_propellant_mass_upper_stage(self, coef_e, m_pl, m_fairing, deltaV, g0, Isp_vac ):
        num = (m_pl - m_fairing) * (1 - math.exp( deltaV / (g0 * Isp_vac) ))
        den = (1 / (coef_e - 1)) * (1 - coef_e * (math.exp( deltaV / (g0 * Isp_vac) )))
        propellantMass = num/den
        return propellantMass

    def build_landing(self):
        Isp_sea = self.firstStageEngine.IspSea[0]
        coef_e =  - math.exp(  (self.deltaV_landing / (Isp_sea * self.g0)))
        self.coef_e1_landing = coef_e
        print(self.coef_e1_landing)
        return
    
    def build_first_stage(self):
        coef_e1 = 0.06
        Isp_vac = self.firstStageEngine.IspVac

        for i in range(50):
            m_s_1_num = 1 - (math.exp( (self.deltaV_firstStage)/ (Isp_vac *self.g0)))
            m_s_1_den =   math.exp((self.deltaV_firstStage)/ (Isp_vac * self.g0)) - 1/coef_e1
            m_s_1 = m_s_1_num / m_s_1_den * self.m_0_2

            m_p_1 = m_s_1 * (1 - coef_e1) / coef_e1
            #m_p_1_landing = m_s_1 * (1 - self.coef_e1_landing) / self.coef_e1_landing
            #m_p_1_ascent = m_p_1 - m_p_1_landing

            self.firstStageStructure = interStageStructure(oxName=self.firstStageStructureParams["oxName"],
                                                        fuelName=self.firstStageStructureParams["fuelName"],
                                                        propellantMass=m_p_1,
                                                        MR=self.upperStageEngine.MR,
                                                        radius=self.firstStageStructureParams["radius"],
                                                        tankPressure=self.firstStageStructureParams["tankPressure"],
                                                        maxEngineThrust=self.firstStageEngine.thrustVac * self.nEnginesFirstStage,
                                                        lowerRadius=False,
                                                        upperMass=m_p_1,
                                                        verbose=False
                                                            )
            self.firstStageStructure.estimate_all()

            dry_mass = self.firstStageStructure.totalMass + self.firstStageEngine.totalMass * self.nEnginesFirstStage
            coef_e1 = dry_mass / (dry_mass + m_p_1)
        print(f"Coeficiente Estrutural: {coef_e1}, Massa de Propelente: {m_p_1}")

        self.m_p_1 = m_p_1
        self.m_0_1 = dry_mass + m_p_1
        self.coef_e1 = coef_e1
        print( m_p_1)

    def build_all(self):
        self.build_engines()
        self.build_payload_bay()
        self.build_upper_stage()
        #self.build_landing()
        self.build_first_stage()

if __name__ == "__main__":
    engineParams = {"oxName": "LOX",
                    "fuelName": "RP-1",
                    "combPressure": 9.72 * 1e6,
                    "MR": 2.34,
                    "nozzleDiam": 0.23125,
                    "eps": 21.4}
    payloadBayParams = {"payloadHeight": 6.7,
                        "payloadRadius": 4.6/2,
                        "payloadMass": 5000,
                        "lowerStageRadius": 3.66/2,
                        "lowerRocketSurfaceArea": 0} # 0 porque ainda nao temos esse valor

    upperStageStructureParams = {"oxName": "LOX",
                                 "fuelName": "RP1",
                                 "MR": 2.34,
                                 "tankPressure": 0.1,
                                 "radius": 2,
                                } # 0 porque ainda nao temos esse valor
    upperStageStructureParams = {"oxName": "LOX",
                                "fuelName": "RP1",
                                "MR": 2.34,
                                "tankPressure": 0.1,
                                "radius": 2.4,
                            } # 0 porque ainda nao temos esse valor


    rocket_model = RocketModel(upperEngineParams=engineParams,
                               firstEngineParams=engineParams,
                               payloadBayParams=payloadBayParams,
                               upperStageStructureParams=upperStageStructureParams,
                               firstStageStructureParams = upperStageStructureParams,
                               deltaV_upperStage=8000,
                               deltaV_landing=2000,
                               deltaV_firstStage=3500,
                               nEnginesUpperStage=1,
                               nEnignesFirstStage=9)

    rocket_model.build_all()