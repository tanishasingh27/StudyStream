# 🎓 StudyStream - AI Exam Prep

StudyStream is a Streamlit application that uses Google Gemini AI to turn lecture PDFs into interactive multiple-choice quizzes.

## 🚀 How to Host (Free via Streamlit Cloud)

1.  **Push to GitHub**: Upload this project code to a GitHub repository.
2.  **Deploy**:
    -   Go to [share.streamlit.io](https://share.streamlit.io/).
    -   Connect your GitHub and select this repository.
    -   Click **"Advanced Settings"** -> **"Secrets"**.
3.  **Configure Secrets**: Paste the following into the Secrets area:
    ```toml
    GOOGLE_API_KEY = "your_actual_api_key"
    ACCESS_CODE = "HIREME2026"
    ```
4.  **Launch**: Click Deploy! 🎈

## 💻 Developer Installation Guide

### Prerequisites
- Python 3.9+
- A Google Gemini API Key

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd StudyStream
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Local Secrets Setup
Create a file at `.streamlit/secrets.toml` and add your keys:
```toml
GOOGLE_API_KEY = "your_api_key_here"
ACCESS_CODE = "HIREME2026"
```

### 4. Run Locally
```bash
streamlit run app.py
```
Or use the provided batch file (Windows):
```bash
run.bat
```

## 📂 Project Structure
```
StudyStream/
├── .streamlit/
│   ├── config.toml        # Streamlit theme configuration
│   └── secrets.toml       # Local API keys (do not share)
├── app.py                 # Main application code
├── style.css              # UI styling
├── requirements.txt       # Python dependencies
├── run.bat                # Windows launcher script
├── .gitignore             # Git ignore rules
└── README.md              # This file
```
