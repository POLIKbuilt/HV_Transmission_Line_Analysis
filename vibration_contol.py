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
