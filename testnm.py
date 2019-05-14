import numpy as np

x = "X"

a = np.array([[x, 0], [0, x]])


row_r1 = a[1, : ]
row_r2 = a[1:1, : ]

print(row_r1, row_r2.shape)


