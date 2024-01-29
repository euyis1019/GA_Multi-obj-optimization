import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
a = -37 / 65**2
length = 130 + 70
width = 46 + 5
height = 37
R_user, L_user, W_user = 15.5, 104.9, 33.7

def S(x, y, R_user, L_user, W_user):
    return R_user - (4 * R_user / L_user**2 * (x - L_user/2)**2 - y**2 / W_user)

# Create a grid of x and y values
x = np.linspace(-100, length, 400)
y = np.linspace(-20, width, 400)
x, y = np.meshgrid(x, y)

# Calculate z values for the grid
z = S(x, y, R_user, L_user, W_user)

# Plotting
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, rstride=10, cstride=10, cmap='viridis', edgecolor='none')

# Drawing a square
square_x = np.array([L_user / 2 - R_user, L_user / 2 + R_user, L_user / 2 + R_user, L_user / 2 - R_user, L_user / 2 - R_user])
square_y = np.array([W_user / 2 - R_user, W_user / 2 - R_user, W_user / 2 + R_user, W_user / 2 + R_user, W_user / 2 - R_user])
square_z = S(square_x, square_y, R_user, L_user, W_user)  # Get the z coordinates from the surface function
ax.plot(square_x, square_y, square_z, label='Special Square', color='r')  # Plot the square

# Labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Arch Shape Surface with Special Square')

# Set the same scale for all three axes
ax.set_box_aspect([length, width, height])  # aspect ratio is 1:1:1

# Set the viewing angle for better visualization
ax.view_init(elev=40., azim=-60)

plt.show()
