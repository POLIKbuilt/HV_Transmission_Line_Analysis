import numpy as np
import os

base_dir = os.path.dirname(__file__)

file_path = os.path.join(base_dir, 'data.csv')
# 'D:\IT\Transmission_Line_Analysis_VEV'

def load_terrain(file_path):
    with open(file_path, 'r') as csv:
        land_data = csv.reader()

def

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
    
    
    