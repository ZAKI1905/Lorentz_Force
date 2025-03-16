import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
dt = 1e-8  # Time step for numerical integration
num_steps = 5000  # Number of simulation steps

# Streamlit UI
st.title("Charged Particle Motion in Electric and Magnetic Fields")
st.write("""
This simulation visualizes the motion of a charged particle under the influence of an electric field \(E\) and a magnetic field \(B\) perpendicular to the plane.
Adjust the parameters and observe the trajectory!
""")

# Sliders for user input
charge = st.slider("Charge (C, x10⁻¹⁶)", -10.0, 10.0, -4.8) * 1e-16
mass = st.slider("Mass (kg, x10⁻²⁵)", 1.0, 10.0, 7.5) * 1e-25
velocity_x = st.slider("Initial Velocity in x (m/s, x10⁶)", -20.0, 20.0, 10.0) * 1e6
velocity_y = st.slider("Initial Velocity in y (m/s, x10⁶)", -20.0, 20.0, 0.0) * 1e6
B_field = st.slider("Magnetic Field Strength (T)", -5.0, 5.0, -2.9)
E_field = st.slider("Electric Field Strength (V/m, x10⁵)", -10.0, 10.0, 0.0) * 1e5

# Initial conditions
position = np.array([0.0, 0.0])
velocity = np.array([velocity_x, velocity_y])
trajectory = [position.copy()]

def lorentz_force(q, v, E, B):
    """Computes the Lorentz force."""
    return q * (E + np.cross(v, np.array([0, 0, B]))[:2])

# Numerical integration using Euler's method
for _ in range(num_steps):
    force = lorentz_force(charge, velocity, np.array([E_field, 0]), B_field)
    acceleration = force / mass
    velocity += acceleration * dt
    position += velocity * dt
    trajectory.append(position.copy())

trajectory = np.array(trajectory)

# Plotting
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(trajectory[:, 0] * 1000, trajectory[:, 1] * 1000, 'b-', label="Trajectory")
ax.set_xlabel("x position (mm)")
ax.set_ylabel("y position (mm)")
ax.set_title("Charged Particle Motion")
ax.legend()
st.pyplot(fig)

# Data export functionality
data = pd.DataFrame({
    "Time (s)": np.arange(0, num_steps * dt, dt),
    "X Position (m)": trajectory[:, 0],
    "Y Position (m)": trajectory[:, 1]
})

st.download_button("Download Data", data.to_csv(index=False), "particle_motion.csv", "text/csv")
