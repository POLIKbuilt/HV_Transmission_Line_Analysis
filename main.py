import os
import csv
from current_demand import *

base_dir = os.path.dirname(__file__)

file_path = os.path.join(base_dir, 'data.csv')
# 'D:\IT\Transmission_Line_Analysis_VEV'

def load_terrain(file_path):
    # csv read
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
    return reader


if __name__ == "__main__":
    file_path = "data/data.csv"
    # project data input
    T_env_max = 33 # C degrees
    V_min = 0.4 # m/s
    I_sun = 1097 # w/m
    k_abs = 0.5
    k_emis = 0.5
    h_sea = 400
    # cable data sheet input
    T_cab_max = 80 # C degree
    h_env = 12 # m
    L_dn = 5 # m
    ampacita_min = 2000 # A

    Rdc20 = 0.0608

    # main run
    terrain_data = load_terrain(file_path)
    Pc = Demand_Current.teplo_konvekcii(80, 35, 400, 0.5, 30.2, 3.35)
    Pr = Demand_Current.teplo_radiation(30.2, 35, 80)
    Ps = Demand_Current.teplo_ziarenia(1000, 30.2)
    result = round(Demand_Current.ampacita(Pc, Pr, Ps, Rdc20),3)

    print("Current demand:", result)


    
    