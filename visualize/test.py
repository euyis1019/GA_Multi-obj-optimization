from matplotlib import pyplot as plt
import numpy as np
from numpy import cos,pi
# 生成测试数据
theta1 = np.linspace(0, 2*pi, 1000)
theta2 = np.linspace(0, 2*pi, 1000)
THETA1,THETA2 = np.meshgrid(theta1,theta2)
L1 = cos(THETA1)+cos(THETA2)
# 生成画布(两种形式)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Projection Space")
# ax = fig.add_subplot(111, projection="3d", title="plot title")
# 画三维折线图
ax.plot_surface(THETA1, THETA2, L1, color="red", linestyle="-")
# 设置坐标轴图标
ax.set_xlabel("theta1")
ax.set_ylabel("theta2")
ax.set_zlabel("L1")
# 图形显示
plt.show()
