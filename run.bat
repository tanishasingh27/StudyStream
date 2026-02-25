@echo off
cd /d "d:\Jai Mata Di\StudyStream"

IF NOT EXIST venv (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

echo 🚀 Activating environment...
call venv\Scripts\activate

echo 📥 Checking dependencies...
pip install -r requirements.txt

echo 🎓 Starting StudyStream...
streamlit run app.py
pause
