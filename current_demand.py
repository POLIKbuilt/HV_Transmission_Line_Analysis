import numpy as np
from scipy.constants import sigma, g

class Demand_Current:
    def teplo_ziarenia(I_s, d):
        Ps = 0.5 * I_s * (d / 1000)
        return Ps

    def teplo_konvekcii(t_s, t_a, h, v, d, d_s):
        t_f = 0.5 * (t_s + t_a)
        v_f = 0.0000132 + 0.000000095 * t_f
        lambda_f = 0.0242 + 0.000072 * t_f
        por = np.e ** (-0.000116 * h)
        print("por", por)
        R_e = por * v * ( (d / 1000) / v_f )
        print("re", R_e)
        R_s = d_s / ( 2 * ( d - d_s ) )
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
        print("90", Nu90)
        Nu45 = (0.42 + 0.58 * (np.sin(45)) ** 0.90 ) * Nu90
        print("45", Nu45)
        Nu_corr = 0.55 * Nu90
        Gr = ((d / 1000) ** 3 * ( t_s - t_a ) * g ) / (( t_f + 273 ) * v_f ** 2)
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
        print(max(Nu_nat,Nu_corr,Nu45))
        Pc = np.pi * lambda_f * ( t_s - t_a ) * max(Nu_nat,Nu_corr,Nu45)
        return Pc

    def teplo_radiation(d, t_a, t_s):
        Pr = np.pi * (d / 1000) * sigma  * 0.5 * ( (t_s + 273 ) ** 4 - (t_a + 273) ** 4)
        return  Pr

    def ampacita(Pc, Pr, Ps, Rdc20):
        alpha_R = 0.00403
        k_acdc = 1.080
        Rdc80 = (Rdc20 * (1 - alpha_R * (80 - 20) )) / 1000
        Rac80 = Rdc80 * k_acdc
        I_dov = np.sqrt((Pc + Pr - Ps) / Rac80)
        return I_dov

if __name__ == "__main__":
    Rdc20 = 0.0608
    Pc = Demand_Current.teplo_konvekcii(80, 35, 400, 0.5, 30.2, 3.35)
    Pr = Demand_Current.teplo_radiation(30.2, 35, 80)
    Ps = Demand_Current.teplo_ziarenia(1000, 30.2)
    result = Demand_Current.ampacita(Pc, Pr, Ps, Rdc20)

    print("For current demand result is:", result)