import numpy as np

from constants import *
from ampacity import *
from cable_parameters import *
# from overload_auto import *

if __name__ == "__main__":
    # Chosen cable data
    cable = {
        "name": "434-AL1/56-ST1A",
        "diameter": 0.0288,  # m
        "area_full": 0.0004906,  # m2
        "St_wires": 7,
        "St_diameter": 0.0032, # m
        "St_area": 0.0000563, # m2
        "Al_wires": 54,
        "Al_diameter": 0.0032, # m
        "Al_area": 0.00043429, # m2
        "weight": 1.6413,  # kg/m
        "RTS": 133.59e3,  # N Rated tensile strength
        "young_mod": 70_491e6,  # [Pa] Young's modulus
        "Rdc20": 0.0666 / 1000,  # [Ω/m] DC resistance at 20°C
        "alpha_linear": 0.00403,  # teplotný koeficient odporu – lineárny
        "betta_square": 0.0000008,  # teplotný koeficient odporu – kvadratický
        "alpha_l": 19.3e-6,  # [1/K] Linear thermal expansion coefficient,
    }

    end_montage_table_temps = np.array([-30, -20, -10, -5, -5, -5, -5, -5, 0, 10, 20, 40, 60, 80])
    climate_montage_table_temps = np.array([-10, -5, 0, 10, 15, 17, 20, 22, 25, 27, 30, 35, 40])
    towers_Y = np.array([0,275,600,800,1300])


    # Basic cable parameters
    cable_calculations = CableParameters(cable, MAX_CABLE_TEMP, MAX_OUTSIDE_TEMP)
    R_AC80 = cable_calculations.AC80_resistance()
    print("AC80_resistance =", R_AC80)

    # Ampacity Calculations Full
    amp_calculations = AmpacityCalculation(SUN_POWER_OUTPUT, K_ABSORPTION, cable["diameter"], MAX_CABLE_TEMP, MAX_OUTSIDE_TEMP, SEA_HEIGHT, MIN_WIND_SPEED, cable["Al_diameter"], R_AC80)
    Ps = amp_calculations.sun_radiation_heat()
    print("Sun radiation heat =", Ps)
    Pc = amp_calculations.convection_heat()
    print("Convection heat =", Pc)
    Pr = amp_calculations.cable_radiation_heat()
    print("Cable radiation heat =", Pr)
    I = amp_calculations.ampacity(Ps, Pc, Pr)
    print("Ampacity = ", I)


    #Vibration
    montazne_tabulky_konecne = np.random.rand(6, 10)
    v_rozpatie = np.array([275, 275, 310, 320, 305, 298])
    v_sigma_h1 = np.array([0, 0, 0, 1000])
    v_h_alt = np.array([259.2, 254.3, 256.7, 256.2, 258.7, 234.2, 259.1])
    v_h_con = np.array([21.2, 22, 22, 25, 25, 25, 21.2])
    d = 27
    g_c = 9.81
    S = 431.2
    terrain_type = 3

    # main run
    # terrain_data = Overload_calculations([0,275,600,800,1300], cable_unit_weight, cable_diameter)
    # terrain_data.overload_result()
    # vibr = VibrationControl(montazne_tabulky_konecne, v_rozpatie, v_sigma_h1,v_h_alt, v_h_con, d, g_c, S, terrain_type)
    # vibr.run()

    
