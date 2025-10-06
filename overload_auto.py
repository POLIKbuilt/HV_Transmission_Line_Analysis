# Basically calculation of overload on task provided cable
import csv
import numpy as np

class Overload_calculations:
    def __init__(self, file_path, chosen_X):
        self.file_path = file_path
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


    def overload_result(self):
        print("Chosen X for posts", self.posts_X)
        print("Chosen Y for posts", self.posts_Y)



    # posts_data = np.array([posts_X, posts_Y, posts_H, posts_N])

    # def geometrical_stats(self):


