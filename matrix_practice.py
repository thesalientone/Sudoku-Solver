import numpy as np


x1 = 1
y1 = 3
x2 = 4
y2 = 7

# x1 = 1
# y1 = 3
# x2 = 1
# y2 = 7

c = 10

point_array = np.array([[x1, y1], [x2, y2]])
c_array = np.array([[c], [c]])

print(point_array)
print(c_array)

ans = np.linalg.solve(point_array, c_array)

c_output = ans[0]*x1 + ans[1]*y1
print(c)

print(ans)