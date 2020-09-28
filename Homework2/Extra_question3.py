import numpy as np
x = np.array([[0, 10, 20], [20, 30, 40]])
print("Original array: ")
print(x)
indices = np.argwhere(x > 10)
arr = np.where(x>10)
overall = np.vstack((arr[0], arr[1], x[x>10])).transpose()
# values = x[indices]
print("results: ")
print(overall)
