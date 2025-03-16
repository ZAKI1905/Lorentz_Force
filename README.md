**Repository: Charged-Particle-Simulator**

### Description
This repository contains a **Streamlit-based web application** for simulating the motion of a charged particle in the presence of **electric (E) and magnetic (B) fields**. Users can adjust parameters such as **charge, mass, velocity, E-field, and B-field**, visualize the trajectory, and download data for further analysis. 

### Features
- **Interactive Parameter Controls**: Adjust charge, mass, velocity, and field strengths.
- **Real-Time Visualization**: Displays the trajectory of the charged particle in a 2D plane.
- **Numerical Integration**: Uses Euler's method to compute motion based on the Lorentz force.
- **Data Export**: Allows users to download trajectory data for analysis.
- **Planned Enhancements**:
  - Animated trajectory visualization
  - Additional data analysis tools
  - Support for 3D motion

---

## README.md

# Charged Particle Motion Simulator

### Overview
This **interactive web-based simulator** allows users to explore the motion of a **charged particle in electric and magnetic fields** using **Streamlit** and **Python**. The simulation is based on the **Lorentz force equation**, which governs the trajectory of charged particles in electromagnetic fields.

### Features
- **Real-time adjustable parameters**
  - Charge (Coulombs)
  - Mass (kg)
  - Initial velocity (m/s)
  - Magnetic field strength (Tesla)
  - Electric field strength (V/m)
- **Graphical trajectory visualization**
- **Data logging and export for analysis**

### Installation
To run this simulator locally:
```sh
# Clone the repository
git clone https://github.com/yourusername/Charged-Particle-Simulator.git
cd Charged-Particle-Simulator

# Install dependencies
pip install streamlit numpy matplotlib pandas

# Run the application
streamlit run app.py
```

### Usage
- Adjust the sliders to set the charge, mass, velocity, and field values.
- Click the **Run Simulation** button to visualize the trajectory.
- Download the particle motion data as a CSV file for analysis.

### Theory
The particle's motion is governed by the **Lorentz force**:
\[ \mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B}) \]

where:
- `q` is the charge of the particle,
- `E` is the electric field,
- `B` is the magnetic field,
- `v` is the velocity of the particle.

### Future Improvements
- **Animated trajectory visualization**
- **Expanded support for 3D motion**
- **Curve fitting tools for experimental verification**

---

**Developed for PHY 132 at Eastern Kentucky University**  
**Instructor: Professor Zakeri (m.zakeri@eku.edu)**
