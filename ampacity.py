import numpy as np
from scipy.constants import sigma, g
from constants import *


class AmpacityCalculation:
    def __init__(self, sun_power_input, k_absorption, cable_diameter_full, cable_temp, outside_temp, sea_height, wind_speed, outer_cable_diameter, DC20_cable_resistance):
        self.I_s = sun_power_input
        self.k_abs = k_absorption
        self.d = cable_diameter_full
        self.t_s = cable_temp
        self.t_a = outside_temp
        self.h = sea_height
        self.v = wind_speed
        self.d_s = outer_cable_diameter
        self.Rdc20 = DC20_cable_resistance

    def sun_radiation_heat(self):
        Ps = self.k_abs * self.I_s * (self.d / 1000)
        return Ps

    def convection_heat(self):
        t_f = 0.5 * (self.t_s + self.t_a)
        v_f = 0.0000132 + 0.000000095 * t_f
        lambda_f = 0.0242 + 0.000072 * t_f
        por = np.e ** (-0.000116 * self.h)
        R_e = por * self.v * ( (self.d / 1000) / v_f )
        R_s = self.d_s / ( 2 * (self.d - self.d_s ) )
        if R_s < 0.05 and R_e > 100 and R_e < 2650:
            B1 = 0.691
            N1 = 0.471
        elif R_s < 0.05 and R_e > 2650 and R_e < 50000:
            B1 = 0.178
            N1 = 0.633
        elif R_s > 0.05 and R_e > 100 and R_e < 2650:
            B1 = 0.691
            N1 = 0.471
        elif R_s > 0.05 and R_e > 2650 and R_e < 50000:
            B1 = 0.048
            N1 = 0.8
        Nu90 = B1 * (R_e ** N1)
        Nu45 = (0.42 + 0.58 * (np.sin(45)) ** 0.90 ) * Nu90
        Nu_corr = 0.55 * Nu90
        Gr = ((self.d / 1000) ** 3 * (self.t_s - self.t_a ) * g ) / (( t_f + 273 ) * v_f ** 2)
        Pr = 0.715 - 0.00025 * t_f
        sumar = Gr * Pr
        if sumar > 0 and sumar < 0.1:
            A2 = 0.675
            M2 = 0.058
        elif sumar > 0.1 and sumar < 100:
            A2 = 1.020
            M2 = 0.148
        elif sumar > 100 and sumar < 1000:
            A2 = 0.850
            M2 = 0.188
        elif sumar > 1000 and sumar < 10 ** 7:
            A2 = 0.480
            M2 = 0.250
        else:
            A2 = 0.125
            M2 = 0.333
        Nu_nat = A2 * (Gr * Pr) ** M2
        Pc = np.pi * lambda_f * (self.t_s - self.t_a ) * max(Nu_nat,Nu_corr,Nu45)
        return Pc

    def cable_radiation_heat(self):
        Pr = np.pi * (self.d / 1000) * sigma  * 0.5 * ( (self.t_s + 273 ) ** 4 - (self.t_a + 273) ** 4)
        return  Pr

    def ampacity(self, Ps, Pc, Pr):
        alpha_R = 0.00403
        k_acdc = 1.080
        Rdc80 = (self.Rdc20 * (1 - alpha_R * (80 - 20) )) / 1000
        Rac80 = Rdc80 * k_acdc
        I_dov = np.sqrt((Pc + Pr - Ps) / Rac80)
        return I_dov

amp_calculations = AmpacityCalculation(SUN_POWER_OUTPUT, K_ABSORPTION, 21.84, MAX_CABLE_TEMP, MAX_OUTSIDE_TEMP, SEA_HEIGHT, MIN_WIND_SPEED, 3.45, 0.1188)
Ps = amp_calculations.sun_radiation_heat()
print("Sun radiation heat =", Ps)
Pc = amp_calculations.convection_heat()
print("Convection heat =", Pc)
Pr = amp_calculations.cable_radiation_heat()
print("Cable radiation heat =", Pr)
I = amp_calculations.ampacity(Ps, Pc, Pr)
print("Ampacity = " , I)