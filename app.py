import streamlit as st
from google import genai
from google.genai import types
import PyPDF2
import pandas as pd
import json
import io

# -------------------------------------------------------------------------
# 1. Page Configuration & Design
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="StudyStream - AI Exam Prep",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a professional look
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')

# -------------------------------------------------------------------------
# 2. CONSTANTS & SETUP
# -------------------------------------------------------------------------
# Try to get ACCESS_CODE from secrets, otherwise default (good for local testing)
if "ACCESS_CODE" in st.secrets:
    ACCESS_CODE = st.secrets["ACCESS_CODE"]
else:
    ACCESS_CODE = "HIREME2026" # Fallback/Default

SYSTEM_PROMPT = """
You are a strict university professor. Analyze the text and generate 10 difficult multiple-choice questions. 
Return ONLY a raw JSON array. Do not wrap in markdown code blocks.
Each object in the array must have:
- question (string)
- options (list of 4 strings)
- correct_answer (string - matching one of the options)
- explanation (string - why it is correct)
"""

# -------------------------------------------------------------------------
# 3. Helper Functions
# -------------------------------------------------------------------------
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'questions' not in st.session_state:
        st.session_state['questions'] = None
    if 'quiz_generated' not in st.session_state:
        st.session_state['quiz_generated'] = False

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def generate_quiz(text, api_key):
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[SYSTEM_PROMPT, text],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        # Clean up response if it contains markdown code blocks
        content = response.text.replace('```json', '').replace('```', '').strip()
        quiz_data = json.loads(content)
        return quiz_data
    except Exception as e:
        st.error(f"Error generating quiz: {e}")
        return None

def check_password():
    if st.session_state['password_input'] == ACCESS_CODE:
        st.session_state['authenticated'] = True
    else:
        st.session_state['error_message'] = "❌ Invalid Access Code. Please try again."

# -------------------------------------------------------------------------
# 4. Pages
# -------------------------------------------------------------------------
def login_page():
    # Centered Layout for Login using Columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("� StudyStream Login")
        st.markdown("Please enter the access code to continue.")
        
        st.text_input("Access Code", key="password_input", help="Enter the code from the resume", on_change=check_password)
        
        if st.button("Unlock App 🔓"):
            check_password()
        
        if 'error_message' in st.session_state:
            st.error(st.session_state['error_message'])
            del st.session_state['error_message']

def main_app():
    # Top bar for Title and Logout
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🎓 StudyStream</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Turn your slides into a Quiz instantly.</h3>", unsafe_allow_html=True)
    with col3:
        st.write("") # Add some spacing
        st.write("")
        if st.button("Logout", key="logout_btn", type="secondary"):
            st.session_state['authenticated'] = False
            st.rerun()

    # Check for API Key in secrets or input
    api_key = None
    
    # Try to get from secrets first
    if "GOOGLE_API_KEY" in st.secrets:
        secret_key = st.secrets["GOOGLE_API_KEY"]
        if secret_key and secret_key != "PASTE_YOUR_KEY_HERE":
            api_key = secret_key

    # If not found in secrets (or is placeholder), show input box
    if not api_key:
        api_key = st.text_input("Enter Google API Key", type="password", help="Get it from aistudio.google.com")

    if not api_key:
        st.warning("Please provide a Google API Key to proceed.")
        return

    # Feature B: PDF Ingestion
    uploaded_file = st.file_uploader("Upload Lecture Slides (PDF)", type=['pdf'])

    if uploaded_file is not None and not st.session_state['quiz_generated']:
        if st.button("Generate Quiz 🚀"):
            with st.spinner("Analyzing content and crafting questions..."):
                # Extract Text
                pdf_text = extract_text_from_pdf(uploaded_file)
                
                if pdf_text:
                    # Feature C: AI Brain
                    quiz_data = generate_quiz(pdf_text, api_key)
                    
                    if quiz_data:
                        st.session_state['questions'] = quiz_data
                        st.session_state['quiz_generated'] = True
                        st.rerun()

    # Feature D: Interactive Quiz UI
    if st.session_state['quiz_generated'] and st.session_state['questions']:
        st.markdown("---")
        st.write(f"### 📝 Knowledge Check ({len(st.session_state['questions'])} Questions)")
        
        questions = st.session_state['questions']
        
        for i, q in enumerate(questions):
            st.markdown(f"""
            <div style="background-color: #f0f4f8; border: 1px solid #cbd5e1; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <h4 style="color: #1e3a8a; margin-top: 0;">Q{i+1}: {q['question']}</h4>
            </div>
            """, unsafe_allow_html=True)
                
            # Unique key for each radio widget
            radio_key = f"q_radio_{i}"
            
            # Options
            options = q['options']
            
            user_choice = st.radio(
                f"Q{i+1} Options",
                options,
                key=radio_key,
                index=None,
                label_visibility="collapsed"
            )
            
            check_key = f"check_btn_{i}"
            
            if st.button("Check Answer", key=check_key):
                if user_choice:
                    if user_choice == q['correct_answer']:
                        st.success("✅ Correct! " + q['explanation'])
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: **{q['correct_answer']}**\n\n**Reason:** {q['explanation']}")
                else:
                    st.warning("Please select an option first.")
            
            st.markdown("---")

        # Feature E: Take Home Export
        st.subheader("💾 Save for Later")
        
        # Prepare CSV Data
        csv_data = []
        for q in questions:
            csv_data.append({
                "Question": q['question'],
                "Correct Answer": q['correct_answer'],
                "Explanation": q['explanation']
            })
        
        df = pd.DataFrame(csv_data)
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Quiz as CSV 📥",
            data=csv,
            file_name='study_quiz.csv',
            mime='text/csv',
        )
        
        if st.button("Start Over 🔄"):
            st.session_state['quiz_generated'] = False
            st.session_state['questions'] = None
            st.rerun()

# -------------------------------------------------------------------------
# 5. Main Application Entry Point
# -------------------------------------------------------------------------
init_session_state()

if st.session_state['authenticated']:
    main_app()
else:
    login_page()
