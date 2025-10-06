# Basically calculation of overload on task provided cable
import csv
from constants import *
from scipy.constants import g
import numpy as np

class Overload_calculations:
    def __init__(self, iso_length, chosen_X, cable_unit_weight):
        self.file_path = FILE_PATH
        self.iso_length = iso_length
        self.cable_weight = cable_unit_weight
        self.posts_X = chosen_X
        self.posts_Y = []
        self.posts_H = []
        self.posts_N = []

    def load_terrain(self):
        # csv read
        ter_X = []
        ter_Y = []
        with open(self.file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ter_X.append(float(row["X"]))
                ter_Y.append(float(row["Y"]))
            for i in range(len(self.posts_X)):
                for j in range(len(ter_X)):
                    if self.posts_X[i] == ter_X[j]:
                        self.posts_Y.append(round(ter_Y[j],3))
                self.posts_N.append(0)
                if i == 0 or i == len(self.posts_X):
                    self.posts_H.append(18.20)
                else:
                    self.posts_H.append(24)

    def load_calculations(self):
        cable_g = self.cable_weight * g



    def overload_result(self):
        self.load_terrain()
        print("Chosen X for posts", self.posts_X)
        print("Chosen Y for posts", self.posts_Y)
        print("Chosen H for posts", self.posts_H)
        print("Chosen N for posts", self.posts_N)



    # posts_data = np.array([posts_X, posts_Y, posts_H, posts_N])

    # def geometrical_stats(self):


