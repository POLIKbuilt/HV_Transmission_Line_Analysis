from current_demand import *
from overload_auto import *

if __name__ == "__main__":
    file_path = "data/data.csv"
    # terrain data input
    post_type = "Sudok"
    reliability_level = 2
    terrain_category = 2
    wind_area = 1
    terrain_type = 2
    frost_area = "I2"
    frost_type = "Wet Snow"
    T_env_max = 33 # C degrees
    V_min = 0.4 # m/s
    I_sun = 1097 # w/m
    k_abs = 0.5
    k_emis = 0.5
    h_sea = 400
    isolator_length = 5
    # cable data sheet input
    T_cab_max = 80 # C degree
    h_env = 12 # m
    L_dn = 5 # m
    ampacita_min = 2000 # A

    Rdc20 = 0.0608

    # main run
    terrain_data = Overload_calculations(file_path, isolator_length,[0,275,600,800,1300])
    terrain_data.overload_result()

    result_array = []
    temp_array = range(35,80,1)
    for t_a in temp_array:
        Pc = Demand_Current.teplo_konvekcii(80, t_a, 400, 0.5, 30.2, 3.35)
        Pr = Demand_Current.teplo_radiation(30.2, t_a, 80)
        Ps = Demand_Current.teplo_ziarenia(1000, 30.2)
        result_array.append(round(Demand_Current.ampacita(Pc, Pr, Ps, Rdc20),3))

    