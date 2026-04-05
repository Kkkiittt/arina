import streamlit as st
import re, os, json
import pandas as pd
from datetime import datetime

# --- Helpers ---
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

def validate(name, birth, uid):
    errs = []
    if not re.fullmatch(r"[A-Za-z\s'-]+", name): errs.append("Invalid Name")
    try: datetime.strptime(birth.strip(), "%Y-%m-%d")
    except: errs.append("Invalid Date (YYYY-MM-DD)")
    if not uid.isdigit(): errs.append("Invalid ID")
    return errs

def get_result(score):
    if score <= 15: return "Very Low Effect"
    elif score <= 30: return "Search for other methods"
    elif score <= 50: return "Neutral Impact"
    elif score <= 60: return "High Calm Focus"
    else: return "Negative/Opposite Effect"

def save_csv(data):
    df = pd.DataFrame([data])
    f = "survey_results.csv"
    if os.path.exists(f): df = pd.concat([pd.read_csv(f), df], ignore_index=True)
    df.to_csv(f, index=False)

# --- Init State ---
for k, v in {'step': 0, 'info': {}, 'scores': {}}.items():
    if k not in st.session_state: st.session_state[k] = v

# --- Step 0: Info ---
if st.session_state.step == 0:
    st.title("🌿 Herbal Tea Survey")
    with st.form("info"):
        n = st.text_input("Name")
        b = st.text_input("DOB (YYYY-MM-DD)")
        i = st.text_input("Student ID")
        if st.form_submit_button("Start"):
            e = validate(n, b, i)
            if e: 
                for x in e: st.error(x)
            else:
                st.session_state.info = {"Name": n, "DOB": b, "ID": i}
                st.session_state.step = 1
                st.rerun()

# --- Step 1: Questions ---
elif st.session_state.step == 1:
    st.title("📝 Questions")
    qs = load_questions()
    with st.form("quiz"):
        temp_scores = {}
        for idx, item in enumerate(qs):
            st.markdown(f"**{idx+1}. {item['question']}**")
            # Create map for quick lookup: {"Never": 0, "Rarely": 1...}
            label_map = {opt['label']: opt['score'] for opt in item['options']}
            labels = list(label_map.keys())
            
            sel = st.radio("Choice", labels, key=f"q{idx}")
            temp_scores[idx] = label_map[sel]
        
        if st.form_submit_button("Submit"):
            st.session_state.scores = temp_scores
            st.session_state.step = 2
            st.rerun()

# --- Step 2: Results ---
else:
    st.title("📊 Results")
    total = sum(st.session_state.scores.values())
    res = get_result(total)
    
    c1, c2 = st.columns(2)
    c1.metric("Score", total)
    c2.metric("Result", res)
    
    if "High" in res: st.success("✅ Working well!")
    elif "Negative" in res: st.error("❌ Opposite effect")
    elif "Low" in res or "other" in res.lower(): st.warning("⚠️ Try other methods")
    else: st.info("ℹ️ Neutral")

    # Save
    row = {**st.session_state.info, "Score": total, "Result": res, "Time": datetime.now()}
    save_csv(row)
    st.success("Saved to survey_results.csv")
    
    if st.button("Restart"):
        st.session_state.step = 0
        st.session_state.scores = {}
        st.rerun()

    if os.path.exists("survey_results.csv"):
        with open("survey_results.csv", "rb") as f:
            st.download_button("📥 Download CSV", f, "survey_results.csv", "text/csv")
