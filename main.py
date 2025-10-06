from current_demand import *
from overload_auto import *
from constants import *

if __name__ == "__main__":
    # cable data sheet input
    cable_unit_weight = 1.4523 # kg/m
    T_cab_max = 80 # C degree
    h_env = 12 # m
    L_dn = 5 # m
    ampacita_min = 2000 # A

    Rdc20 = 0.0608

    # main run
    terrain_data = Overload_calculations(isolator_length,[0,275,600,800,1300], cable_unit_weight)
    terrain_data.overload_result()

    result_array = []
    temp_array = range(35,80,1)
    for t_a in temp_array:
        Pc = Demand_Current.teplo_konvekcii(80, t_a, 400, 0.5, 30.2, 3.35)
        Pr = Demand_Current.teplo_radiation(30.2, t_a, 80)
        Ps = Demand_Current.teplo_ziarenia(1000, 30.2)
        result_array.append(round(Demand_Current.ampacita(Pc, Pr, Ps, Rdc20),3))

    