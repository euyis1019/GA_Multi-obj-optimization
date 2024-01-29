import numpy as np
import plotly.graph_objects as go

# Constants
length = 130 + 70
width = 46 + 5
height = 37
R_user, L_user, W_user = 15.5, 104.9, 33.7

# S function from the user's code
def S(x, y, R_user, L_user, W_user):
    return R_user - (4*R_user/L_user**2 * (x - L_user/2)**2 - y**2/W_user)

# Create a grid of x and y values
x = np.linspace(0, length, 400)
y = np.linspace(0, width, 400)

x, y = np.meshgrid(x, y)

# Calculate z values for the grid
z = S(x, y, R_user, L_user, W_user)

# Create a 3D surface plot
fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='3D Surface plot of the function S(x, y)',
                  scene = dict(
                      xaxis_title='X AXIS',
                      yaxis_title='Y AXIS',
                      zaxis_title='S(x, y)'),
                  autosize=False,
                  width=800, height=800,
                  margin=dict(l=65, r=50, b=65, t=90))

# Show plot
fig.show()
