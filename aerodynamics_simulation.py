import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define cube geometry
length = 1.0  # Length of one side of the cube

# Discretize the cube
num_points = 20  # Number of points along each side
x_points, y_points, z_points = np.meshgrid(np.linspace(0, length, num_points),
                                           np.linspace(0, length, num_points),
                                           np.linspace(0, length, num_points))

# Freestream conditions
freestream_velocity = 50  # m/s
angle_of_attack = 0  # degrees

# Function to calculate lift and drag coefficients using potential flow theory
def potential_flow_aero_coefficients(angle_of_attack, x_points, y_points, z_points):
    # Angle of attack in radians
    alpha_rad = np.radians(angle_of_attack)
    
    # Calculate relative velocity and angle of attack at each point
    u = freestream_velocity * np.cos(alpha_rad) * np.ones_like(x_points)
    v = -freestream_velocity * np.sin(alpha_rad) * np.ones_like(x_points)
    w = np.zeros_like(x_points)
    
    # Calculate lift and drag coefficients
    cl = 0  # For a cube, the lift coefficient is zero
    cd = 2 * np.cos(alpha_rad)**2  # Drag coefficient for a cube
    
    return cl, cd

# Calculate lift and drag coefficients
cl, cd = potential_flow_aero_coefficients(angle_of_attack, x_points, y_points, z_points)

# Plot the cube shape
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_points, y_points, z_points)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Cube Model')
plt.show()

# Plot lift and drag coefficients
plt.figure(figsize=(8, 6))
plt.plot(angle_of_attack, cl, label='CL')
plt.plot(angle_of_attack, cd, label='CD')
plt.xlabel('Angle of Attack (degrees)')
plt.ylabel('Coefficient')
plt.title('Lift and Drag Coefficients vs Angle of Attack')
plt.legend()
plt.grid()
plt.show()
