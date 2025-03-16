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

# Initialize session state for trajectory persistence
if "trajectory" not in st.session_state:
    st.session_state["trajectory"] = []
    st.session_state["time_array"] = []
    st.session_state["velocity"] = np.array([0.0, 0.0, 0.0])
    st.session_state["position"] = np.array([0.0, 0.0, 0.0])
    st.session_state["reset"] = False
    st.session_state["mode"] = "Numerical"

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
mode = st.radio("Select Simulation Mode", ["Numerical", "Analytical"], index=0)
reset_button = st.button("Reset Simulation")

if reset_button:
    st.session_state["trajectory"] = []
    st.session_state["time_array"] = []
    st.session_state["velocity"] = np.array([velocity_x, velocity_y, 0.0])
    st.session_state["position"] = np.array([0.0, 0.0, 0.0])
    st.session_state["reset"] = True
    st.session_state["mode"] = mode

def lorentz_force(q, v, E, B):
    """Computes the relativistic Lorentz force."""
    return q * (E + np.cross(v, B))

def gamma_factor(v):
    """Computes the relativistic Lorentz factor."""
    speed = np.linalg.norm(v)
    return 1 / np.sqrt(1 - (speed**2 / c**2)) if speed < c else 1e6

# Analytical Solution Function
def analytical_solution(q, m, v0, E, B, t_array):
    omega_c = np.abs(q * B[2] / m)
    v_perp = np.linalg.norm(v0[:2])
    x_vals = (v_perp / omega_c) * np.sin(omega_c * t_array)
    y_vals = (v_perp / omega_c) * np.cos(omega_c * t_array)
    z_vals = v0[2] * t_array  # Assuming uniform motion in z
    return np.vstack((x_vals, y_vals, z_vals)).T

# Convert E and B to 3D vectors
E = np.array([E_field, 0, 0])
B = np.array([0, 0, B_field])

fig, ax = plt.subplots(figsize=(6, 6))
trajectory_plot, = ax.plot([], [], 'b-', label="Trajectory")
ax.set_xlabel("x position (mm)")
ax.set_ylabel("y position (mm)")
ax.set_title("Charged Particle Motion")
ax.legend()
ax.set_xlim(-boundary * 1000, boundary * 1000)
ax.set_ylim(-boundary * 1000, boundary * 1000)
st_plot = st.pyplot(fig)

if mode == "Numerical":
    if not st.session_state["reset"]:
        for step in range(num_steps):
            velocity, position = rk4_step(charge, mass, st.session_state["velocity"], st.session_state["position"], E, B, dt)
            st.session_state["velocity"] = velocity
            st.session_state["position"] = position
            st.session_state["trajectory"].append(position[:2].copy())
            st.session_state["time_array"].append((step + 1) * dt)
            if np.abs(position[0]) > boundary or np.abs(position[1]) > boundary:
                break
            if step % max(1, int(50 / animation_speed)) == 0:
                trajectory_np = np.array(st.session_state["trajectory"])
                if trajectory_np.shape[0] > 0:
                    trajectory_plot.set_data(trajectory_np[:, 0] * 1000, trajectory_np[:, 1] * 1000)
                st_plot.pyplot(fig, clear_figure=True)
                time.sleep(animation_speed / 1000.0)
else:
    t_vals = np.linspace(0, max_time, num_steps)
    trajectory_np = analytical_solution(charge, mass, np.array([velocity_x, velocity_y, 0.0]), E, B, t_vals)
    trajectory_plot.set_data(trajectory_np[:, 0] * 1000, trajectory_np[:, 1] * 1000)
    st_plot.pyplot(fig, clear_figure=True)

if len(st.session_state["trajectory"]) > 0:
    trajectory_np = np.array(st.session_state["trajectory"])
    data = pd.DataFrame({
        "Time (s)": st.session_state["time_array"],
        "X Position (m)": trajectory_np[:, 0],
        "Y Position (m)": trajectory_np[:, 1]
    })
    st.download_button(
        "Download Simulation Data", data.to_csv(index=False), "particle_motion.csv", "text/csv"
    )
