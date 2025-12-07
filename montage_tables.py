import csv
import numpy as np
import pandas as pd
from scipy.constants import g

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
        self.w_fe = 0.266
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
        self.state_z = [1, 1, 1, 1, 0.9, 1.1, 1.05, 1, 1, 1, 1, 1, 1, 1]


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
                h_diff = self.towers_H[i] + self.towers_N[i] - self.b_i
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
        V_h = self.wind_area_speed * 1 * 1 * k_r * np.log(H_con_average / z_0)
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
        self.state_z[4] = z_I
        self.state_z[5] = z_W
        self.state_z[6] = z_wI
        self.state_z[7] = z_Wi
        print("-5 + N =", self.state_z[4])
        print("-5 + V =", self.state_z[5])
        print("-5 + Nv =", self.state_z[6])
        print("-5 + Vn =", self.state_z[7])

    def end_state_equation(self):
        # Montage table parameters
        sigma_state = [0] * len(self.temp_list)
        c_state = [0] * len(self.temp_list)
        f_vid_state = np.zeros((len(self.span_length), len(self.temp_list)))
        F_h_state = [0] * len(self.temp_list)
        RTS_state = [0] * len(self.temp_list)
        start_z = 1
        start_sigma_h = 52.1
        start_temp = -5
        delta_H = []
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
            part_D[i] = -(((gamma ** 2) * self.young_mod) / 24) * ((a_St * self.state_z[i]) ** 2)

            part_q[i] = -(part_B[i] ** 2) / 9
            part_r[i] = (-27 * part_D[i] - 2 * part_B[i] ** 3) / 54

            if (part_q[i] ** 3 + part_r[i] ** 2) > 0:
                sigma_state[i] = round(((part_r[i] - np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) + (part_r[i] + np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) - part_B[i] / 3), 3)
            else:
                sigma_state[i] = round(2 * (-part_q[i] ** 3) ** (1 / 6) * np.cos(np.arccos(part_r[i] / np.sqrt(-part_q[i] ** 3)) / 3) - part_B[i] / 3, 3)

        print("A:", part_A[10], "B:", part_B[10], "C:", part_C[10], "D:", part_D[10], "Q:", part_q[10], "R:", part_r[10], "sigma_state:", part_q[9] ** 3 + part_r[9] ** 2 )

        for i in range(len(self.temp_list)):
            c_state[i] = round(sigma_state[i] / (gamma * self.state_z[i]),3)
            F_h_state[i] = round(sigma_state[i] * (self.S / 1000),3)
            RTS_state[i] = round((F_h_state[i] * 1000) / self.rts * 100,3)
            for j in range(len(self.span_length)):
                A = self.span_length[j] / (2 * c_state[i])
                B = np.asinh(-delta_H[j] / self.span_length[j])
                C = np.asinh(-delta_H[j] / (2 * c_state[i] * np.sinh(self.span_length[j] / (2 * c_state[i]))))
                f_vid_state[j, i] = round(c_state[i] * (np.cosh(A + C) - np.cosh(B) - (-delta_H[j] / self.span_length[j]) * (A + C - B)),3)
        end_montage_table = np.vstack([self.temp_list, self.state_z, sigma_state, F_h_state, c_state, RTS_state, f_vid_state])
        return end_montage_table

    def write_end_table(self, table):
        excel_file_path = 'data/end_montage_table.xlsx'
        row_names = ["temp", "z", "sigma","F_h","c", "%RTS","a1","a2","a3","a4"]
        col_names = ["-30", "-20", "-10", "-5", "-5+N", "-5+V", "-5+Nv", "-5+Vn", "0", "10", "20", "40", "60", "80"]
        df = pd.DataFrame(table, index=row_names, columns=col_names)
        with pd.ExcelWriter(excel_file_path) as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        df1 = pd.read_excel(excel_file_path, sheet_name='Sheet1')
        print('End table:')
        print(df1)

    def step_montage_table(self, t_step):
        sigma1r_state = [0] * len(self.temp_list)
        c1r_state = [0] * len(self.temp_list)
        f1r_vid_state = np.zeros((len(self.span_length), len(self.temp_list)))
        F1r_state = [0] * len(self.temp_list)
        RTS1r_state = [0] * len(self.temp_list)
        start_z = 1
        start_sigma_h = 52.1
        start_temp = -5
        delta_H = []
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
        phi = 28.2 # mm/ km * h ** -1
        t_0 = 262800 # h
        T_EDT = 20 # C degrees for SR
        nu = 0.263
        if True:
            i = 10
            part_A[i] = 1
            part_B[i] = ((gamma ** 2 * self.young_mod) / 24) * (((a_St * start_z) / start_sigma_h) ** 2) + (self.alpha * self.young_mod * (self.temp_list[i] - start_temp)) - start_sigma_h
            part_C[i] = 0
            part_D[i] = -(((gamma ** 2) * self.young_mod) / 24) * ((a_St * self.state_z[i]) ** 2)

            part_q[i] = -(part_B[i] ** 2) / 9
            part_r[i] = (-27 * part_D[i] - 2 * part_B[i] ** 3) / 54

            if (part_q[i] ** 3 + part_r[i] ** 2) > 0:
                sigma_EDT = round(((part_r[i] - np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) + (part_r[i] + np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) - part_B[i] / 3), 3)
            else:
                sigma_EDT = round(2 * (-part_q[i] ** 3) ** (1 / 6) * np.cos(np.arccos(part_r[i] / np.sqrt(-part_q[i] ** 3)) / 3) - part_B[i] / 3, 3)

        k_w = 1.212 - 1.06 * self.w_fe
        k_EDS = round(0.0319 * ((100 * sigma_EDT * self.S) / self.rts) ** 1.15, 3)
        k_EDT = 0.842 + 0.0079 * T_EDT
        delta_T1r = - (1 / (self.alpha * 10e5)) * k_EDT * k_EDS * k_w * phi * ((t_0 ** nu) - (t_step ** nu))
        temp_xekv1 = [0] * len(self.temp_list)

        for i in range(len(self.temp_list)):
            temp_xekv1[i] = self.temp_list[i] + delta_T1r
            part_A[i] = 1
            part_B[i] = ((gamma ** 2 * self.young_mod) / 24) * (((a_St * start_z) / start_sigma_h) ** 2) + (self.alpha * self.young_mod * (temp_xekv1[i] - start_temp)) - start_sigma_h
            part_C[i] = 0
            part_D[i] = -(((gamma ** 2) * self.young_mod) / 24) * ((a_St * self.state_z[i]) ** 2)

            part_q[i] = -(part_B[i] ** 2) / 9
            part_r[i] = (-27 * part_D[i] - 2 * part_B[i] ** 3) / 54

            if (part_q[i] ** 3 + part_r[i] ** 2) > 0:
                sigma1r_state[i] = round(((part_r[i] - np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) + (part_r[i] + np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) - part_B[i] / 3), 3)
            else:
                sigma1r_state[i] = round(
                    2 * (-part_q[i] ** 3) ** (1 / 6) * np.cos(np.arccos(part_r[i] / np.sqrt(-part_q[i] ** 3)) / 3) - part_B[i] / 3, 3)

        for i in range(len(self.temp_list)):
            c1r_state[i] = round(sigma1r_state[i] / (gamma * self.state_z[i]), 3)
            F1r_state[i] = round(sigma1r_state[i] * (self.S / 1000), 3)
            RTS1r_state[i] = round((F1r_state[i] * 1000) / self.rts * 100, 3)
            for j in range(len(self.span_length)):
                A = self.span_length[j] / (2 * c1r_state[i])
                B = np.asinh(-delta_H[j] / self.span_length[j])
                C = np.asinh(-delta_H[j] / (2 * c1r_state[i] * np.sinh(self.span_length[j] / (2 * c1r_state[i]))))
                f1r_vid_state[j, i] = round(c1r_state[i] * (np.cosh(A + C) - np.cosh(B) - (-delta_H[j] / self.span_length[j]) * (A + C - B)), 3)
        step_montage_table = np.vstack([self.temp_list, temp_xekv1, self.state_z, sigma1r_state, F1r_state, c1r_state, RTS1r_state, f1r_vid_state])
        return step_montage_table

    def write_step_table(self, table):
        excel_file_path = 'data/step_montage_table.xlsx'
        row_names = ["temp", "temp_cor", "z", "sigma","F_h","c", "%RTS","a1","a2","a3","a4"]
        col_names = ["-30", "-20", "-10", "-5", "-5+N", "-5+V", "-5+Nv", "-5+Vn", "0", "10", "20", "40", "60", "80"]
        df = pd.DataFrame(table, index=row_names, columns=col_names)
        with pd.ExcelWriter(excel_file_path) as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        df1 = pd.read_excel(excel_file_path, sheet_name='Sheet1')
        print('Step table:')
        print(df1)

    def init_montage_table(self, t_step, start_temp_list):
        sigma1r_state = [0] * len(start_temp_list)
        c1r_state = [0] * len(start_temp_list)
        f1r_vid_state = np.zeros((len(self.span_length), len(start_temp_list)))
        F1r_state = [0] * len(start_temp_list)
        RTS1r_state = [0] * len(start_temp_list)
        start_z = 1
        start_sigma_h = 52.1
        start_temp = -5
        delta_H = []
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
        part_A = [0] * len(start_temp_list)
        part_B = [0] * len(start_temp_list)
        part_C = [0] * len(start_temp_list)
        part_D = [0] * len(start_temp_list)
        part_q = [0] * len(start_temp_list)
        part_r = [0] * len(start_temp_list)
        phi = 28.2 # mm/ km * h ** -1
        t_0 = 262800 # h
        T_EDT = 20 # C degrees for SR
        nu = 0.263
        if True:
            i = 10
            part_A[i] = 1
            part_B[i] = ((gamma ** 2 * self.young_mod) / 24) * (((a_St * start_z) / start_sigma_h) ** 2) + (self.alpha * self.young_mod * (self.temp_list[i] - start_temp)) - start_sigma_h
            part_C[i] = 0
            part_D[i] = -(((gamma ** 2) * self.young_mod) / 24) * ((a_St * self.state_z[i]) ** 2)

            part_q[i] = -(part_B[i] ** 2) / 9
            part_r[i] = (-27 * part_D[i] - 2 * part_B[i] ** 3) / 54

            if (part_q[i] ** 3 + part_r[i] ** 2) > 0:
                sigma_EDT = round(((part_r[i] - np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) + (part_r[i] + np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) - part_B[i] / 3), 3)
            else:
                sigma_EDT = round(2 * (-part_q[i] ** 3) ** (1 / 6) * np.cos(np.arccos(part_r[i] / np.sqrt(-part_q[i] ** 3)) / 3) - part_B[i] / 3, 3)

        k_w = 1.212 - 1.06 * self.w_fe
        k_EDS = round(0.0319 * ((100 * sigma_EDT * self.S) / self.rts) ** 1.15, 3)
        k_EDT = 0.842 + 0.0079 * T_EDT
        delta_T1r = - (1 / (self.alpha * 10e5)) * k_EDT * k_EDS * k_w * phi * ((t_0 ** nu) - (t_step ** nu))
        temp_xekv1 = [0] * len(start_temp_list)
        init_z = [0] * len(start_temp_list)

        for i in range(len(start_temp_list)):
            temp_xekv1[i] = start_temp_list[i] + delta_T1r
            init_z[i] = 1
            part_A[i] = 1
            part_B[i] = ((gamma ** 2 * self.young_mod) / 24) * (((a_St * start_z) / start_sigma_h) ** 2) + (self.alpha * self.young_mod * (temp_xekv1[i] - start_temp)) - start_sigma_h
            part_C[i] = 0
            part_D[i] = -(((gamma ** 2) * self.young_mod) / 24) * ((a_St * init_z[i]) ** 2)

            part_q[i] = -(part_B[i] ** 2) / 9
            part_r[i] = (-27 * part_D[i] - 2 * part_B[i] ** 3) / 54

            if (part_q[i] ** 3 + part_r[i] ** 2) > 0:
                sigma1r_state[i] = round(((part_r[i] - np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) + (part_r[i] + np.sqrt(part_q[i] ** 3 + part_r[i] ** 2)) ** (1 / 3) - part_B[i] / 3), 3)
            else:
                sigma1r_state[i] = round(
                    2 * (-part_q[i] ** 3) ** (1 / 6) * np.cos(np.arccos(part_r[i] / np.sqrt(-part_q[i] ** 3)) / 3) - part_B[i] / 3, 3)

        for i in range(len(start_temp_list)):
            c1r_state[i] = round(sigma1r_state[i] / (gamma * init_z[i]), 3)
            F1r_state[i] = round(sigma1r_state[i] * (self.S / 1000), 3)
            RTS1r_state[i] = round((F1r_state[i] * 1000) / self.rts * 100, 3)
            for j in range(len(self.span_length)):
                A = self.span_length[j] / (2 * c1r_state[i])
                B = np.asinh(-delta_H[j] / self.span_length[j])
                C = np.asinh(-delta_H[j] / (2 * c1r_state[i] * np.sinh(self.span_length[j] / (2 * c1r_state[i]))))
                f1r_vid_state[j, i] = round(c1r_state[i] * (np.cosh(A + C) - np.cosh(B) - (-delta_H[j] / self.span_length[j]) * (A + C - B)), 3)
        init_montage_table = np.vstack([start_temp_list, temp_xekv1, init_z, sigma1r_state, F1r_state, c1r_state, RTS1r_state, f1r_vid_state])
        return init_montage_table

    def write_init_table(self, table):
        excel_file_path = 'data/init_montage_table.xlsx'
        row_names = ["temp", "temp_cor", "z", "sigma","F_h","c", "%RTS","a1","a2","a3","a4"]
        col_names = [-10, -5, 0, 10, 15, 17, 20, 22, 25, 27, 30, 35, 40]
        df = pd.DataFrame(table, index=row_names, columns=col_names)
        with pd.ExcelWriter(excel_file_path) as writer:
            df.to_excel(writer, sheet_name='Sheet1')
        df1 = pd.read_excel(excel_file_path, sheet_name='Sheet1')
        print('Step table:')
        print(df1)