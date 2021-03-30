#!/home/larce/Documents/game1/game1_venv/bin/python
import numpy as np
from perlin import perlin_list
from loguru import logger


####

logger.add(
    "log_file.log",
    colorize=True,
    format="{time} {level} <green>{message}</green>",
    level="INFO",
    rotation="5 MB",
)

####
matrix_size = 50

eval = perlin_list(matrix_size, matrix_size)

coordinates = []

points = [[[x, y, z] for x, z in enumerate(row)] for y, row in enumerate(eval)]


for i in range(matrix_size):
    if i + 1 < matrix_size - 1:
        for j in range(matrix_size):
            
            if j + 1 < matrix_size - 1:
                coordinates.append(points[i][j])
                coordinates.append(points[i][j+1])
                coordinates.append(points[i+1][j])
            else:
                break

            if j + 1 < matrix_size - 1:
                coordinates.append(points[i][j+1])
                coordinates.append(points[i+1][j])
                coordinates.append(points[i+1][j+1])
            else:
                break




# Make data.

# x = points[:,0]
# y = points[:,1]
# z = points[:,2]

logger.info(len(coordinates))