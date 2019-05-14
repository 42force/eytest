import numpy as np

n = 10
a = [[0] * n for i in range(n)]
x = "X"
for i in range(n):
    for j in range(n):
        if i > j:
                a[i][j] = x
        elif i < j:
                a[i][j] = 0
       
for row in a:
    print(' '.join([str(elem) for elem in row]))