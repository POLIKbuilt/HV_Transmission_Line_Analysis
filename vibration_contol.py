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
    
    def compute_heights(self):
        self.c_80 = self.montazne_tabulky_konecne[5, -1]

        n = len(self.v_rozpatie)
        self.v_a_ciarka = np.zeros(n)
        self.v_h_par = np.zeros(n)
        self.v_x_min = np.zeros(n)
        self.j_x = np.zeros(n)

        for i in range(n):
            if i + 1 < len(self.v_h_alt):
                self.v_a_ciarka[i] = self.v_rozpatie[i] - (asinh(((self.v_h_alt[i + 1] + self.v_h_con[i + 1]) - (self.v_h_alt[i] + self.v_h_con[i])) / (2 * self.c_80 * np.sinh(self.v_rozpatie[i] / (2 * self.c_80)))) + self.v_rozpatie[i] / (2 * self.c_80)) * self.c_80
                self.v_h_par[i] = ((self.v_h_alt[i] + self.v_h_con[i]) - self.c_80 * np.cosh(self.v_a_ciarka[i] / self.c_80) + self.c_80)

        for i in range(n):
            if i + 1 < len(self.v_h_alt):
                pom_a = (self.v_h_alt[i + 1] - self.v_h_alt[i]) / self.v_rozpatie[i]
                self.v_x_min[i] = log(pom_a + np.sqrt(pom_a ** 2 + 1)) * self.c_80 + self.v_a_ciarka[i]

        for i in range(n):
            if i + 1 < len(self.v_h_alt):
                self.j_x[i] = (
                    self.c_80 * (np.cosh((self.v_x_min[i] - self.v_a_ciarka[i]) / self.c_80)) - self.c_80 + self.v_h_par[i] - (self.v_x_min[i] * (self.v_h_alt[i + 1] - self.v_h_alt[i]) / self.v_rozpatie[i] + self.v_h_alt[i]))
                
    def calculate_plot(self, x, f_x, g_x, f_x_12, setIndex, v_rozpatie):
        plt.figure()
        plt.plot(x, f_x, '-.', label='f(x)', linewidth=1.0)
        plt.plot(x, g_x, '--', label='g(x)')
        plt.plot(x, f_x_12, ':', label='f_12(x)', linewidth=1.25)
        plt.grid(True)
        plt.title(f'Розпяття {setIndex}')
        plt.ylabel("h [м]")
        plt.xlabel("a [м]")
        plt.xlim([0, v_rozpatie])
        plt.legend()
        plt.show()

    def run(self):
        self.vibro_equations()
        self.compute_heights()

        for setIndex in range(len(self.v_rozpatie)):
            x = np.arange(1, self.v_rozpatie[setIndex] + 1)

            g_x = self.c_80 * (
                np.cosh((x - self.v_a_ciarka[setIndex]) / self.c_80)
            ) - self.c_80 + self.v_h_par[setIndex]

            f_x = (
                x * (self.v_h_alt[setIndex + 1] - self.v_h_alt[setIndex])
                / self.v_rozpatie[setIndex]
                + self.v_h_alt[setIndex]
            )

            f_x_12 = f_x + 12

            self.calculate_plot(
                x, f_x, g_x, f_x_12, setIndex + 1, self.v_rozpatie[setIndex]
            )
