import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
q_e = 1.6e-19  # Charge of the particle (Coulombs)
# m_e = 9.11e-31  # Mass of the particle (kg)
m_e =3.8175458e-26 # Na+ ion

def export_trajectory(trajectory, velocity, angle, q_e, m_e, E_field, B_field):
    """
    Exports the simulation trajectory to a CSV string for download.

    Parameters:
        trajectory (list of tuples): Each tuple contains (time, x, y, v_x, v_y, a_x, a_y).
        velocity (float): Initial velocity in m/s.
        angle (float): Initial velocity angle in degrees.
        q_e (float): Charge of the particle in Coulombs.
        m_e (float): Mass of the particle in kg.
        E_field (float): Electric field in V/m.
        B_field (float): Magnetic field in T.

    Returns:
        csv_string (str): CSV formatted string.
    """
    header_lines = [
        f"Simulation Parameters",
        f"Initial Velocity (v0): {velocity} m/s",
        f"Angle (theta): {angle} degrees",
        f"Charge (q): {q_e} C",
        f"Mass (m): {m_e} kg",
        f"Electric Field (E): {E_field} V/m",
        f"Magnetic Field (B): {B_field} T",
        "",  # Empty line for separation
        "Time (s), X Position (m), Y Position (m), V_X (m/s), V_Y (m/s), a_X (m/s^2), a_Y (m/s^2)"
    ]

    df = pd.DataFrame(trajectory, columns=["Time (s)", "X Position (m)", "Y Position (m)", 
                                           "V_X (m/s)", "V_Y (m/s)", "a_X (m/s^2)", "a_Y (m/s^2)"])
    
    csv_string = "\n".join(header_lines) + "\n" + df.to_csv(index=False)
    return csv_string

def analytical_solution(E, B, v0, theta, t, q, m):
    vt = v0 * np.array([np.cos(theta), np.sin(theta)])

    if B == 0:  # Pure electric field motion (linear acceleration)
        x_t = vt[0] * t + 0.5 * (q * E / m) * t**2
        y_t = vt[1] * t

        vx_t = vt[0] + (q * E / m) * t  # Increasing velocity in x due to E-field
        vy_t = vt[1]  # Constant velocity in y

        ax_t = (q * E / m)  # Constant acceleration in x
        ay_t = 0  # No acceleration in y

    else:  # Magnetic field present
        omega = q * B / m  # Cyclotron frequency
        v_d = E / B  # Drift velocity in x

        x_t = (vt[1] / omega) * (1 - np.cos(omega * t)) + v_d * t
        y_t = (vt[1] / omega) * np.sin(omega * t) - (vt[0] / omega) * (1 - np.cos(omega * t))

        vx_t = v_d + vt[0] * np.cos(omega * t) - vt[1] * np.sin(omega * t)
        vy_t = vt[1] * np.cos(omega * t) + vt[0] * np.sin(omega * t)

        ax_t = (q * E / m) - omega * vy_t  # Lorentz force in x
        ay_t = omega * vx_t  # Lorentz force in y

    return x_t, y_t, vx_t, vy_t, ax_t, ay_t

# Streamlit UI
st.title("Charged Particle in E & B Fields")

# User Inputs
log_E_field = st.slider("Electric Field Strength (V/m)", -3, +3, 0)
E_field = 10 ** log_E_field

log_B_field = st.slider("Magnetic Field Strength (T)", -5, +1, -4)
B_field = 10 ** log_B_field

velocity = st.number_input("Initial Velocity (m/s)", value=1e5)
angle = st.number_input("Angle of Velocity (degrees)", value=0.0)

# Logarithmic slider for simulation time
log_time = st.slider("Simulation Duration (ns to ms)", -9, -3, -6)
time_max = 10 ** log_time  # Convert log scale to actual time in seconds

# Convert angle to radians
theta = np.radians(angle)

if st.button("Update Plot"):
    t_vals = np.linspace(0, time_max, 1000)
    x_vals, y_vals, vx_vals, vy_vals, ax_vals, ay_vals = analytical_solution(E_field, B_field, velocity, theta, t_vals, q_e, m_e)
    
    trajectory = list(zip(t_vals, x_vals, y_vals, vx_vals, vy_vals, ax_vals, ay_vals))
    
    # Generate CSV data
    trajectory_csv = export_trajectory(trajectory, velocity, angle, q_e, m_e, E_field, B_field)
    
    # Add download button
    st.download_button(
        label="Download Trajectory Data",
        data=trajectory_csv,
        file_name="trajectory_data.csv",
        mime="text/csv"
    )

    # Plot results
    fig, ax = plt.subplots()
    ax.plot(x_vals * 1e3, y_vals * 1e3, label="Trajectory")  # Convert to mm for readability
    
    # Add E and B field indicators in a small corner area
    ax.quiver(0, 8, 1, 0, angles='xy', scale_units='xy', scale=3, color='r', label='E Field (+x)')
    ax.text(0, 7, r'$\odot$', fontsize=14, color='b', ha='center', va='center')  # B field out of screen
    
    ax.set_xlabel("x position (mm)")
    ax.set_ylabel("y position (mm)")
    
    ax.set_xlim(-10, 10)  # x-axis from -10 mm to 10 mm
    ax.set_ylim(-10, 10)  # y-axis from -10 mm to 10 mm
    
    ax.set_title("Charged Particle Motion")
    ax.legend()
    st.pyplot(fig)
