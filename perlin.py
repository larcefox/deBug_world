import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np
import timeit
from noise import pnoise2
import noise


def perlin_list2(width=15, height=15, octaves=10, seed=1):
    noise = PerlinNoise(octaves, seed)

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

def perlin_list(width=15, height=15, octaves=10, persistence=1):

    coordinates_x = [i/width for i in range(width)]
    coordinates_y = [i/height for i in range(height)]
    
    pic = np.array([[pnoise2(i, j, octaves=1, persistence=0.5) for i in coordinates_x] for j in coordinates_y]) + \
        2 * np.array([[pnoise2(i * 0.5, j * 0.5, octaves=1, persistence=0.5) for i in coordinates_x] for j in coordinates_y]) + \
            4 * np.array([[pnoise2(i * 0.25, j * 0.25, octaves=1, persistence=0.5) for i in coordinates_x] for j in coordinates_y]) + \
                8 * np.array([[pnoise2(i * 0.125, j * 0.125, octaves=1, persistence=0.5) for i in coordinates_x] for j in coordinates_y])

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
    test_num = 10
    print(timeit.timeit('perlin_list()', setup='from __main__ import perlin_list', number=test_num))
    print(timeit.timeit('perlin_list2()', setup='from __main__ import perlin_list2', number=test_num))
    # help(noise)