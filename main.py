from constants import *
from ampacity import *
from cable_parameters import *
from montage_tables import *
from vibration_control import *

if __name__ == "__main__":
    # Chosen cable data
    cable = {
        "name": "434-AL1/56-ST1A",
        "diameter": 0.0288,  # m
        "area_full": 0.0004906,  # m2
        "St_wires": 7,
        "St_diameter": 0.0032,  # m
        "St_area": 0.0000563,  # m2
        "Al_wires": 54,
        "Al_diameter": 0.0032,  # m
        "Al_area": 0.00043429,  # m2
        "weight": 1.6413,  # kg/m
        "RTS": 133.59e3,  # N Rated tensile strength
        "young_mod": 70491,  # [MPa] Young's modulus
        "Rdc20": 0.0666 / 1000,  # [Ω/m] DC resistance at 20°C
        "alpha_linear": 0.00403,  # teplotný koeficient odporu – lineárny
        "betta_square": 0.0000008,  # teplotný koeficient odporu – kvadratický
        "alpha_l": 19.3e-6,  # [1/K] Linear thermal expansion coefficient,
    }
    towers_X = [0, 275, 600, 860, 1160, 1300]
    towers_H = [18.2, 24, 24, 24, 24, 18.20]
    towers_N = [12, 12, 12, 15, 18, 3]
    end_montage_table_temps = np.array([-30, -20, -10, -5, -5, -5, -5, -5, 0, 10, 20, 40, 60, 80])
    start_montage_table_temps = np.array([-10, -5, 0, 10, 15, 17, 20, 22, 25, 27, 30, 35, 40])


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

    #End Montage Table
    table_calculations = EndMontageTable(FILE_PATH, cable, end_montage_table_temps, ISOLATOR_LENGTH, towers_X, towers_H, towers_N, WIND_AREA, FROST_AREA, FROST_TYPE, TERRAIN_CATEGORY, TERRAIN_TYPE, RELIABILITY_LEVEL)
    table_calculations.load_terrain()
    table_calculations.overload_calculations()
    end_table = table_calculations.end_state_equation()
    table_calculations.write_end_table(end_table)
    step_table = table_calculations.step_montage_table(t_step=8760)
    table_calculations.write_step_table(step_table)
    init_table = table_calculations.init_montage_table(0, start_montage_table_temps)
    table_calculations.write_init_table(init_table)
    # Vibration
    vibration_calculations = VibrationControl(FILE_PATH, cable, end_table, towers_X, towers_H, towers_N, ISOLATOR_LENGTH, TERRAIN_TYPE)
    print(vibration_calculations.vibration_control_equations())
    vibration_calculations.minimal_height_check()

    
