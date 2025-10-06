from constants import *
from current_demand import *
from overload_auto import *

if __name__ == "__main__":
    # cable data sheet input
    cable_unit_weight = 1.4523 # kg/m
    cable_diameter = 30.2 # mm
    T_cab_max = 80 # C degree
    h_env = 12 # m
    L_dn = 5 # m
    ampacita_min = 2000 # A

    Rdc20 = 0.0608

    # main run
    terrain_data = Overload_calculations([0,275,600,800,1300], cable_unit_weight, cable_diameter)
    terrain_data.overload_result()


    