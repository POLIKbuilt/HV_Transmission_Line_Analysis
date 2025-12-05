# Basically calculation of overload on task provided cable
import csv
from constants import *
from scipy.constants import g
import numpy as np

class Overload_calculations:
    def __init__(self, chosen_X, cable_unit_weight, d_mm):
        self.file_path = FILE_PATH
        self.iso_length = ISOLATOR_LENGTH
        self.cable_weight = cable_unit_weight
        self.cable_d = d_mm / 1000
        self.posts_X = chosen_X
        self.posts_Y = []
        self.posts_H = []
        self.posts_N = [12, 12, 12, 12, 3]
        self.posts_A = []
        for i in range(len(chosen_X) - 1):
            x_diff = chosen_X[i+1] - chosen_X[i]
            self.posts_A.append(x_diff)

    def load_terrain(self):
        # csv read
        ter_X = []
        ter_Y = []
        with open(self.file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ter_X.append(float(row["X"]))
                ter_Y.append(float(row["Y"]))
            for i in range(len(self.posts_X)):
                for j in range(len(ter_X)):
                    if self.posts_X[i] == ter_X[j]:
                        self.posts_Y.append(round(ter_Y[j],3))
                if i == 0 or i == len(self.posts_X):
                    self.posts_H.append(18.20)
                else:
                    self.posts_H.append(24)

    def load_calculations(self):
        cable_g = self.cable_weight * g
        I_R50 = FROST_K1 + FROST_K2 * (self.cable_d * 1000)
        posts_H_con = []
        for i in range(len(self.posts_X)):
            if i == 0 or i == len(self.posts_X):
                h_diff = self.posts_H[i] + self.posts_N[i]
                posts_H_con.append(h_diff)
            else:
                h_diff = self.posts_H[i] + self.posts_N[i] - ISOLATOR_LENGTH
                posts_H_con.append(h_diff)
        H_con_average = sum(posts_H_con) / len(posts_H_con)
        k_h = (H_con_average / 10) ** 0.13
        wind_v_average = WIND_V_SPEC * C_DIR * C_0 * K_R * np.log(H_con_average / Z_0)
        turb_intz = 1 / (C_0 * np.log(H_con_average / Z_0))
        turb_responce = sum(self.posts_A)
        turb_lenth = 300 * ( (H_con_average / 200) ** (0.67 + 0.05 * np.log(Z_0)))
        frost_load = I_R50 * k_h * K_LC
        wind_q_average = 0.5 * P_AIR * wind_v_average ** 2
        wind_q_max = (1 + 7 * turb_intz) * wind_q_average
        k_response = 1 / (1 + (1.5 * (turb_responce / turb_lenth)))
        k_construction = (1 + 2 * K_P * turb_intz * np.sqrt(k_response + R)) / (1 + 7 * turb_intz) # k_p is unknown value for now check the tables
        wind_load = wind_q_max * self.cable_d * C_0 * k_construction
        frost_extreme_load = frost_load * frost_extreme_k
        wind_extreme_load = wind_load * wind_extreme_k
        frost_average_load = frost_load * frost_tau
        cable_d_frost_extreme = np.sqrt(self.cable_d + ((4 * frost_extreme_load) / (g * np.pi * 500)))
        cable_d_frost_average = np.sqrt(self.cable_d + ((4 * frost_average_load) / (g * np.pi * 500)))
        wind_average_load_extreme_frost = wind_q_max * cable_d_frost_extreme *
        wind_extreme_load_average_frost =

        # continue later...






    def overload_result(self):
        self.load_terrain()
        self.load_calculations()
        print("Chosen X for posts", self.posts_X)
        print("Chosen Y for posts", self.posts_Y)
        print("Chosen H for posts", self.posts_H)
        print("Chosen N for posts", self.posts_N)
        print("Chosen A for posts", self.posts_A)



    # posts_data = np.array([posts_X, posts_Y, posts_H, posts_N])

    # def geometrical_stats(self):


