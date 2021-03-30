import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np


def perlin_list(width, height, octaves=10, seed=1):
    noise = PerlinNoise(octaves, seed)
    # elevation[y][x] =    1 * noise(1 * nx, 1 * ny);
    #             +  0.5 * noise(2 * nx, 2 * ny);
    #             + 0.25 * noise(4 * nx, 4 * ny);

    coordinates_x = [i/width for i in range(width)]
    coordinates_y = [i/height for i in range(height)]
    
    pic = np.array([[noise([i, j]) for i in coordinates_x] for j in coordinates_y]) + \
        2 * np.array([[noise([i * 0.5, j * 0.5]) for i in coordinates_x] for j in coordinates_y]) + \
            4 * np.array([[noise([i * 0.25, j * 0.25]) for i in coordinates_x] for j in coordinates_y]) + \
                8 * np.array([[noise([i * 0.125, j * 0.125]) for i in coordinates_x] for j in coordinates_y])

    if __name__ == "__main__":
        plt.imshow(pic, cmap='gray')
        plt.savefig("mygraph.png")
    else:
        return pic

def mesh_3d(width, height, octaves=10, seed=1):
    
    noise = PerlinNoise(octaves, seed)
    coordinates_x = list(range(width))
    coordinates_y = list(range(height))
    return np.array([[(i, noise([i/width, j/height]), j) for i in coordinates_x] for j in coordinates_y]) + \
        np.array([[(i, noise([i/width * 0.5, j/height * 0.5]), j) for i in coordinates_x] for j in coordinates_y]) * 2 + \
            np.array([[(i, noise([i/width * 0.25, j/height * 0.25]), j) for i in coordinates_x] for j in coordinates_y]) * 4

if __name__ == "__main__":
    mesh = mesh_3d(15,3)