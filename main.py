import math
import numpy as np
import os
from scipy.constants import sigma, g

base_dir = os.path.dirname(__file__)

file_path = os.path.join(base_dir, 'data.csv')
# 'D:\IT\Transmission_Line_Analysis_VEV'

def load_terrain(file_path):
    with open(file_path, 'r') as csv:
        land_data = csv.reader()

def teplo_ziarenia(I_s, d):
    Ps = 0.5 * I_s * (d / 1000)
    return Ps

def teplo_konvekcii(t_s, t_a, h, v, d, d_s):
    t_f = 0.5 * (t_s - t_a)
    v_f = 0.0000132 + 0.000000015 * t_f
    lambda_f = 0.0242 + 0.000072 * t_f
    por = np.e ** (-0.000116 * h)
    R_e = por * v * ( (d / 1000) / v_f )
    R_s = d_s / ( 2 * ( d - d_s ) )
    print("rs", R_s)
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
    Nu90 = B1 * (R_e * N1)
    Nu45 = (0.42 + 0.58 * np.sin(45) ** 0.9 ) * v * Nu90
    print(Nu45)
    Nu_corr = 0.55 * Nu45
    Gr = ( (d / 1000) ** 3 * ( t_s - t_a ) * g ) / ( t_f + 273 ) * v_f ** 2
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
    Pc = np.pi * lambda_f * ( t_s - t_a ) * max(Nu_nat,Nu_corr,Nu45)
    return Pc

def teplo_radiation(d, t_a, t_s):
    Pr = np.pi * (d / 1000) * sigma  * 0.5 * ( (t_s + 273 ) ** 4 - (t_a + 273) ** 4)
    return  Pr

def ampacita(Pc, Pr, Ps, Rdc20):
    alpha_R = 0.00403
    betta_R = 0
    k_acdc = 1.080
    Rdc80 = (Rdc20 * (1 - alpha_R * (80 - 20) + betta_R * (80 - 20))) / 1000
    Rac80 = Rdc80 * k_acdc
    I_dov = np.sqrt((Pc + Pr - Ps) / Rac80)
    return I_dov


def txline_from_per_length(Zp, Yp, length_m):
    """
    Zp: complex series impedance per meter (ohm/m)
    Yp: complex shunt admittance per meter (siemens/m)
    length_m: length of line in meters
    Returns: dict with Zc, gamma, A,B,C,D
    """
    # characteristic impedance (ohm)
    Zc = np.sqrt(Zp / Yp)
    # propagation constant (neper/m + j rad/m)
    gamma = np.sqrt(Zp * Yp)
    # total series impedance and shunt admittance for the line
    Z_total = Zp * length_m
    Y_total = Yp * length_m
    # ABCD parameters for a uniform transmission line of length L:
    A = np.cosh(gamma * length_m)
    B = Zc * np.sinh(gamma * length_m)
    C = (1 / Zc) * np.sinh(gamma * length_m)
    D = A
    return {
        "Zc": Zc,
        "gamma": gamma,
        "Z_total": Z_total,
        "Y_total": Y_total,
        "A": A, "B": B, "C": C, "D": D
    }

if __name__ == "__main__":
    # Example inputs (replace with real per-length values)
    # Example per-km values (convert to per-meter below)
    R_per_km = 0.1        # ohm/km  (series resistance)
    L_per_mH_per_km = 1.0 # mH/km  (series inductance)
    C_nF_per_km = 10.0    # nF/km  (shunt capacitance)
    G_per_km = 0.0        # S/km   (shunt conductance, often ~0)
    f = 50.0              # Hz
    length_km = 100.0     # km

    # convert to per-meter
    R_p = R_per_km / 1000.0
    L_p = (L_per_mH_per_km * 1e-3) / 1000.0   # H/m
    C_p = (C_nF_per_km * 1e-9) / 1000.0       # F/m
    G_p = G_per_km / 1000.0

    omega = 2 * np.pi * f
    Zp = R_p + 1j * omega * L_p
    Yp = G_p + 1j * omega * C_p

    length_m = length_km * 1000.0

    result = txline_from_per_length(Zp, Yp, length_m)

    # Print key results with reasonable formatting
    def cmplx(x):
        return f"{x.real:.6g} {x.imag:+.6g}j"
    print("Characteristic impedance Zc (ohm):", cmplx(result["Zc"]))
    print("Propagation constant gamma (neper/m + j rad/m):", cmplx(result["gamma"]))
    print("ABCD parameters (A,B,C,D):")
    print(" A =", cmplx(result["A"]))
    print(" B =", cmplx(result["B"]))
    print(" C =", cmplx(result["C"]))
    print(" D =", cmplx(result["D"]))

    Rdc20 = 0.0608
    Pc = teplo_konvekcii(80, 35, 400, 0.5, 30.2, 3.35)
    Pr = teplo_radiation(30.2, 35, 80)
    Ps = teplo_ziarenia(1000, 30.2)

    print("For current demand result is:", ampacita(Pc, Pr, Ps, Rdc20))
    
    