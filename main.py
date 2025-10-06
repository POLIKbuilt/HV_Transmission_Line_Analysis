import csv
import  matplotlib.pyplot as plt
from current_demand import *

def load_terrain(file_path):
    # csv read
    ter_X = []
    ter_Y = []
    with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader.fieldnames)
        for row in reader:
            ter_X.append(float(row["X"]))
            ter_Y.append(float(row["Y"]))
        # plt.plot(ter_X,ter_Y)
        # plt.title("Terrain")
        # plt.show()


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

    result_array = []
    temp_array = range(35,80,1)
    for t_a in temp_array:
        Pc = Demand_Current.teplo_konvekcii(80, t_a, 400, 0.5, 30.2, 3.35)
        Pr = Demand_Current.teplo_radiation(30.2, t_a, 80)
        Ps = Demand_Current.teplo_ziarenia(1000, 30.2)
        result_array.append(round(Demand_Current.ampacita(Pc, Pr, Ps, Rdc20),3))
    plt.plot(temp_array, result_array)
    plt.title("Ampacy")
    plt.show()

    