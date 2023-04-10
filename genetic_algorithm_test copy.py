{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pygad\n",
    "import numpy as np\n",
    "from model.build_rocket import RocketModel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'upperStageStructureParams' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn [2], line 55\u001b[0m\n\u001b[1;32m     52\u001b[0m     fitness \u001b[39m=\u001b[39m \u001b[39m1.0\u001b[39m\u001b[39m/\u001b[39mglow\n\u001b[1;32m     53\u001b[0m     \u001b[39mreturn\u001b[39;00m fitness\n\u001b[0;32m---> 55\u001b[0m fitness_func(params_list)\n",
      "Cell \u001b[0;32mIn [2], line 50\u001b[0m, in \u001b[0;36mfitness_func\u001b[0;34m(parameters_list)\u001b[0m\n\u001b[1;32m     33\u001b[0m payloadBayParams \u001b[39m=\u001b[39m {\u001b[39m\"\u001b[39m\u001b[39mpayloadHeight\u001b[39m\u001b[39m\"\u001b[39m: \u001b[39m6.7\u001b[39m,\n\u001b[1;32m     34\u001b[0m                 \u001b[39m\"\u001b[39m\u001b[39mpayloadRadius\u001b[39m\u001b[39m\"\u001b[39m: \u001b[39m4.6\u001b[39m\u001b[39m/\u001b[39m\u001b[39m2\u001b[39m,\n\u001b[1;32m     35\u001b[0m                 \u001b[39m\"\u001b[39m\u001b[39mpayloadMass\u001b[39m\u001b[39m\"\u001b[39m: \u001b[39m7500\u001b[39m,\n\u001b[1;32m     36\u001b[0m                 \u001b[39m\"\u001b[39m\u001b[39mlowerStageRadius\u001b[39m\u001b[39m\"\u001b[39m: parameters_list[\u001b[39m8\u001b[39m],\n\u001b[1;32m     37\u001b[0m                 \u001b[39m\"\u001b[39m\u001b[39mlowerRocketSurfaceArea\u001b[39m\u001b[39m\"\u001b[39m: \u001b[39m0\u001b[39m} \u001b[39m# 0 porque ainda nao temos esse valor\u001b[39;00m\n\u001b[1;32m     39\u001b[0m rocket_model \u001b[39m=\u001b[39m RocketModel(upperEngineParams\u001b[39m=\u001b[39mengineParams,\n\u001b[1;32m     40\u001b[0m                            firstEngineParams\u001b[39m=\u001b[39mengineParamsFirst,\n\u001b[1;32m     41\u001b[0m                            payloadBayParams\u001b[39m=\u001b[39mpayloadBayParams,\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m     47\u001b[0m                            nEnginesUpperStage\u001b[39m=\u001b[39m\u001b[39m1\u001b[39m,\n\u001b[1;32m     48\u001b[0m                            nEnignesFirstStage\u001b[39m=\u001b[39m\u001b[39m9\u001b[39m)\n\u001b[0;32m---> 50\u001b[0m rocket_model\u001b[39m.\u001b[39;49mbuild_all()\n\u001b[1;32m     51\u001b[0m glow \u001b[39m=\u001b[39m rocket_model\u001b[39m.\u001b[39mglow\n\u001b[1;32m     52\u001b[0m fitness \u001b[39m=\u001b[39m \u001b[39m1.0\u001b[39m\u001b[39m/\u001b[39mglow\n",
      "File \u001b[0;32m~/Documents/Estudos/Mestrado/Tese/Implementação da Tese do Jentzsch/rocket_optimization_implementation/model/build_rocket.py:147\u001b[0m, in \u001b[0;36mRocketModel.build_all\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    145\u001b[0m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mbuild_engines()\n\u001b[1;32m    146\u001b[0m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mbuild_payload_bay()\n\u001b[0;32m--> 147\u001b[0m \u001b[39mself\u001b[39;49m\u001b[39m.\u001b[39;49mbuild_upper_stage()\n\u001b[1;32m    148\u001b[0m \u001b[39m#self.build_landing()\u001b[39;00m\n\u001b[1;32m    149\u001b[0m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mbuild_first_stage()\n",
      "File \u001b[0;32m~/Documents/Estudos/Mestrado/Tese/Implementação da Tese do Jentzsch/rocket_optimization_implementation/model/build_rocket.py:73\u001b[0m, in \u001b[0;36mRocketModel.build_upper_stage\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m     66\u001b[0m \u001b[39m#Isp_vac = 351.1\u001b[39;00m\n\u001b[1;32m     68\u001b[0m propellantMass \u001b[39m=\u001b[39m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mcalculate_propellant_mass_upper_stage(coef_e2, m_pl, m_fairing, deltaV, \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mg0, Isp_vac)\n\u001b[1;32m     69\u001b[0m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageStructure \u001b[39m=\u001b[39m interStageStructure(oxName\u001b[39m=\u001b[39m\u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageStructureParams[\u001b[39m\"\u001b[39m\u001b[39moxName\u001b[39m\u001b[39m\"\u001b[39m],\n\u001b[1;32m     70\u001b[0m                                             fuelName\u001b[39m=\u001b[39m\u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageStructureParams[\u001b[39m\"\u001b[39m\u001b[39mfuelName\u001b[39m\u001b[39m\"\u001b[39m],\n\u001b[1;32m     71\u001b[0m                                             propellantMass\u001b[39m=\u001b[39mpropellantMass,\n\u001b[1;32m     72\u001b[0m                                             MR\u001b[39m=\u001b[39m\u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageEngine\u001b[39m.\u001b[39mMR,\n\u001b[0;32m---> 73\u001b[0m                                             radius\u001b[39m=\u001b[39mupperStageStructureParams[\u001b[39m\"\u001b[39m\u001b[39mradius\u001b[39m\u001b[39m\"\u001b[39m],\n\u001b[1;32m     74\u001b[0m                                             tankPressure\u001b[39m=\u001b[39mupperStageStructureParams[\u001b[39m\"\u001b[39m\u001b[39mtankPressure\u001b[39m\u001b[39m\"\u001b[39m],\n\u001b[1;32m     75\u001b[0m                                             maxEngineThrust\u001b[39m=\u001b[39m\u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageEngine\u001b[39m.\u001b[39mthrustVac,\n\u001b[1;32m     76\u001b[0m                                             lowerRadius\u001b[39m=\u001b[39m\u001b[39mFalse\u001b[39;00m,\n\u001b[1;32m     77\u001b[0m                                             upperMass\u001b[39m=\u001b[39mm_pl,\n\u001b[1;32m     78\u001b[0m                                             verbose\u001b[39m=\u001b[39m\u001b[39mFalse\u001b[39;00m\n\u001b[1;32m     79\u001b[0m                                                 )\n\u001b[1;32m     80\u001b[0m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageStructure\u001b[39m.\u001b[39mestimate_all()\n\u001b[1;32m     82\u001b[0m dryMass \u001b[39m=\u001b[39m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageStructure\u001b[39m.\u001b[39mtotalMass \u001b[39m+\u001b[39m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mupperStageEngine\u001b[39m.\u001b[39mtotalMass \u001b[39m*\u001b[39m \u001b[39mself\u001b[39m\u001b[39m.\u001b[39mnEnginesUpperStage\n",
      "\u001b[0;31mNameError\u001b[0m: name 'upperStageStructureParams' is not defined"
     ]
    }
   ],
   "source": [
    "\n",
    "params_list = [11.5 * 1e6, 2.9, 0.23125, 190, \n",
    "                11.5 * 1e6, 2.9, 0.23125, 190,\n",
    "                2,\n",
    "                2.6]\n",
    "\n",
    "def fitness_func(parameters_list):\n",
    "    engineParams = {\"oxName\": \"LOX\",\n",
    "                    \"fuelName\": \"RP-1\",\n",
    "                    \"combPressure\": parameters_list[0],\n",
    "                    \"MR\": parameters_list[1],\n",
    "                    \"nozzleDiam\": parameters_list[2],\n",
    "                    \"eps\": parameters_list[3]}\n",
    "\n",
    "    engineParamsFirst = {\"oxName\": \"LOX\",\n",
    "                    \"fuelName\": \"RP-1\",\n",
    "                    \"combPressure\": parameters_list[4],\n",
    "                    \"MR\": parameters_list[5],\n",
    "                    \"nozzleDiam\": parameters_list[6],\n",
    "                    \"eps\": parameters_list[7]}\n",
    "\n",
    "    upperStageStructureParams = {\"oxName\": \"LOX\",\n",
    "                                 \"fuelName\": \"RP1\",\n",
    "                                 \"MR\": parameters_list[1],\n",
    "                                 \"tankPressure\": 0.1,\n",
    "                                 \"radius\": parameters_list[8],\n",
    "                                } # 0 porque ainda nao temos esse valor\n",
    "    firstStageStructureParams = {\"oxName\": \"LOX\",\n",
    "                                \"fuelName\": \"RP1\",\n",
    "                                \"MR\": parameters_list[5],\n",
    "                                \"tankPressure\": 0.1,\n",
    "                                \"radius\": parameters_list[9],\n",
    "                            } # 0 porque ainda nao temos esse valor\n",
    "    payloadBayParams = {\"payloadHeight\": 6.7,\n",
    "                    \"payloadRadius\": 4.6/2,\n",
    "                    \"payloadMass\": 7500,\n",
    "                    \"lowerStageRadius\": parameters_list[8],\n",
    "                    \"lowerRocketSurfaceArea\": 0} # 0 porque ainda nao temos esse valor\n",
    "\n",
    "    rocket_model = RocketModel(upperEngineParams=engineParams,\n",
    "                               firstEngineParams=engineParamsFirst,\n",
    "                               payloadBayParams=payloadBayParams,\n",
    "                               upperStageStructureParams=upperStageStructureParams,\n",
    "                               firstStageStructureParams = firstStageStructureParams,\n",
    "                               deltaV_upperStage=8000,\n",
    "                               deltaV_landing=2000,\n",
    "                               deltaV_firstStage=4000,\n",
    "                               nEnginesUpperStage=1,\n",
    "                               nEnignesFirstStage=9)\n",
    "\n",
    "    rocket_model.build_all()\n",
    "    glow = rocket_model.glow\n",
    "    fitness = 1.0/glow\n",
    "    return fitness\n",
    "\n",
    "fitness_func(params_list)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "deeplearning",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  },
  "orig_nbformat": 4,
  "vscode": {
   "interpreter": {
    "hash": "fed2aa9592218c4b4de25ecb09c6b292eb81f342cc059d9c96856c64676dbef4"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
