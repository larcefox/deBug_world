import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np

noise = PerlinNoise(octaves=10, seed=1)

def perlin_list(width, height):

    pic = np.array([[noise([i/width, j/height]) for j in range(width)] for i in range(height)])

    if __name__ == "__main__":
        plt.imshow(pic, cmap='gray')
        plt.savefig("mygraph.png")
    else:
        return pic


if __name__ == "__main__":
    perlin_list(100, 100)