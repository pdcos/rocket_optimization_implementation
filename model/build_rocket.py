import numpy as np
import math

from structure.payload_bay_structure import PayloadBayStructure
from structure.stage_structure import interStageStructure
from engines.engine_modeling import EngineProp



class RocketModel():
    def __init__(self, upperEngineParams, firstEngineParams, payloadBayParams):
        self.upperEngineParams = upperEngineParams
        self.firsEngineParams = firstEngineParams
        self.payloadBayParams = payloadBayParams

    def build_engines(self):
        self.upperStageEngine = EngineProp(fuelName = self.upperEngineParams["fuelName"],
                                           oxName = self.upperEngineParams["oxName"],
                                           Pc = self.upperEngineParams["combPressure"],
                                           MR = self.upperEngineParams["MR"],
                                           nozzleDiam = self.upperEngineParams["nozzleDiam"],
                                           eps = self.upperEngineParams["eps"])
        self.firstStageEngine = EngineProp(fuelName = self.firsEngineParams["fuelName"],
                                           oxName = self.firsEngineParams["oxName"],
                                           Pc = self.firsEngineParams["combPressure"],
                                           MR = self.firsEngineParams["MR"],
                                           nozzleDiam = self.firsEngineParams["nozzleDiam"],
                                           eps = self.firsEngineParams["eps"])
        
        self.upperStageEngine.estimate_all()
        self.firstStageEngine.estimate_all()

    def build_payload_bay(self):
        self.payloadBay = PayloadBayStructure(payloadRaidus=self.payloadBayParams["payloadRadius"],
                                              payloadHeight=self.payloadBayParams["payloadHeight"],
                                              payloadMass=self.payloadBayParams["payloadMass"],
                                              lowerSategeRadius=self.payloadBayParams["lowerStageRadius"],
                                              S_lower_rocket=0)        
        self.payloadBay.estimate_all()

    def build_all(self):
        self.build_engines()
        self.build_payload_bay()


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
    
    rocket_model = RocketModel(upperEngineParams=engineParams,
                               firstEngineParams=engineParams,
                               payloadBayParams=payloadBayParams)

    rocket_model.build_all()