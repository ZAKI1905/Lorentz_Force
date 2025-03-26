# cosmic_ray_defense.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(page_title="Cosmic Ray Defense", layout="wide")

# --- Title and Description ---
st.title("🌌 Cosmic Ray Defense Simulator")
st.markdown("""
Model the trajectory of charged cosmic rays entering a planetary magnetic field.
Use your knowledge of the Lorentz force and magnetic deflection to protect your base!
""")

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Simulation Settings")

charge = st.sidebar.selectbox("Particle Charge (q)", [-1, 1], index=0)
mass = st.sidebar.slider("Particle Mass (kg)", 1e-27, 1e-24, value=1.67e-27)
velocity_mag = st.sidebar.slider("Initial Speed (m/s)", 1e5, 1e7, step=1e5, value=1e6)
angle_deg = st.sidebar.slider("Entry Angle (deg)", 0, 90, 45)
B_mag = st.sidebar.slider("Magnetic Field Strength (T)", 0.0, 5.0, 1.0)

# --- Calculate Initial Conditions ---
angle_rad = np.radians(angle_deg)
v0 = np.array([velocity_mag * np.cos(angle_rad), velocity_mag * np.sin(angle_rad), 0])
q = charge * 1.6e-19

# --- Magnetic Field (Constant in this version) ---
B = np.array([0, 0, B_mag])

# --- Particle Trajectory Function ---
def simulate_trajectory(q, m, v0, B, dt=1e-9, steps=2000):
    r = np.zeros((steps, 3))
    v = v0.copy()
    for i in range(1, steps):
        F = q * np.cross(v, B)
        a = F / m
        v += a * dt
        r[i] = r[i-1] + v * dt
    return r

# --- Run Simulation ---
trajectory = simulate_trajectory(q, mass, v0, B)

# --- Plotting ---
fig, ax = plt.subplots()
ax.plot(trajectory[:,0], trajectory[:,1])
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Charged Particle Trajectory")
ax.grid(True)
st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.markdown("**Professor Zakeri – PHY 132 – Eastern Kentucky University** | m.zakeri@eku.edu")
