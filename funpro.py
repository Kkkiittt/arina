import streamlit as st
import re
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION & HELPER FUNCTIONS ---

def validate_name(name):
    """Validates name using regex"""
    return re.fullmatch(r"[A-Za-z\s'-]+", name) is not None

def validate_birth(birth_str):
    """Validates date format YYYY-MM-DD"""
    try:
        datetime.strptime(birth_str.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_id(aydi):
    """Checks if ID is digits only"""
    return aydi.isdigit()

def get_questions():
    """Returns the list of questions and weighted options"""
    return [
        ("Do you regularly drink herbal tea while studying?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Do you prefer herbal tea over caffeinated drinks during study sessions?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Do you consume herbal tea specifically to improve your concentration?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Do you drink herbal tea at least 3 times per week while studying?",
         [("Never", 0), ("Rarely", 1), ("Maybe", 2), ("Often", 3), ("Always", 4)]),
        
        ("Do you choose specific types of herbal tea based on their calming effects?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Does drinking herbal tea help you stay focused for longer periods?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Do you feel more mentally alert after drinking herbal tea?",
         [("Always", 0), ("Often", 1), ("Maybe", 2), ("Rarely", 3), ("Never", 4)]), # Note: Reverse scoring
        
        ("How often do you feel calm?",
         [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)]), # Note: Reverse scoring
        
        ("Does herbal tea improve your overall study performance?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Very Often", 3), ("Always", 4)]),
        
        ("Does herbal tea reduce distractions during your study sessions?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Does herbal tea help you feel calmer while studying?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Super Often", 3), ("Always", 4)]),
        
        ("Do you experience less stress when you drink herbal tea during study sessions?",
         [("Always", 0), ("Often", 1), ("Sometimes", 2), ("Rarely", 3), ("Never", 4)]), # Note: Reverse scoring
        
        ("Does herbal tea help reduce anxiety before exams or assignments?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Do you feel more relaxed and less overwhelmed when drinking herbal tea?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]),
        
        ("Does herbal tea create a comfortable and productive study environment for you?",
         [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)])
    ]

def calculate_result(score):
    """Determines the textual result based on score"""
    if score <= 15:
        return "Very Low Effect"
    elif score <= 30:
        return "Preference to search for other methods"
    elif score <= 50:
        return "Neutral Impact"
    elif score <= 60:
        return "High Calm Focus from Herbal Tea"
    else:
        return "Negative or Opposite Effect"

def save_to_csv(data):
    """Appends data to a CSV file"""
    df_new = pd.DataFrame([data])
    filename = "survey_results.csv"
    
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
        
    df_combined.to_csv(filename, index=False)

# --- STREAMLIT APP LOGIC ---

st.set_page_config(page_title="Herbal Tea Study Survey", layout="centered")

# Initialize Session State
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0: Info, 1: Survey, 2: Result
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# --- STEP 0: PERSONAL INFO ---
if st.session_state.step == 0:
    st.title("🌿 Herbal Tea & Study Habits Survey")
    st.markdown("Please enter your details to begin.")
    
    with st.form("info_form"):
        name = st.text_input("Full Name", placeholder="e.g. John Doe")
        birth = st.text_input("Date of Birth", placeholder="YYYY-MM-DD")
        uid = st.text_input("Student ID", placeholder="e.g. 123456")
        
        submitted = st.form_submit_button("Start Survey")
        
        if submitted:
            errors = []
            if not validate_name(name):
                errors.append("Invalid Name (Letters, spaces, hyphens only).")
            if not validate_birth(birth):
                errors.append("Invalid Date Format (Use YYYY-MM-DD).")
            if not validate_id(uid):
                errors.append("Invalid ID (Digits only).")
                
            if errors:
                for err in errors:
                    st.error(err)
            else:
                st.session_state.user_info = {
                    "name": name,
                    "birth": birth,
                    "id": uid
                }
                st.session_state.step = 1
                st.rerun()

# --- STEP 1: SURVEY QUESTIONS ---
elif st.session_state.step == 1:
    st.title("📝 Survey Questions")
    st.progress(0.5) # Visual indicator
    
    questions = get_questions()
    
    # We use a form to collect all answers at once to prevent page reloads on every click
    with st.form("survey_form"):
        temp_answers = {}
        
        for i, (question_text, options) in enumerate(questions):
            st.markdown(f"**{i+1}. {question_text}**")
            
            # Create radio buttons for each option
            # We store the score value directly as the key for the radio button
            option_labels = [opt[0] for opt in options]
            option_scores = [opt[1] for opt in options]
            
            # Map label to score for retrieval later
            label_to_score = {label: score for label, score in options}
            
            selected_label = st.radio(
                f"Select for Q{i+1}", 
                options=option_labels,
                key=f"q_{i}",
                horizontal=False # Set to True if you want them side-by-side
            )
            temp_answers[i] = label_to_score[selected_label]
            
        submit_survey = st.form_submit_button("Submit Answers")
        
        if submit_survey:
            st.session_state.answers = temp_answers
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: RESULTS ---
elif st.session_state.step == 2:
    st.title("📊 Your Results")
    
    # Calculate Score
    total_score = sum(st.session_state.answers.values())
    result_text = calculate_result(total_score)
    
    # Display Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Score", total_score)
    col2.metric("Impact Level", result_text)
    
    # Visual Feedback
    if "High Calm" in result_text:
        st.success("✅ Herbal tea seems to be working well for you!")
    elif "Low Effect" in result_text or "Other methods" in result_text:
        st.warning("⚠️ You might want to explore other study aids.")
    elif "Negative" in result_text:
        st.error("❌ Herbal tea might be having an opposite effect.")
    else:
        st.info("ℹ️ Neutral impact detected.")

    # Save Data
    final_data = {
        "Name": st.session_state.user_info['name'],
        "DOB": st.session_state.user_info['birth'],
        "ID": st.session_state.user_info['id'],
        "Score": total_score,
        "Result": result_text,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_to_csv(final_data)
    st.success("💾 Results saved to 'survey_results.csv'")
    
    # Option to restart
    if st.button("Take Survey Again"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.user_info = {}
        st.rerun()
        
    # Download Link for CW demonstration
    if os.path.exists("survey_results.csv"):
        with open("survey_results.csv", "rb") as f:
            st.download_button(
                label="📥 Download All Results (CSV)",
                data=f,
                file_name='survey_results.csv',
                mime='text/csv'
            )
