# cosmic_ray_defense_app.py

import streamlit as st
import pandas as pd

@st.cache_data
def load_badge_data(csv_file="data/badges.csv"):
    """
    Load badge data from a CSV file.
    The CSV is expected to have a single column "badge" containing valid badge numbers.
    """
    return pd.read_csv(csv_file)

def get_dicebear_avatar_url(seed, style="bottts"):
    """
    Construct a DiceBear avatar URL using the unique seed (badge number) and chosen style.
    
    Parameters:
      - seed: A unique string (e.g., badge number) to generate the avatar.
      - style: The avatar style; options include "bottts", "adventurer", "avataaars", etc.
    
    Returns:
      A URL string pointing to the generated avatar image.
    """
    # return f"https://api.dicebear.com/6.x/<style>/svg?seed=<seed>"
    return f"https://api.dicebear.com/9.x/{style}/svg?seed={seed}"

def show_sign_in():
    st.header("Sign In")
    st.write("Enter your unique badge number to log in:")
    badge = st.text_input("Badge Number")
    
    if st.button("Sign In"):
        badges_df = load_badge_data()
        # Ensure consistency by converting to string
        valid_badges = badges_df["badge"].astype(str).values
        if badge in valid_badges:
            st.session_state["badge"] = badge
            st.success("Badge accepted!")
            st.session_state["page"] = "Profile Setup"
        else:
            st.error("Badge number not recognized. Please try again.")

def show_profile_setup():
    st.header("Profile Setup")
    st.write("Select your avatar using DiceBear. Your profile is identified solely by your badge number.")
    
    # Retrieve the badge from session state
    badge = st.session_state.get("badge", "")
    if not badge:
        st.error("No badge number found. Please sign in first.")
        return

    st.write("Your unique avatar is generated based on your badge number. Choose your preferred avatar style below:")
    
    # Let the user choose an avatar style
    styles = ["bottts", "adventurer", "adventurer-neutral", "avataaars", "initials", "identicon", "micah"]
    style_choice = st.selectbox("Select Avatar Style", options=styles, index=0)
    
    # Generate the DiceBear avatar URL using the badge as the seed
    avatar_url = get_dicebear_avatar_url(badge, style=style_choice)
    st.image(avatar_url, caption="Your Avatar", width=200)
    
    # Optionally, allow the user to choose a nickname (defaults to "User <badge>")
    nickname = st.text_input("Choose a nickname (optional)", value=f"User {badge}")
    st.session_state["nickname"] = nickname
    st.session_state["avatar_url"] = avatar_url
    
    if st.button("Next"):
        st.session_state["page"] = "Mission Intro"

def show_mission_intro():
    st.header("Mission Introduction")
    st.write("Placeholder for the mission narrative and instructions.")
    st.write("This is where you'll introduce the Cosmic Ray Defense mission.")

def main():
    # Set initial page if not set
    if "page" not in st.session_state:
        st.session_state["page"] = "Sign In"
    
    # Sidebar Navigation (optional: remove or disable to enforce linear flow)
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
