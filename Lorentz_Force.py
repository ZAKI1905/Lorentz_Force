# cosmic_ray_defense_app.py

import streamlit as st
import pandas as pd

# Function to load student data from a CSV file
@st.cache_data
def load_student_data(csv_file="students.csv"):
    return pd.read_csv(csv_file)

def show_sign_in():
    st.header("Sign In")
    st.write("Enter your badge number to log in:")
    badge = st.text_input("Badge Number")
    
    if st.button("Sign In"):
        students_df = load_student_data()
        # Search for the badge number in the data
        student_row = students_df[students_df["badge"] == badge]
        if not student_row.empty:
            student = student_row.iloc[0]
            # Save student info in session state for later use
            st.session_state["badge"] = badge
            st.session_state["first_name"] = student["first_name"]
            st.session_state["last_name"] = student["last_name"]
            st.session_state["image"] = student["image"]
            # Show welcome message and automatically advance to profile setup
            st.success(f"Welcome {student['first_name']} {student['last_name']}!")
            st.session_state["page"] = "Profile Setup"
        else:
            st.error("Badge number not found. Please try again.")

def show_profile_setup():
    st.header("Profile Setup")
    st.write("Review your profile and choose an avatar and nickname:")
    
    # Display student information from the sign-in step
    first_name = st.session_state.get("first_name", "")
    last_name = st.session_state.get("last_name", "")
    st.write(f"Name: {first_name} {last_name}")
    
    # Display the student's current image (provided in the CSV)
    if "image" in st.session_state:
        st.image(st.session_state["image"], width=200)
    
    # Allow them to set/change their nickname
    nickname = st.text_input("Choose your nickname", value=first_name)
    st.session_state["nickname"] = nickname
    
    # Provide a list of available avatars as a placeholder.
    # Later you can update these to paths/URLs for the avatars you choose.
    avatar_options = [
        "avatar1.png", "avatar2.png", "avatar3.png", "avatar4.png"
    ]
    selected_avatar = st.selectbox("Select an avatar", options=avatar_options)
    st.session_state["avatar"] = selected_avatar
    
    # A button to proceed to the next page (e.g., Mission Intro)
    if st.button("Next"):
        st.session_state["page"] = "Mission Intro"

def show_mission_intro():
    st.header("Mission Introduction")
    st.write("Placeholder for the mission narrative and instructions.")
    # Additional mission intro content goes here...

def main():
    # Initialize session state for page navigation if not already set
    if "page" not in st.session_state:
        st.session_state["page"] = "Sign In"
    
    # Navigation: you can also hide the sidebar if you want to force linear progression
    st.sidebar.title("Navigation")
    page_options = ["Sign In", "Profile Setup", "Mission Intro"]
    selected_page = st.sidebar.radio("Go to", page_options, index=page_options.index(st.session_state["page"]))
    st.session_state["page"] = selected_page

    # Render the selected page
    if st.session_state["page"] == "Sign In":
        show_sign_in()
    elif st.session_state["page"] == "Profile Setup":
        show_profile_setup()
    elif st.session_state["page"] == "Mission Intro":
        show_mission_intro()

if __name__ == "__main__":
    main()
