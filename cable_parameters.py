class CableParameters:
    def __init__(self, cable, cable_temp, outside_temp):
        self.cable_name = cable["name"]
        self.d = cable["diameter"]
        self.S = cable["area_full"]
        self.St_n = cable["St_wires"]
        self.St_d = cable["St_diameter"]
        self.Al_n = cable["Al_wires"]
        self.Al_d = cable["Al_diameter"]
        self.m = cable["weight"]
        self.RTS = cable["RTS"]
        self.young_mod = cable["young_mod"]
        self.Rdc20 = cable["Rdc20"]
        self.alpha_r = cable["alpha_linear"]
        self.beta_r = cable["betta_square"]
        self.alpha_l = cable["alpha_l"]
        self.t_s = cable_temp
        self.t_a = outside_temp


    def AC80_resistance(self):
        Rdc80 = (self.Rdc20 * (1 + self.alpha_r * (80 - 20) + self.beta_r * ((80 - 20) ** 2)))
        print("Rdc80: ", Rdc80)
        if self.Al_n <= 2:
            if self.d < 20:
                k_ACDC = 1.005
            elif 20 <= self.d <= 25:
                k_ACDC = 1.01
            else:
                k_ACDC = 1.025
        else:
            if 20 < self.d <= 25:
                k_ACDC = 1.04
            elif 25 < self.d <= 30:
                k_ACDC = 1.05
            else:
                k_ACDC = 1.08
        Rac80 = Rdc80 * k_ACDC
        return Rac80
