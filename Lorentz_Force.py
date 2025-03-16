import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
q = 1.6e-19  # Charge of the particle (Coulombs)
m = 9.11e-31  # Mass of the particle (kg)

# Function to compute analytical solution
def analytical_solution(E, B, v0, theta, t):
    vt = v0 * np.array([np.cos(theta), np.sin(theta)])
    
    if B == 0:  # Pure electric field motion (linear acceleration)
        x_t = vt[0] * t + 0.5 * (q * E / m) * t**2
        y_t = vt[1] * t
    else:  # Magnetic field present
        omega = q * B / m  # Cyclotron frequency
        x_t = (vt[0] / omega) * np.sin(omega * t) + (E / B) * t
        y_t = (vt[1] / omega) * (1 - np.cos(omega * t))
    
    return x_t, y_t

# Streamlit UI
st.title("Charged Particle in E & B Fields")

# User Inputs
E_field = st.number_input("Electric Field Strength (V/m)", value=0.0)
B_field = st.number_input("Magnetic Field Strength (T)", value=0.1)
velocity = st.number_input("Initial Velocity (m/s)", value=1e5)
angle = st.number_input("Angle of Velocity (degrees)", value=0.0)
time_max = st.number_input("Simulation Duration (s)", value=1e-6)

# Convert angle to radians
theta = np.radians(angle)

# Button to update plot
if st.button("Update Plot"):
    t_vals = np.linspace(0, time_max, 1000)
    x_vals, y_vals = analytical_solution(E_field, B_field, velocity, theta, t_vals)
    
    # Plot results
    fig, ax = plt.subplots()
    ax.plot(x_vals * 1e3, y_vals * 1e3, label="Trajectory")  # Convert to mm for readability
    
    # Show field directions
    ax.quiver(0, 0, 1, 0, angles='xy', scale_units='xy', scale=5, color='r', label='E Field (x-direction)')
    ax.quiver(0, 0, 0, 1, angles='xy', scale_units='xy', scale=5, color='b', label='B Field (out of screen)')
    
    ax.set_xlabel("x position (mm)")
    ax.set_ylabel("y position (mm)")
    ax.set_title("Charged Particle Motion")
    ax.legend()
    st.pyplot(fig)
