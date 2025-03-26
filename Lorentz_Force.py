# cosmic_ray_defense_app.py

import streamlit as st

def show_sign_in():
    st.header("Sign In")
    st.write("Enter your badge number to log in:")
    badge = st.text_input("Badge Number")
    if st.button("Submit"):
        st.success("Logged in successfully! (Placeholder)")
        st.session_state.page = "Mission Intro"

def show_mission_intro():
    st.header("Mission Introduction")
    st.write("Welcome to the Cosmic Ray Defense mission!")
    st.write("Narrative: Your goal is to protect a planet by mapping its magnetosphere.")
    nickname = st.text_input("Choose your nickname")
    planet_choice = st.selectbox("Choose a planet to work on", ["Mercury", "Earth", "Jupiter"])  # Example choices
    st.write("Placeholder: Displaying information about the selected planet.")
    if st.button("Start Spaceship Experiment"):
        st.session_state.page = "Spaceship Experiment"

def show_spaceship_experiment():
    st.header("Spaceship Experiment")
    st.write("Placeholder: Set up your experiments by firing cosmic rays and measuring trajectories.")
    st.write("Placeholder: Insert diagrams, controls, and results here.")
    if st.button("Proceed to Drone Deployment"):
        st.session_state.page = "Drone Deployment"

def show_drone_deployment():
    st.header("Drone Deployment")
    st.write("Placeholder: Deploy the drone to measure the surface magnetic field using a current loop.")
    st.write("Placeholder: Display results and additional mission details.")
    if st.button("Finish Mission"):
        st.write("Mission Completed. (Placeholder: Display summary and feedback)")

def main():
    # Initialize session state for page navigation if not already set
    if 'page' not in st.session_state:
        st.session_state.page = "Sign In"
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page_options = ["Sign In", "Mission Intro", "Spaceship Experiment", "Drone Deployment"]
    selected_page = st.sidebar.radio("Go to", page_options, index=page_options.index(st.session_state.page))
    st.session_state.page = selected_page

    # Render the selected page
    if st.session_state.page == "Sign In":
        show_sign_in()
    elif st.session_state.page == "Mission Intro":
        show_mission_intro()
    elif st.session_state.page == "Spaceship Experiment":
        show_spaceship_experiment()
    elif st.session_state.page == "Drone Deployment":
        show_drone_deployment()

if __name__ == "__main__":
    main()
