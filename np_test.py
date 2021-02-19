import numpy as np

a = np.random.rand(3, 5)
b = np.zeros((3, 5))
a *= b
print(a, b)

