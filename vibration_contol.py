import numpy as np
import matplotlib.pyplot as plt
from math import asinh, log

class VibrationControl:
    def __init__(self, montazne_tabulky_konecne, v_rozpatie, v_sigma_h1, v_h_alt, v_h_con, d, g_c, S, terrain_type):
        self.montazne_tabulky_konecne = montazne_tabulky_konecne
        self.v_rozpatie = v_rozpatie
        self.v_sigma_h1 = v_sigma_h1
        self.v_h_alt = v_h_alt
        self.v_h_con = v_h_con
        self.d = d
        self.g_c = g_c
        self.S = S
        self.terrain_type = terrain_type

def vibration_control_equations(self):
        self.y_coor = (self.v_rozpatie * self.d * 1e-3) / self.g_c

        self.T_0 = self.v_sigma_h1[3] * self.S
        self.x_coor = self.T_0 / self.g_c

        if self.terrain_type == 1:
            self.Eq_vib = (1.3 * 10 ** 27) / (self.T_0 / self.g_c) ** 8.3
            self.c_vib = 1000
        elif self.terrain_type == 2:
            self.Eq_vib = (5.4 * 10 ** 27) / (self.T_0 / self.g_c) ** 8.4
            self.c_vib = 1125
        elif self.terrain_type == 3:
            self.Eq_vib = (1.3 * 10 ** 28) / (self.T_0 / self.g_c) ** 8.4
            self.c_vib = 1225
        elif self.terrain_type == 4:
            self.Eq_vib = (1.1 * 10 ** 29) / (self.T_0 / self.g_c) ** 8.6
            self.c_vib = 1425

        # Условие
        if self.x_coor <= self.c_vib:
            self.oblast = 1
        else:
            self.oblast = 0
            for i in range(len(self.v_rozpatie)):
                if (self.y_coor[i] <= 1.5) and (self.y_coor[i] <= self.Eq_vib):
                    self.oblast = 2
                elif (self.y_coor[i] > 1.5) and (self.y_coor[i] > self.Eq_vib):
                    self.oblast = 3
        return self.oblast
