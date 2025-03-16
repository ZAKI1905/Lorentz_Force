import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
dt = 1e-10  # Smaller time step to improve stability
num_steps = 5000  # Number of simulation steps
c = 3e8  # Speed of light in m/s

# Streamlit UI
st.title("Charged Particle Motion in Electric and Magnetic Fields")
st.write("""
This simulation visualizes the motion of a charged particle under the influence of an electric field \(E\) and a magnetic field \(B\) perpendicular to the plane.
Adjust the parameters and observe the trajectory!
""")

# Sliders for user input
charge = st.slider("Charge (C, x10⁻¹⁶)", -10.0, 10.0, -4.8) * 1e-16
mass = st.slider("Mass (kg, x10⁻²⁵)", 1.0, 10.0, 7.5) * 1e-25
velocity_x = st.slider("Initial Velocity in x (m/s, x10⁶)", -50.0, 50.0, 10.0) * 1e6
velocity_y = st.slider("Initial Velocity in y (m/s, x10⁶)", -50.0, 50.0, 0.0) * 1e6
B_field = st.slider("Magnetic Field Strength (T)", -5.0, 5.0, -2.9)
E_field = st.slider("Electric Field Strength (V/m, x10⁵)", -10.0, 10.0, 0.0) * 1e5

# Initial conditions
position = np.array([0.0, 0.0, 0.0])
velocity = np.array([velocity_x, velocity_y, 0.0])
trajectory = [position[:2].copy()]
time_array = [0.0]

def lorentz_force(q, v, E, B):
    """Computes the relativistic Lorentz force, ensuring 3D vectors."""
    v = np.array([v[0], v[1], 0.0])  # Ensure v is a 3D vector
    return q * (E + np.cross(v, np.array([0, 0, B])))

def gamma_factor(v):
    """Computes the relativistic Lorentz factor."""
    speed = np.linalg.norm(v)
    return 1 / np.sqrt(1 - (speed**2 / c**2)) if speed < c else 1e6  # Prevent infinity

# Relativistic Runge-Kutta 4th Order Method
def rk4_step(q, m, v, r, E, B, dt):
    def acceleration(v):
        v = np.array([v[0], v[1], 0.0])  # Ensure velocity is always 3D
        gamma = gamma_factor(v)
        F = lorentz_force(q, v, E, B)
        v_dot_F = np.dot(v, F)
        return (F - (gamma**2 / c**2) * v_dot_F * v) / (gamma * m)
    
    v = np.array([v[0], v[1], 0.0])  # Ensure v is 3D at the start
    
    k1_v = dt * acceleration(v)
    k1_r = dt * v
    
    k2_v = dt * acceleration(v + 0.5 * k1_v)
    k2_r = dt * (v + 0.5 * k1_v)
    
    k3_v = dt * acceleration(v + 0.5 * k2_v)
    k3_r = dt * (v + 0.5 * k2_v)
    
    k4_v = dt * acceleration(v + k3_v)
    k4_r = dt * (v + k3_v)
    
    v_new = v + (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
    r_new = r + (k1_r + 2*k2_r + 2*k3_r + k4_r) / 6
    
    return np.array([v_new[0], v_new[1], 0.0]), r_new  # Always return 3D velocity

# Run simulation
for step in range(num_steps):
    velocity, position = rk4_step(charge, mass, velocity, position, np.array([E_field, 0, 0]), np.array([0, 0, B_field]), dt)
    trajectory.append(position[:2].copy())
    time_array.append((step + 1) * dt)

trajectory = np.array(trajectory)

# Plotting
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(trajectory[:, 0] * 1000, trajectory[:, 1] * 1000, 'b-', label="Trajectory")
ax.set_xlabel("x position (mm)")
ax.set_ylabel("y position (mm)")
ax.set_title("Charged Particle Motion (Relativistic)")
ax.legend()
st.pyplot(fig)

# Data export functionality
data = pd.DataFrame({
    "Time (s)": time_array,
    "X Position (m)": trajectory[:, 0],
    "Y Position (m)": trajectory[:, 1]
})

st.download_button("Download Data", data.to_csv(index=False), "particle_motion.csv", "text/csv")
