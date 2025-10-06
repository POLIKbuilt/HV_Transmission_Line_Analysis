import os
import csv
from current_demand import *

base_dir = os.path.dirname(__file__)

file_path = os.path.join(base_dir, 'data.csv')
# 'D:\IT\Transmission_Line_Analysis_VEV'

def load_terrain(file_path):
    with open(file_path, 'r') as csv:
        land_data = csv.reader()



if __name__ == "__main__":
    with open("data/data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
    Rdc20 = 0.0608
    Pc = Demand_Current.teplo_konvekcii(80, 35, 400, 0.5, 30.2, 3.35)
    Pr = Demand_Current.teplo_radiation(30.2, 35, 80)
    Ps = Demand_Current.teplo_ziarenia(1000, 30.2)
    result = round(Demand_Current.ampacita(Pc, Pr, Ps, Rdc20),3)

    print("Current demand:", result)


    
    