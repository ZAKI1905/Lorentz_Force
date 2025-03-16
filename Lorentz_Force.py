import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

# Constants
dt = 1e-10  # Initial small time step
num_steps = 5000  # Max steps to simulate
c = 3e8  # Speed of light in m/s
max_time = 10  # Maximum simulation time in seconds
boundary = 0.01  # Boundary limit in meters (10 mm screen size)

# Streamlit UI
st.title("Charged Particle Motion in Electric and Magnetic Fields")
st.write(r"""
This simulation visualizes the motion of a charged particle under the influence of an electric field \(E\) and a magnetic field \(B\) perpendicular to the plane.
""")

# Sliders for user input
charge = st.slider("Charge (C, x10⁻¹⁶)", -10.0, 10.0, -4.8) * 1e-16
mass = st.slider("Mass (kg, x10⁻²⁵)", 1.0, 10.0, 7.5) * 1e-25
velocity_x = st.slider("Initial Velocity in x (m/s, x10⁶)", -50.0, 50.0, 10.0) * 1e6
velocity_y = st.slider("Initial Velocity in y (m/s, x10⁶)", -50.0, 50.0, 0.0) * 1e6
B_field = st.slider("Magnetic Field Strength (T)", -5.0, 5.0, -2.9)
E_field = st.slider("Electric Field Strength (V/m, x10⁵)", -10.0, 10.0, 0.0) * 1e5
animation_speed = st.slider("Animation Speed (ms per frame)", 1, 100, 20)

# Initial conditions
position = np.array([0.0, 0.0, 0.0])
velocity = np.array([velocity_x, velocity_y, 0.0])
trajectory = []
time_array = []

def lorentz_force(q, v, E, B):
    """Computes the relativistic Lorentz force."""
    return q * (E + np.cross(v, B))

def gamma_factor(v):
    """Computes the relativistic Lorentz factor."""
    speed = np.linalg.norm(v)
    return 1 / np.sqrt(1 - (speed**2 / c**2)) if speed < c else 1e6

# Adaptive RK4 Step
def rk4_step(q, m, v, r, E, B, dt):
    def acceleration(v):
        gamma = gamma_factor(v)
        F = lorentz_force(q, v, E, B)
        v_dot_F = np.dot(v, F)
        return (F - (gamma**2 / c**2) * v_dot_F * v) / (gamma * m)
    
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
    
    return v_new, r_new

# Convert E and B to 3D vectors
E = np.array([E_field, 0, 0])
B = np.array([0, 0, B_field])

# Placeholder for Data Download Button
data_placeholder = st.empty()

# Animation Setup
fig, ax = plt.subplots(figsize=(6, 6))
trajectory_plot, = ax.plot([], [], 'b-', label="Trajectory")
ax.set_xlabel("x position (mm)")
ax.set_ylabel("y position (mm)")
ax.set_title("Charged Particle Motion")
ax.legend()
ax.set_xlim(-boundary * 1000, boundary * 1000)
ax.set_ylim(-boundary * 1000, boundary * 1000)
st_plot = st.pyplot(fig)

# Simulation Loop
for step in range(num_steps):
    velocity, position = rk4_step(charge, mass, velocity, position, E, B, dt)
    trajectory.append(position[:2].copy())
    time_array.append((step + 1) * dt)
    
    # Stop simulation if particle leaves boundary
    if np.abs(position[0]) > boundary or np.abs(position[1]) > boundary:
        break  # Stop simulation when particle exits
    
    # Adaptive resolution: Skip updates for fast animation speeds
    if step % max(1, int(50 / animation_speed)) == 0:
        trajectory_np = np.array(trajectory)
        trajectory_plot.set_data(trajectory_np[:, 0] * 1000, trajectory_np[:, 1] * 1000)
        st_plot.pyplot(fig, clear_figure=True)
        time.sleep(animation_speed / 1000.0)

# Ensure data arrays are of equal length
data_length = min(len(time_array), len(trajectory))
time_array = time_array[:data_length]
trajectory = trajectory[:data_length]
data = pd.DataFrame({
    "Time (s)": time_array,
    "X Position (m)": np.array(trajectory)[:, 0],
    "Y Position (m)": np.array(trajectory)[:, 1]
})

# Display Download Button
data_placeholder.download_button(
    "Download Simulation Data", data.to_csv(index=False), "particle_motion.csv", "text/csv"
)
