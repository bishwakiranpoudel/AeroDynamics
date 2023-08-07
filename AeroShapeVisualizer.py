import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AeroShape:
    def __init__(self, shape, dimensions, num_points=20, freestream_velocity=50):
        self.shape = shape
        self.dimensions = dimensions
        self.num_points = num_points
        self.freestream_velocity = freestream_velocity
        self.angle_of_attack = 0
        self.calculate_points()
        self.calculate_coefficients()

    def calculate_points(self):
        x_points, y_points, z_points = self.shape(self.dimensions, self.num_points)
        self.x_points = x_points
        self.y_points = y_points
        self.z_points = z_points

    def calculate_coefficients(self):
        self.cl, self.cd = self.calculate_aero_coefficients()

    def calculate_aero_coefficients(self):
        alpha_rad = np.radians(self.angle_of_attack)
        u = self.freestream_velocity * np.cos(alpha_rad) * np.ones_like(self.x_points)
        v = -self.freestream_velocity * np.sin(alpha_rad) * np.ones_like(self.x_points)
        w = np.zeros_like(self.x_points)
        cl = np.zeros_like(self.x_points)
        cd = 2 * np.cos(alpha_rad)**2 * np.ones_like(self.x_points)
        return cl, cd

def cube_shape(dimensions, num_points):
    x_points, y_points, z_points = np.meshgrid(
        np.linspace(0, dimensions[0], num_points),
        np.linspace(0, dimensions[1], num_points),
        np.linspace(0, dimensions[2], num_points)
    )
    return x_points, y_points, z_points

def sphere_shape(dimensions, num_points):
    phi = np.linspace(0, np.pi, num_points)
    theta = np.linspace(0, 2 * np.pi, num_points)
    phi, theta = np.meshgrid(phi, theta)
    x_points = dimensions[0] * np.sin(phi) * np.cos(theta)
    y_points = dimensions[0] * np.sin(phi) * np.sin(theta)
    z_points = dimensions[0] * np.cos(phi)
    return x_points, y_points, z_points

def custom_shape(dimensions, num_points):
    # Define custom shape function here
    x_points, y_points, z_points = np.meshgrid(
        np.linspace(0, dimensions[0], num_points),
        np.linspace(0, dimensions[1], num_points),
        np.linspace(0, dimensions[2], num_points)
    )
    return x_points, y_points, z_points

def plot_shape():
    selected_shape = shape_var.get()

    try:
        length = float(length_entry.get())
        width = float(width_entry.get())
        height = float(height_entry.get())

        if selected_shape == "Cube":
            shape_function = cube_shape
            dimensions = (length, length, length)
        elif selected_shape == "Sphere":
            shape_function = sphere_shape
            dimensions = (length, )
        elif selected_shape == "Custom":
            shape_function = custom_shape
            dimensions = (length, width, height)
        
        shape = AeroShape(shape_function, dimensions)
        
        ax.cla()
        ax.scatter(shape.x_points, shape.y_points, shape.z_points)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Shape Model')
        
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric dimensions.")

# GUI Setup
root = tk.Tk()
root.title("AeroShape Visualizer")

shape_var = tk.StringVar(value="Cube")

shape_label = ttk.Label(root, text="Select Shape:")
shape_label.pack()

shape_combobox = ttk.Combobox(root, textvariable=shape_var, values=["Cube", "Sphere", "Custom"])
shape_combobox.pack()

length_label = ttk.Label(root, text="Length:")
length_label.pack()
length_entry = ttk.Entry(root)
length_entry.pack()

width_label = ttk.Label(root, text="Width:")
width_label.pack()
width_entry = ttk.Entry(root)
width_entry.pack()

height_label = ttk.Label(root, text="Height:")
height_label.pack()
height_entry = ttk.Entry(root)
height_entry.pack()

plot_button = ttk.Button(root, text="Plot Shape", command=plot_shape)
plot_button.pack()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
