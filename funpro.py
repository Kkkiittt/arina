import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for storing answers
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Define survey steps
steps = ["Demographics", "Main Questions", "Feedback"]

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def save_data():
    # Convert answers to DataFrame
    df = pd.DataFrame([st.session_state.answers])
    df['Timestamp'] = datetime.now()
    
    # Append to existing CSV or create new
    try:
        existing_df = pd.read_csv("survey_responses.csv")
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        updated_df = df
    
    updated_df.to_csv("survey_responses.csv", index=False)
    st.success("Thank you! Your response has been saved.")
    st.balloons()

# --- UI Layout ---
st.title("📋 Coursework Survey")

# Progress Bar
progress = (st.session_state.step + 1) / len(steps)
st.progress(progress)

# Step 1: Demographics
if st.session_state.step == 0:
    st.header("Step 1: About You")
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    gender = st.radio("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    
    if st.button("Next →"):
        if age and gender:
            st.session_state.answers['Age'] = age
            st.session_state.answers['Gender'] = gender
            next_step()
            st.rerun()
        else:
            st.warning("Please fill all fields.")

# Step 2: Main Questions
elif st.session_state.step == 1:
    st.header("Step 2: Your Opinions")
    satisfaction = st.slider("How satisfied are you with the service?", 1, 10, 5)
    issues = st.multiselect("What issues did you face?", ["Slow Internet", "Cleanliness", "Noise", "Food Quality", "None"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.answers['Satisfaction'] = satisfaction
            st.session_state.answers['Issues'] = ", ".join(issues)
            next_step()
            st.rerun()

# Step 3: Feedback & Submit
elif st.session_state.step == 2:
    st.header("Step 3: Final Comments")
    comments = st.text_area("Any additional comments?")
    
    if st.button("Submit Survey"):
        st.session_state.answers['Comments'] = comments
        save_data()
        
    if st.button("← Back"):
        prev_step()
        st.rerun()
