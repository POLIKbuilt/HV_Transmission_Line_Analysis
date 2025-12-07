import csv
from scipy.constants import g
import numpy as np
from constants import *

cable = {
        "name": "434-AL1/56-ST1A",
        "diameter": 0.0288,  # m
        "area_full": 0.0004906,  # m2
        "St_wires": 7,
        "St_diameter": 0.0032, # m
        "St_area": 0.0000563, # m2
        "Al_wires": 54,
        "Al_diameter": 0.0032, # m
        "Al_area": 0.00043429, # m2
        "weight": 1.6413,  # kg/m
        "RTS": 133.59e3,  # N Rated tensile strength
        "young_mod": 70491,  # [MPa] Young's modulus
        "Rdc20": 0.0666 / 1000,  # [Ω/m] DC resistance at 20°C
        "alpha_linear": 0.00403,  # teplotný koeficient odporu – lineárny
        "betta_square": 0.0000008,  # teplotný koeficient odporu – kvadratický
        "alpha_l": 19.3e-6,  # [1/K] Linear thermal expansion coefficient,
    }
towers_X = [0,275,600,800,1300]
end_montage_table_temps = np.array([-30, -20, -10, -5, -5, -5, -5, -5, 0, 10, 20, 40, 60, 80])


class EndMontageTable:
    def __init__(self, terrain_file, cable, temp_list, isolator_length, towers_X, wind_area, frost_area, frost_type, terrain_category, terrain_type, reliability_level):
        self.file = terrain_file
        self.d = cable["diameter"]
        self.w_c = cable["weight"]
        self.S = cable["area_full"] * 10e5
        self.alpha = cable["alpha_l"]
        self.young_mod = cable["young_mod"]
        self.rts = cable["RTS"]
        self.rts_control = 50 # %
        self.w_st = cable["St_area"]
        self.w_fe = self.w_st / self.w_c
        self.f_max = 12 # m
        self.temp_list = temp_list
        self.b_i = isolator_length
        self.W_i = 350 # kg
        self.A_i = 0.8 # m2
        if wind_area == 1:
            self.wind_area_speed = 24
        elif wind_area == 2:
            self.wind_area_speed = 26
        elif wind_area == 3:
            self.wind_area_speed = 30
        elif wind_area == 4:
            self.wind_area_speed = 33
        if frost_type == "WET SNOW":
            self.C_cl = 1
            self.p_i = 500
        self.frost_area = frost_area
        self.terrain_category = terrain_category
        self.terrain_type = terrain_type
        if reliability_level == 1:
            self.gamma_w = 1
            self.psi_w = 0.25
            self.gamma_I = 1
            self.psi_I = 0.35
        elif reliability_level == 2:
            self.gamma_w = 1.2
            self.psi_w = 0.25
            self.gamma_I = 1.25
            self.psi_I = 0.35
        elif reliability_level == 3:
            self.gamma_w = 1.4
            self.psi_w = 0.25
            self.gamma_I = 1.5
            self.psi_I = 0.35
        self.p_air = 1.25 # Pa

        self.towers_X = towers_X
        self.towers_Y = []
        self.towers_H = [18.2, 24, 24, 24, 18.20]
        self.towers_N = [12, 12, 12, 12, 3]
        self.towers_A = []
        self.n = len(towers_X)
        self.i = len(towers_X) - 1
        self.towers_N = [12, 12, 12, 12, 3]
        self.span_length = []
        for i in range(self.n - 1):
            self.span_length.append(self.towers_X[i + 1] - self.towers_X[i])


    def load_terrain(self):
        ter_X = []
        ter_Y = []
        with open(self.file, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ter_X.append(float(row["X"]))
                ter_Y.append(float(row["Y"]))
            for i in range(len(self.towers_X)):
                for j in range(len(ter_X)):
                    if self.towers_X[i] == ter_X[j]:
                        self.towers_Y.append(round(ter_Y[j],3))
        print(self.towers_Y)


    def overload_calculations(self):
        g_c = self.w_c * g
        if self.d < 0.03 and self.frost_area == "I2":
            I_R50 = 8.661 + 0.3653 * self.d * 1000
        elif self.d > 0.03 and self.frost_area == "I2":
            I_R50 =  17.53 + 0.070 * self.d * 1000
        self.towers_H_con = []
        for i in range(self.n):
            if i == 0 or i == self.n - 1:
                h_diff = self.towers_H[i] + self.towers_N[i]
                self.towers_H_con.append(h_diff)
            else:
                h_diff = self.towers_H[i] + self.towers_N[i] - ISOLATOR_LENGTH
                self.towers_H_con.append(h_diff)
        H_con_average = sum(self.towers_H_con) / len(self.towers_H_con)
        k_h = (H_con_average / 10) ** 0.13
        if self.terrain_category == 0:
            z_0 = 0.003
            k_r = 0.155
        elif self.terrain_category == 1:
            z_0 = 0.01
            k_r = 0.169
        elif self.terrain_category == 2:
            z_0 = 0.05
            k_r = 0.189
        elif self.terrain_category == 3:
            z_0 = 0.3
            k_r = 0.214
        elif self.terrain_category == 4:
            z_0 = 1
            k_r = 0.233
        V_h = self.wind_area_speed * 1 * 1 * k_r * np.log(H_con_average / Z_0)
        I_v = 1 / (1 * np.log(H_con_average / z_0))
        L_m = sum(self.span_length)
        L = 300 * ((H_con_average / 200) ** (0.67 + 0.05 * np.log(z_0)))
        I_50 = I_R50 * k_h * 1
        q_h = 0.5 * self.p_air * (V_h ** 2)
        q_p = (1 + 7 * I_v) * q_h # Pa
        B_response = 1 / (1 + (1.5 * (L_m / L)))
        K_p = 3 # k_p is unknown value for now check the tables
        R = 0
        G_construction = (1 + 2 * K_p * I_v * np.sqrt(B_response + R)) / (1 + 7 * I_v)
        q_wc = q_p * self.d * 1 * G_construction # N/m
        I_T = I_50 * self.gamma_I
        q_wT = q_wc * self.gamma_w
        I_3 = I_50 * self.psi_I
        D_I = np.sqrt(self.d ** 2 + ((4 * I_T) / (g * np.pi * self.p_i)))
        D_i = np.sqrt(self.d ** 2 + ((4 * I_3) / (g * np.pi * self.p_i)))
        q_wI3 = q_p * D_I * self.C_cl * G_construction * self.psi_w
        q_wIT = q_p * D_i * self.C_cl *  G_construction * (0.656 ** 2) * self.gamma_w # 0.656 is some B_I
        z_I = (I_T + g_c) / g_c
        z_W = (np.sqrt(q_wT ** 2 + g_c ** 2)) / g_c
        z_Wi = (np.sqrt((I_3 + g_c) ** 2 + q_wIT ** 2)) / g_c
        z_wI = (np.sqrt((I_T + g_c) ** 2 + q_wI3 ** 2)) / g_c
        print("-5 + N =", z_I)
        print("-5 + V =", z_W)
        print("-5 + Nv =", z_wI)
        print("-5 + Vn =", z_Wi)

    def state_equation(self):
        start_z = 1
        state_z = [1, 1, 1, 1, 0.9, 1.1, 1.05, 1, 1, 1, 1, 1, 1, 1]
        start_sigma_h = 52.1
        start_temp = -5
        delta_H = []
        sigma_state = [0] * len(self.temp_list)
        for i in range(self.n - 1):
            delta_H.append(self.towers_Y[i] + self.towers_H_con[i] - (self.towers_Y[i + 1] + self.towers_H_con[i + 1]))
        x = 0
        y = 0
        for i in range(self.n - 1):
            x += (self.span_length[i] ** 4) / np.sqrt(self.span_length[i] ** 2 + delta_H[i] ** 2)
            y += np.sqrt(self.span_length[i] ** 2 + delta_H[i] ** 2)
        a_St = np.sqrt(x / y)
        gamma = (self.w_c * g) / self.S
        # Parts of state equation
        part_A = [0] * len(self.temp_list)
        part_B = [0] * len(self.temp_list)
        part_C = [0] * len(self.temp_list)
        part_D = [0] * len(self.temp_list)
        part_q = [0] * len(self.temp_list)
        part_r = [0] * len(self.temp_list)
        for i in range(len(self.temp_list)):
            part_A[i] = 1
            part_B[i] = ((gamma ** 2 * self.young_mod) / 24) * (((a_St * start_z) / start_sigma_h) ** 2) + (self.alpha * self.young_mod * (self.temp_list[i] - start_temp)) - start_sigma_h
            part_C[i] = 0
            part_D[i] = -(((gamma ** 2) * self.young_mod) / 24) * ((a_St * state_z[i]) ** 2)

            part_q[i] = -(part_B[i] ** 2) / 9
            part_r[i] = (-27 * part_D[i] - 2 * part_B[i] ** 3) / 54

            if (part_q[i] ** 3 + part_r[i] ** 2) > 0:
                sigma_state[i] = round((part_r[i] - np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) + (part_r[i] + np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) - part_B[i] / 3, 3)
            else:
                sigma_state[i] = round(2 * (-part_q[i]) ** (1 / 6) * np.cos(np.arccos(part_r[i] / np.sqrt(-part_q[i] ** 3)) / 3) - part_B[i] / 3, 3)




table_calculations = EndMontageTable(FILE_PATH, cable, end_montage_table_temps, ISOLATOR_LENGTH, towers_X, WIND_AREA, FROST_AREA, FROST_TYPE, TERRAIN_CATEGORY, TERRAIN_TYPE, RELIABILITY_LEVEL)
table_calculations.load_terrain()
table_calculations.overload_calculations()
table_calculations.state_equation()