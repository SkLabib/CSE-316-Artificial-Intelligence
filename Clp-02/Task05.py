import numpy as np
matrix = np.random.randint(1, 101, size=(5, 5))
RowSums = matrix.sum(axis=1)
print("Matrix:")
print(matrix)
print("\nRow-wise sums:")
print(RowSums)
