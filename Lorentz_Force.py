# cosmic_ray_defense_app.py

import streamlit as st
import pandas as pd

@st.cache_data
def load_badge_data(csv_file="data/badges.csv"):
    # Expects a CSV file with a column "badge" containing unique badge numbers.
    return pd.read_csv(csv_file)

def show_sign_in():
    st.header("Sign In")
    st.write("Enter your unique badge number to log in:")
    badge = st.text_input("Badge Number")
    
    if st.button("Sign In"):
        badges_df = load_badge_data()
        # Convert badge numbers to strings for consistency
        valid_badges = badges_df["badge"].astype(str).values
        if badge in valid_badges:
            st.session_state["badge"] = badge
            st.success("Badge accepted!")
            st.session_state["page"] = "Profile Setup"
        else:
            st.error("Badge number not recognized. Please try again.")

def show_profile_setup():
    st.header("Profile Setup")
    st.write("Select your avatar. Your profile is identified only by your badge number.")
    
    # List of available avatars (placeholder names or file paths)
    avatar_options = [
        "avatar1.png", "avatar2.png", "avatar3.png", "avatar4.png", "avatar5.png",
        # Add more as needed, or generate dynamically using an API like DiceBear
    ]
    selected_avatar = st.selectbox("Choose an avatar", options=avatar_options)
    st.session_state["avatar"] = selected_avatar
    
    # Optional: allow the student to set a nickname if desired (defaulting to their badge)
    nickname = st.text_input("Choose a nickname (optional)", value=f"User {st.session_state['badge']}")
    st.session_state["nickname"] = nickname
    
    if st.button("Next"):
        st.session_state["page"] = "Mission Intro"

def show_mission_intro():
    st.header("Mission Introduction")
    st.write("Placeholder for the mission narrative and instructions.")
    # Mission narrative content will go here...

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Sign In"
    
    # Optional: sidebar navigation if you want to allow moving between pages manually.
    st.sidebar.title("Navigation")
    page_options = ["Sign In", "Profile Setup", "Mission Intro"]
    selected_page = st.sidebar.radio("Go to", page_options, index=page_options.index(st.session_state["page"]))
    st.session_state["page"] = selected_page
    
    if st.session_state["page"] == "Sign In":
        show_sign_in()
    elif st.session_state["page"] == "Profile Setup":
        show_profile_setup()
    elif st.session_state["page"] == "Mission Intro":
        show_mission_intro()

if __name__ == "__main__":
    main()
