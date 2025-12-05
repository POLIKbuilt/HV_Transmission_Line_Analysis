import numpy as np
import matplotlib.pyplot as plt
from math import asinh, log

# Завантаження вхідних даних
montazne_tabulky_konecne = np.random.rand(6, 10)  # Приклад даних таблиці
v_rozpatie = np.array([275, 275, 310, 320, 305, 298])  # Розпяття для прикладу
v_sigma_h1 = np.array([0, 0, 0, 1000])  # Приклад даних
v_h_alt = np.array([259.2, 254.3, 256.7, 256.2, 258.7, 234.2, 259.1])
v_h_con = np.array([21.2, 22, 22, 25, 25, 25, 21.2])
d = 27  # Діаметр
g_c = 9.81  # Гравітаційна стала
S = 431.2  # Приклад площі
typ_ter = 3   # Тип території

# Контроль вібрацій проводу
y_coor = (v_rozpatie * d * 1e-3) / g_c

T_0 = v_sigma_h1[3] * S
x_coor = T_0 / g_c

# Рівняння Eqvib
if typ_ter == 1:
    Eq_vib = (1.3 * 10 ** 27) / (T_0 / g_c) ** 8.3
    c_vib = 1000
elif typ_ter == 2:
    Eq_vib = (5.4 * 10 ** 27) / (T_0 / g_c) ** 8.4
    c_vib = 1125
elif typ_ter == 3:
    Eq_vib = (1.3 * 10 ** 28) / (T_0 / g_c) ** 8.4
    c_vib = 1225
elif typ_ter == 4:
    Eq_vib = (1.1 * 10 ** 29) / (T_0 / g_c) ** 8.6
    c_vib = 1425

# Перевірка умов
if x_coor <= c_vib:
    oblast = 1
else:
    oblast = 0
    for i in range(len(v_rozpatie)):
        if (y_coor[i] <= 1.5) and (y_coor[i] <= Eq_vib):
            oblast = 2
        elif (y_coor[i] > 1.5) and (y_coor[i] > Eq_vib):
            oblast = 3

# Визначення мінімальної висоти проводу
c_80 = montazne_tabulky_konecne[5, -1]

v_a_ciarka = np.zeros(len(v_rozpatie))
v_h_par = np.zeros(len(v_rozpatie))

for i in range(len(v_rozpatie)):
    if i + 1 < len(v_h_alt):
        v_a_ciarka[i] = v_rozpatie[i] - (
            asinh(((v_h_alt[i + 1] + v_h_con[i + 1]) - (v_h_alt[i] + v_h_con[i])) /
                  (2 * c_80 * np.sinh(v_rozpatie[i] / (2 * c_80)))) + v_rozpatie[i] / (2 * c_80)) * c_80
        v_h_par[i] = (v_h_alt[i] + v_h_con[i]) - c_80 * np.cosh(v_a_ciarka[i] / c_80) + c_80

# Відстань від першої стійки до мінімального наближення проводу до землі
v_x_min = np.zeros(len(v_rozpatie))

for i in range(len(v_rozpatie)):
    if i + 1 < len(v_h_alt):
        pom_a = (v_h_alt[i + 1] - v_h_alt[i]) / v_rozpatie[i]
        v_x_min[i] = log(pom_a + np.sqrt(pom_a ** 2 + 1)) * c_80 + v_a_ciarka[i]

# Мінімальна відстань проводу від землі
j_x = np.zeros(len(v_rozpatie))

for i in range(len(v_rozpatie)):
    if i + 1 < len(v_h_alt):
        j_x[i] = c_80 * (np.cosh((v_x_min[i] - v_a_ciarka[i]) / c_80)) - c_80 + v_h_par[i] - (
            v_x_min[i] * (v_h_alt[i + 1] - v_h_alt[i]) / v_rozpatie[i] + v_h_alt[i])

# Функція для розрахунку та побудови графіків
def calculate_plot(x, f_x, g_x, f_x_12, setIndex, v_rozpatie):
    plt.figure()
    plt.plot(x, f_x, '-.', label='f(x)', linewidth=1.0)
    plt.plot(x, g_x, '--', label='g(x)')
    plt.plot(x, f_x_12, ':', label='f_12(x)', linewidth=1.25)
    plt.grid(True)
    plt.title(f'Розпяття {setIndex}')
    plt.ylabel("h [м]")
    plt.xlabel("a [м]")
    plt.xlim([0, v_rozpatie])
    plt.legend()
    plt.show()

# Розрахунки для кожного розпяття
for setIndex in range(len(v_rozpatie)):
    x = np.arange(1, v_rozpatie[setIndex] + 1)
    g_x = c_80 * (np.cosh((x - v_a_ciarka[setIndex]) / c_80)) - c_80 + v_h_par[setIndex]
    f_x = x * (v_h_alt[setIndex + 1] - v_h_alt[setIndex]) / v_rozpatie[setIndex] + v_h_alt[setIndex]
    f_x_12 = f_x + 12

    calculate_plot(x, f_x, g_x, f_x_12, setIndex + 1, v_rozpatie[setIndex])
