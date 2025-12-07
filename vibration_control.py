import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import g

class VibrationControl:
    def __init__(self, terrain_file, cable, end_montage_table, towers_X, towers_H, towers_N, isolator_length, terrain_type):
        self.file = terrain_file
        self.d = cable["diameter"]
        self.S = cable["area_full"]
        self.w_c = cable["weight"]
        self.b_i = isolator_length
        self.table = end_montage_table
        self.terrain_type = terrain_type
        self.g_c = self.w_c * g
        self.towers_X = towers_X
        self.span_length = []
        for i in range(len(towers_X) - 1):
            self.span_length.append(towers_X[i + 1] - towers_X[i])
        self.towers_Y = []
        self.towers_H = towers_H
        self.towers_N = towers_N
        self.towers_H_con = []
        for i in range(len(towers_X)):
            if i == 0 or i == len(towers_X) - 1:
                h_diff = self.towers_H[i] + self.towers_N[i]
                self.towers_H_con.append(h_diff)
            else:
                h_diff = self.towers_H[i] + self.towers_N[i] - self.b_i
                self.towers_H_con.append(h_diff)

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

    def vibration_control_equations(self):
        self.load_terrain()
        self.oblast = [0] * len(self.span_length)
        self.y_coor = [0] * len(self.span_length)
        for i in range(len(self.span_length) - 1):
            self.y_coor[i] = (self.span_length[i] * self.d) / self.g_c
        self.T_0 = self.table[3][3] * self.S
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
        for i in range(len(self.span_length) - 1):
            if self.x_coor <= self.c_vib:
                self.oblast[i] = 1
            else:
                self.oblast[i] = 0
                for j in range(len(self.span_length)):
                    if (self.y_coor[j] <= 1.5) and (self.y_coor[j] <= self.Eq_vib):
                       self.oblast[i] = 2
                    elif (self.y_coor[j] > 1.5) and (self.y_coor[j] > self.Eq_vib):
                        self.oblast[i] = 3
        vibrations_table = np.vstack([self.span_length, self.oblast])
        return print(vibrations_table)


    def compute_heights(self):
        self.c_80 = self.table[4][13]

        self.a_node = [0] * len(self.span_length)
        self.h_node = [0] * len(self.span_length)
        self.x_min = [0] * len(self.span_length)
        self.j_x_min = [0] * len(self.span_length)

        for i in range(len(self.span_length)):
            if i + 1 < len(self.towers_Y):
                self.a_node[i] = self.span_length[i] - (np.asinh(((self.towers_Y[i + 1] + self.towers_H_con[i + 1]) - (self.towers_Y[i] + self.towers_H_con[i])) / (2 * self.c_80 * np.sinh(self.span_length[i] / (2 * self.c_80)))) + self.span_length[i] / (2 * self.c_80)) * self.c_80
                self.h_node[i] = ((self.towers_Y[i] + self.towers_H_con[i]) - self.c_80 * np.cosh(self.a_node[i] / self.c_80) + self.c_80)

        for i in range(len(self.span_length)):
            if i + 1 < len(self.towers_Y):
                X = (self.towers_Y[i + 1] - self.towers_Y[i]) / self.span_length[i]
                self.x_min[i] = np.log(X + np.sqrt(X ** 2 + 1)) * self.c_80 + self.a_node[i]

        for i in range(len(self.span_length)):
            if i + 1 < len(self.towers_Y):
                self.j_x_min[i] = (
                    self.c_80 * (np.cosh((self.x_min[i] - self.a_node[i]) / self.c_80)) - self.c_80 + self.h_node[i] - (self.x_min[i] * (self.towers_Y[i + 1] - self.towers_Y[i]) / self.span_length[i] + self.towers_Y[i]))

                
    def calculate_plot(self, x, f_x, g_x, f_x_12, setIndex, spans):
        plt.figure()
        plt.plot(x, f_x, '-.', label='f(x) - terrain', linewidth=1.0)
        plt.plot(x, g_x, '--', label='g(x) - cable')
        plt.plot(x, f_x_12, ':', label='f_12(x) - min', linewidth=1.25)
        plt.grid(True)
        plt.title(f'Span {setIndex}')
        plt.ylabel("h [m]")
        plt.xlabel("a [m]")
        plt.xlim([0, spans])
        plt.legend()
        plt.show()

    def minimal_height_check(self):
        '''
        self.compute_heights()
        for setIndex in range(len(self.span_length)):
            x = np.arange(1, self.span_length[setIndex] + 1)
            g_x = self.c_80 * (np.cosh((x - self.a_node[setIndex]) / self.c_80)) - self.c_80 + self.h_node[setIndex]
            f_x = (x * (self.towers_Y[setIndex + 1] - self.towers_Y[setIndex]) / self.span_length[setIndex] + self.towers_Y[setIndex])
            f_x_12 = f_x + 12
            self.calculate_plot(x, f_x, g_x, f_x_12, setIndex + 1, self.span_length[setIndex])
        '''
        self.compute_heights()

        # Continuous X cursor
        x_offset = 0

        # Storage for full continuous curves
        X_all = []
        f_all = []
        g_all = []
        f12_all = []

        for i in range(len(self.span_length)):
            span = self.span_length[i]

            # Local x for this span
            x_local = np.arange(0, span)

            # Global continuous x
            x_global = x_local + x_offset

            # Compute curves
            g_x = self.c_80 * (np.cosh((x_local - self.a_node[i]) / self.c_80)) - self.c_80 + self.h_node[i]
            f_x = x_local * (self.towers_Y[i + 1] - self.towers_Y[i]) / span + self.towers_Y[i]
            f_x_12 = f_x + 12

            # Append to global lists
            X_all.append(x_global)
            f_all.append(f_x)
            g_all.append(g_x)
            f12_all.append(f_x_12)

            # Move offset for next span
            x_offset += span

        # Convert lists to single arrays
        X_all = np.concatenate(X_all)
        f_all = np.concatenate(f_all)
        g_all = np.concatenate(g_all)
        f12_all = np.concatenate(f12_all)

        # Plot all spans as continuous curves
        plt.figure(figsize=(12, 6))
        plt.plot(X_all, f_all, '-.', label='f(x) - terrain', linewidth=1.0)
        plt.plot(X_all, g_all, '--', label='g(x) - cable')
        plt.plot(X_all, f12_all, ':', label='f_12(x) - min', linewidth=1.5)

        plt.grid(True)
        plt.title("Continuous Profile Across All Spans")
        plt.xlabel("a [m]")
        plt.ylabel("h [m]")
        plt.legend()
        plt.tight_layout()
        plt.show()


