# Basically calculation of overload on task provided cable
import csv
import numpy as np
import matplotlib.pyplot as plt

class Overload_calculations:
    posts_X = []
    posts_Y = []
    posts_H = []
    posts_N = []

    def load_terrain(self, file_path):
        # csv read
        ter_X = []
        ter_Y = []
        with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            print(reader.fieldnames)
            for row in reader:
                ter_X.append(float(row["X"]))
                ter_Y.append(float(row["Y"]))
            # plt.plot(ter_X, ter_Y)
            # plt.title("Terrain")
            # plt.show()

    posts_data = np.array([posts_X, posts_Y, posts_H, posts_N])

    def geometrical_stats(self):


