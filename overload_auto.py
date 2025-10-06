# Basically calculation of overload on task provided cable
import numpy as np

class Overload_calculations:
    def load_terrain(file_path):
        # csv read
        ter_X = []
        ter_Y = []
        with open(file_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            print(reader.fieldnames)
            for row in reader:
                ter_X.append(float(row["X"]))
                ter_Y.append(float(row["Y"]))
            plt.plot(ter_X, ter_Y)
            plt.title("Terrain")
            plt.show()

    def geometrical_stats(self):
        posts_parameters = np.array([[],[],[]])

