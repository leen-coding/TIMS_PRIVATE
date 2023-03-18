import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import numpy as np

from mpl_toolkits.mplot3d import Axes3D  

# fig = plt.figure()
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
# plt.subplot(projection='3d')

# 测试数据
a = np.loadtxt('C:\LeenWS\src\micro_control_pkg\scripts\gprfile_rbf_best.txt')
# 绘制图形
# a = a[400:500,:]
# ax.plot(x, y, z, label='parametric curve')
x = a[:, 0]
print(min(x))
print(max(x))
y = a[:, 1]
print(min(y))
print(max(y))
z = a[:, 2]
print(min(z))
print(max(z))

ax1.scatter(x, y, z, c='g', marker='o')
ax1.set_xlabel('$X$')
ax1.set_ylabel('$Y$')
ax1.set_zlabel('$Z$')
plt.show()

