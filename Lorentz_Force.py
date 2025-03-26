# cosmic_ray_defense_app.py

import streamlit as st
import pandas as pd
import os

# Path to the CSV file in the data directory
BADGES_CSV = os.path.join("data", "badges.csv")

@st.cache_data
def load_badge_data(csv_file=BADGES_CSV):
    """
    Load badge data from a CSV file.
    The CSV is expected to have columns: "badge", "avatar_style", "avatar_seed", "nickname".
    For new users, avatar_style and avatar_seed may be empty.
    """
    return pd.read_csv(csv_file)

def save_badge_data(df, csv_file=BADGES_CSV):
    """
    Save the DataFrame back to the CSV file.
    """
    df.to_csv(csv_file, index=False)

def get_dicebear_avatar_url(seed, style="bottts"):
    """
    Construct a DiceBear avatar URL using the provided seed and style, using the updated API endpoint.
    
    Parameters:
      - seed: A value (e.g., integer from slider) used to generate the avatar.
      - style: The avatar style; e.g., "bottts", "adventurer", "avataaars", etc.
    
    Returns:
      A URL string pointing to the generated avatar image.
    """
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
            # Get the student's row from the CSV
            student_row = badges_df[badges_df["badge"].astype(str) == badge].iloc[0]
            # Check if avatar information already exists
            if pd.notna(student_row.get("avatar_style")) and pd.notna(student_row.get("avatar_seed")) and student_row.get("avatar_style") != "":
                st.session_state["avatar_style"] = student_row["avatar_style"]
                st.session_state["avatar_seed"] = student_row["avatar_seed"]
                st.session_state["nickname"] = student_row.get("nickname", f"User {badge}")
                st.session_state["avatar_url"] = get_dicebear_avatar_url(student_row["avatar_seed"], style=student_row["avatar_style"])
                st.success("Badge accepted! Avatar already set.")
                st.session_state["page"] = "Mission Intro"
            else:
                st.success("Badge accepted! Please set up your avatar.")
                st.session_state["page"] = "Profile Setup"
        else:
            st.error("Badge number not recognized. Please try again.")

def show_profile_setup():
    st.header("Profile Setup")
    st.write("Select your avatar. (This will be saved and used on subsequent logins.)")
    
    # Retrieve the badge from session state
    badge = st.session_state.get("badge", "")
    if not badge:
        st.error("No badge number found. Please sign in first.")
        return

    st.write("Choose your preferred avatar style and appearance:")
    
    # Let the user choose an avatar style
    styles = ["bottts", "adventurer", "adventurer-neutral", "avataaars", "initials", "identicon", "micah"]
    style_choice = st.selectbox("Select Avatar Style", options=styles, index=0)

    # Let the user choose a seed value via a slider (e.g., between 1 and 30)
    seed_choice = st.slider("Select Avatar Variation", 1, 30, 1)
    
    # Generate the DiceBear avatar URL using the chosen seed and style
    avatar_url = get_dicebear_avatar_url(seed_choice, style=style_choice)
    st.image(avatar_url, caption="Preview Your Avatar", width=200)
    
    # Optionally, allow the user to choose a nickname (defaults to "User <badge>")
    nickname = st.text_input("Choose a nickname (optional)", value=f"User {badge}")
    
    if st.button("Next"):
        # Save the selected avatar info into the CSV
        badges_df = load_badge_data()
        # Update the row matching the badge
        badges_df.loc[badges_df["badge"].astype(str) == badge, "avatar_style"] = style_choice
        badges_df.loc[badges_df["badge"].astype(str) == badge, "avatar_seed"] = seed_choice
        badges_df.loc[badges_df["badge"].astype(str) == badge, "nickname"] = nickname
        save_badge_data(badges_df)
        
        # Update session state
        st.session_state["avatar_style"] = style_choice
        st.session_state["avatar_seed"] = seed_choice
        st.session_state["nickname"] = nickname
        st.session_state["avatar_url"] = avatar_url
        
        st.success("Avatar saved!")
        st.session_state["page"] = "Mission Intro"

def show_mission_intro():
    st.header("Mission Introduction")
    st.write("Placeholder for the mission narrative and instructions.")
    st.write("This is where you'll introduce the Cosmic Ray Defense mission.")
    
    # Optionally display the avatar on the main page (or in the sidebar)
    if "avatar_url" in st.session_state:
        st.image(st.session_state["avatar_url"], width=100, caption="Profile Picture")

def main():
    # Set initial page if not set
    if "page" not in st.session_state:
        st.session_state["page"] = "Sign In"
    
    # Sidebar: Show avatar (if exists) and provide an "Edit Profile" button
    st.sidebar.title("Navigation")
    if "avatar_url" in st.session_state:
        st.sidebar.image(st.session_state["avatar_url"], width=100)
        if st.sidebar.button("Edit Profile"):
            st.session_state["page"] = "Profile Setup"
    
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
