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
    terrain_data = Overload_calculations([0,275,600,800,1300], cable_unit_weight, cable_diameter)
    terrain_data.overload_result()
    vibr = VibrationControl(montazne_tabulky_konecne, v_rozpatie, v_sigma_h1,v_h_alt, v_h_con, d, g_c, S, terrain_type)
    vibr.run()

    
