import numpy as np
import pandas as pd
from math import sqrt, sinh, cosh, asinh, acos

# Вхідні дані (приклад)
v_theta = np.array([-30, -20, -10, -5, -5, -5, -5, -5, 0, 10, 20, 40, 60, 80])
v_z = np.array([1, 1, 1, 1, 0.9, 1.1, 1.05, 1, 1, 1, 1, 1, 1, 1])  # Заміна z_I, z_W тощо
v_sigma_h = np.zeros(len(v_theta))

theta_ref = v_theta[3]
z_ref = 1
v_sigma_h[3] = 60
sigma_h_ref = v_sigma_h[3]

# Приклад вхідних даних для v_rozpatie, v_h_alt, v_h_con
v_rozpatie = np.array([100, 150, 200, 250, 300])  # Замінити на реальні значення
v_h_alt = np.array([10, 15, 20, 25, 30, 35])  # Замінити на реальні значення
v_h_con = np.array([0, 1, 2, 3, 4, 5])  # Замінити на реальні значення

E_AlFe = 67100  # Модуль пружності
S = 1  # Площа перерізу
RTS = 121300  # Міцність на розрив
omega_c = 1.8655  # Одинична вага
alpha_roztaz = 1.94e-5  # Температурний коефіцієнт розширення

# Обчислення
v_delta_h = np.zeros(len(v_rozpatie))
for i in range(len(v_rozpatie) - 1):
    v_delta_h[i] = v_h_alt[i] + v_h_con[i] - v_h_alt[i + 1] - v_h_con[i + 1]

pom_a = 0
pom_b = 0
for i in range(len(v_rozpatie)):
    pom_a += (v_rozpatie[i] ** 4) / sqrt(v_rozpatie[i] ** 2 + v_delta_h[i] ** 2)
    pom_b += sqrt(v_rozpatie[i] ** 2 + v_delta_h[i] ** 2)

a_st = sqrt(pom_a / pom_b)

gamma = (omega_c * 9.81) / S

# Станові рівняння
v_A = np.zeros(len(v_sigma_h))
v_B = np.zeros(len(v_sigma_h))
v_C = np.zeros(len(v_sigma_h))
v_D = np.zeros(len(v_sigma_h))
v_q = np.zeros(len(v_sigma_h))
v_r = np.zeros(len(v_sigma_h))

for i in range(len(v_theta)):
    v_A[i] = 1
    v_B[i] = ((gamma ** 2 * E_AlFe) / 24) * ((a_st * z_ref) / sigma_h_ref) ** 2 + (
                alpha_roztaz * E_AlFe * (v_theta[i] - theta_ref)) - sigma_h_ref
    v_C[i] = 0
    v_D[i] = -((gamma ** 2 * E_AlFe) / 24) * (a_st * v_z[i]) ** 2

    v_q[i] = -v_B[i] ** 2 / 9
    v_r[i] = (-27 * v_D[i] - 2 * v_B[i] ** 3) / 54

    if (v_q[i] ** 3 + v_r[i] ** 2) > 0:
        v_sigma_h[i] = (v_r[i] - np.sqrt(v_q[i] ** 3 + v_r[i] ** 2)) ** (1 / 3) + (
                    v_r[i] + np.sqrt(v_q[i] ** 3 + v_r[i] ** 2)) ** (1 / 3) - v_B[i] / 3
    else:
        v_sigma_h[i] = 2 * (-v_q[i]) ** (1 / 6) * np.cos(np.arccos(v_r[i] / np.sqrt(-v_q[i] ** 3)) / 3) - v_B[i] / 3

# Параметри для остаточних монтажних таблиць
v_c = np.zeros(len(v_sigma_h))
v_Fh = np.zeros(len(v_sigma_h))
v_pRTS = np.zeros(len(v_sigma_h))
v_f_vid = np.zeros((len(v_rozpatie), len(v_sigma_h)))

for i in range(len(v_sigma_h)):
    v_Fh[i] = v_sigma_h[i] * S
    v_pRTS[i] = v_Fh[i] / RTS * 100
    v_c[i] = v_sigma_h[i] / (gamma * v_z[i])

    for j in range(len(v_rozpatie)):
        pom_a = v_rozpatie[j] / (2 * v_c[i])
        pom_b = 2 * v_c[i] * sinh(v_rozpatie[j] / (2 * v_c[i]))
        pom_c = asinh(-v_delta_h[j] / v_rozpatie[j])
        pom_d = asinh(-v_delta_h[j] / (2 * v_c[i] * sinh(v_rozpatie[j] / (2 * v_c[i]))))
        v_f_vid[j, i] = v_c[i] * (
                    cosh(pom_a + pom_d) - cosh(pom_c) - (-v_delta_h[j] / v_rozpatie[j]) * (pom_a + pom_d - pom_c))

# Остаточні монтажні таблиці
montazne_tabulky_konecne = np.vstack([v_theta, v_z, v_sigma_h, v_Fh, v_c, v_pRTS, v_f_vid])

# Збереження таблиць до Excel
excel_file_path = 'montazne_tabulky_all.xlsx'
with pd.ExcelWriter(excel_file_path) as writer:
    pd.DataFrame(montazne_tabulky_konecne).to_excel(writer, sheet_name='Sheet1')

print('Update OK.')

# Читання з Excel файлів
df1 = pd.read_excel(excel_file_path, sheet_name='Sheet1')
print('Кінцеві таблиці:')
print(df1)

# Збереження до CSV
np.savetxt("montazne_tabulky_konecne.csv", montazne_tabulky_konecne, delimiter=",")
