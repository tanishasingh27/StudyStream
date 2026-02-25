# StudyStream - Complete Project Documentation

**For Interview Preparation**

---

## 1. Key Concepts You Should Know for the Interview

This section covers all the fundamental concepts used in this project. Read this first — it will help you understand the code and answer any technical questions confidently.

---

### 1.1 What is Python?

Python is a high-level, general-purpose programming language. It is known for being easy to read and write. Python is widely used in web development, data science, artificial intelligence, automation, and more. In this project, Python is the only programming language used for all the application logic.

**Why Python for this project?**
- Huge ecosystem of libraries (Streamlit, PyPDF2, Pandas, Google GenAI)
- Easy to learn and write quickly
- The go-to language for AI/ML projects

---

### 1.2 What is Streamlit?

Streamlit is an **open-source Python framework** that lets you build interactive web applications using only Python. You do not need to write HTML, CSS, or JavaScript for the app logic. You just write Python functions like `st.button()`, `st.text_input()`, `st.radio()`, and Streamlit renders them as interactive web components in the browser.

**Key things about Streamlit:**
- **Rerun model:** Every time a user clicks a button or interacts with the app, the entire Python script runs again from top to bottom. This is different from traditional web frameworks like Flask or Django.
- **Widgets:** UI elements like buttons, text inputs, file uploaders, radio buttons are all built-in as simple Python function calls.
- **Session State:** Because the script reruns every time, Streamlit provides `st.session_state` — a dictionary that persists data across reruns.
- **Deployment:** Streamlit offers free hosting through Streamlit Community Cloud.

**Example:**

    import streamlit as st
    st.title("Hello World")
    name = st.text_input("Enter your name")
    if st.button("Greet"):
        st.write(f"Hello, {name}!")

This is all you need to create a working web page with an input box and a button.

---

### 1.3 What is an API?

API stands for **Application Programming Interface**. It is a set of rules that allow two software applications to talk to each other.

**Real-world analogy:** Think of a restaurant. You (the customer) don't go into the kitchen. You tell the waiter (the API) what you want, the waiter takes your order to the kitchen (the server), and the kitchen sends the food back through the waiter.

In our project:
- Our app (the customer) sends PDF text to Google's Gemini API (the waiter/kitchen)
- Gemini processes the text and sends back quiz questions
- Our app displays them

---

### 1.4 What is an API Key?

An API Key is a unique string of characters that identifies your application to the API provider. It is like a **password** for your app.

**Why do we need it?**
- Google needs to know WHO is making the request
- It tracks usage (how many requests you make)
- It enforces rate limits and billing

**Security rule:** Never hardcode API keys in your source code or push them to GitHub. Always store them in environment variables or secret managers.

In our project, the API key is stored in:
- **Locally:** `.streamlit/secrets.toml` (this file is in `.gitignore` so it is never committed to Git)
- **In production:** Streamlit Cloud's encrypted secrets dashboard

---

### 1.5 What is Google Gemini AI?

Google Gemini is a family of **Large Language Models (LLMs)** built by Google. LLMs are AI models trained on massive amounts of text data that can understand and generate human-like text.

**Model we use: `gemini-2.5-flash`**
- "Flash" means it is optimized for **speed** — it responds very quickly
- It has a **free tier** with generous limits
- It supports **structured output** — you can tell it to return data in JSON format, and it will always return valid JSON

**How we talk to Gemini:**
1. We create a `Client` object with our API key
2. We call `client.models.generate_content()` with two things:
   - A **system prompt** (instructions for the AI)
   - The **PDF text** (the content to generate questions from)
3. Gemini returns a response containing quiz questions in JSON format

---

### 1.6 What is Prompt Engineering?

Prompt engineering is the practice of writing clear, specific instructions for an AI model to get the best possible output.

**Our system prompt:**

    You are a strict university professor. Analyze the text and generate 10 difficult
    multiple-choice questions. Return ONLY a raw JSON array.
    Each object must have:
    - question (string)
    - options (list of 4 strings)
    - correct_answer (string - matching one of the options)
    - explanation (string - why it is correct)

**Why is this prompt important?**
- "strict university professor" → sets the tone and difficulty level
- "10 difficult multiple-choice questions" → specifies the exact count and type
- "Return ONLY a raw JSON array" → prevents the AI from adding extra text
- The field list → defines the exact structure we expect

If you don't write a good prompt, the AI might return questions in a random format that our code can't parse.

---

### 1.7 What is JSON?

JSON (JavaScript Object Notation) is a lightweight data format used to exchange data between systems. It uses **key-value pairs** and is easy for both humans and machines to read.

**Example of one quiz question in JSON:**

    {
      "question": "What is the capital of France?",
      "options": ["London", "Paris", "Berlin", "Madrid"],
      "correct_answer": "Paris",
      "explanation": "Paris has been the capital of France since the 10th century."
    }

**In our app:**
- The AI returns a JSON **array** (a list) of 10 such objects
- We use Python's `json.loads()` to convert this JSON string into a Python list of dictionaries
- Then we loop through each dictionary to display the question and options

---

### 1.8 What is Session State in Streamlit?

In Streamlit, the **entire Python script reruns from top to bottom** every time the user interacts with any widget (clicks a button, types something, selects a radio button, etc.).

This means if you store data in a normal Python variable, it will be lost on every rerun.

**Session State** is Streamlit's solution — it is a persistent dictionary (`st.session_state`) that survives across reruns.

**In our app, we store three things:**
- `st.session_state['authenticated']` → Has the user logged in? (True/False)
- `st.session_state['questions']` → The generated quiz data (a list of question objects)
- `st.session_state['quiz_generated']` → Has a quiz been generated already? (True/False)

**Without session state:** Every time you click "Check Answer", the page would rerun, the quiz data would disappear, and you'd see a blank page.

---

### 1.9 What is a Virtual Environment (venv)?

A virtual environment is an **isolated Python installation** that keeps your project's packages separate from your system Python and other projects.

**Why do we need it?**
- Project A might need `pandas 1.5` and Project B might need `pandas 2.0`
- Without venv, they'd conflict
- With venv, each project has its own independent set of packages

**How to use it:**

    python -m venv venv          # Create a virtual environment named "venv"
    venv\Scripts\activate        # Activate it (Windows)
    pip install -r requirements.txt  # Install project-specific packages
    deactivate                   # Deactivate when done

---

### 1.10 What is requirements.txt?

`requirements.txt` is a file that lists all the Python packages your project needs. When someone new clones your project, they run `pip install -r requirements.txt` to install everything.

**Our requirements.txt:**

    streamlit
    google-genai
    PyPDF2
    pandas

---

### 1.11 What is Git and GitHub?

**Git** is a version control system. It tracks changes to your code over time so you can go back to previous versions, collaborate with others, and manage multiple features.

**GitHub** is a website that hosts Git repositories online. It lets you share code, collaborate, and deploy applications.

**Key Git commands used in this project:**
- `git init` → Initialize a new repository
- `git add .` → Stage all files for commit
- `git commit -m "message"` → Save a snapshot of your code
- `git remote add origin <url>` → Connect to a GitHub repository
- `git push -u origin main` → Upload code to GitHub

---

### 1.12 What is .gitignore?

`.gitignore` is a file that tells Git which files and folders to **ignore** (not track or upload). This is crucial for:

- **Security:** Never push API keys or secrets (`secrets.toml`)
- **Size:** Don't push the virtual environment folder (`venv/`) — it can be hundreds of MB
- **Cleanliness:** Don't push Python cache files (`__pycache__/`)

---

### 1.13 What is CSS? How is it used here?

CSS (Cascading Style Sheets) is a language used to control the **visual appearance** of HTML elements — colors, sizes, spacing, fonts, animations, etc.

**In Streamlit**, you can inject custom CSS using `st.markdown()` with `unsafe_allow_html=True`. We use CSS to:
- Set the background gradient
- Style buttons (dark blue, rounded corners)
- Style the radio option boxes (fixed height, light gray background)
- Hide the sidebar
- Override Streamlit's default styles using `!important`

**Why a separate CSS file?**
It follows the principle of **Separation of Concerns** — keeping styling separate from logic makes the codebase cleaner and easier to maintain.

---

### 1.14 What is Streamlit Community Cloud?

Streamlit Community Cloud is a **free hosting platform** specifically for Streamlit apps. You connect your GitHub repo, and it automatically:
1. Pulls your code
2. Installs dependencies from `requirements.txt`
3. Runs `app.py`
4. Gives you a public URL

**Secrets management:** You can add API keys and other secrets through the dashboard. They are encrypted and injected at runtime via `st.secrets`.

---

### 1.15 What is Error Handling (try/except)?

Error handling is the practice of anticipating and gracefully handling things that can go wrong in your code.

**In Python, we use try/except:**

    try:
        # Code that might fail
        result = risky_operation()
    except Exception as e:
        # What to do if it fails
        print(f"Error: {e}")

**In our app, we handle errors in:**
- PDF reading — the file might be corrupted or password-protected
- AI API calls — the network might be down, the API key might be invalid, or the AI might return unexpected data
- JSON parsing — the AI might occasionally return malformed JSON

Instead of the app crashing, the user sees a friendly error message via `st.error()`.

---

### 1.16 What is MIME Type?

MIME (Multipurpose Internet Mail Extensions) type is a label that tells a system what kind of data it is receiving.

**Used in two places in our app:**
- `response_mime_type="application/json"` → Tells Gemini AI to return JSON format only
- `mime='text/csv'` → Tells the browser that the download is a CSV file

---

### 1.17 What is a DataFrame (Pandas)?

A DataFrame is a **2D table** (rows and columns) provided by the Pandas library. Think of it like an Excel spreadsheet in Python.

**In our app:**

    df = pd.DataFrame(csv_data)      # Create table from quiz data
    csv = df.to_csv(index=False)     # Convert table to CSV string

We use it to organize quiz questions, correct answers, and explanations into a downloadable CSV file.

---

### 1.18 What is PyPDF2?

PyPDF2 is a Python library that reads PDF files and extracts their text content. It works by:
1. Opening the PDF file
2. Iterating through each page
3. Extracting the text from each page
4. Combining all the text into one string

**Limitation:** It works best with text-based PDFs. If the PDF contains scanned images (like a photograph of a document), PyPDF2 cannot read it — you would need OCR (Optical Character Recognition) for that.

---

---

## 2. What is StudyStream?

StudyStream is an **AI-powered web application** that helps students prepare for exams. You upload a PDF of your lecture slides, and the app automatically generates a **10-question multiple-choice quiz** from the content using Google's Gemini AI.

**In one line for the interview:** "It's a Streamlit web app that uses Google Gemini AI to convert lecture PDFs into interactive MCQ quizzes."

---

## 3. Tech Stack

| Technology | What It Does | Why We Chose It |
|---|---|---|
| **Python** | Programming language for all logic | Easy to learn, huge ecosystem, great for AI projects |
| **Streamlit** | Web application framework | Build web apps using only Python, no HTML/JS needed |
| **Google Gemini AI (gemini-2.5-flash)** | AI model for generating quiz questions | Free tier, fast, supports structured JSON output |
| **PyPDF2** | Extract text from PDF files | Simple and lightweight PDF reader |
| **Pandas** | Data manipulation | Convert quiz data into downloadable CSV |
| **CSS** | UI styling | Professional, custom look for the app |

---

## 4. How Does the App Work? (Flow)

    User opens the app
      --> Login Page (enter access code "HIREME2026")
          --> Main Page
              --> Upload a PDF file
                  --> Click "Generate Quiz"
                      --> PyPDF2 extracts text from the PDF
                          --> Text + System Prompt sent to Gemini AI
                              --> AI returns 10 MCQs as JSON
                                  --> App displays questions with radio buttons
                                      --> User selects answers and clicks "Check Answer"
                                          --> App shows correct/incorrect with explanation
                                              --> User can download quiz as CSV

---

## 5. Project Structure

    StudyStream/
    +-- .streamlit/
    |   +-- config.toml          # Sets Streamlit to use light theme
    |   +-- secrets.toml         # API keys (never pushed to GitHub)
    +-- app.py                   # Main application logic
    +-- style.css                # All CSS styling
    +-- requirements.txt         # Python package list
    +-- run.bat                  # Windows launcher script
    +-- .gitignore               # Files to exclude from Git
    +-- README.md                # Setup instructions

---

## 6. Detailed Code Explanation (app.py)

### 6.1 Imports

    import streamlit as st          # Web framework
    from google import genai         # Google Gemini AI SDK
    from google.genai import types   # Config types for Gemini
    import PyPDF2                    # PDF text extraction
    import pandas as pd              # Data handling (CSV export)
    import json                      # Parse JSON from AI

- **streamlit (st):** The web framework. Every UI element is created using `st.something()`.
- **google.genai:** The official Google Gemini SDK (package name: `google-genai`). We use it to send text to the AI and receive quiz questions.
- **PyPDF2:** Reads PDF files and extracts text from each page.
- **pandas:** Data analysis library. We use it to create a downloadable CSV.
- **json:** Built-in Python module to convert JSON strings into Python dictionaries.

### 6.2 Page Configuration

    st.set_page_config(
        page_title="StudyStream - AI Exam Prep",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

- Sets the browser tab title and favicon
- `layout="wide"` uses the full screen width
- Sidebar is collapsed since we do not use it

### 6.3 Loading CSS

    def load_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    load_css('style.css')

- Reads CSS from the external file and injects it into the page
- `unsafe_allow_html=True` is required because Streamlit blocks raw HTML by default

### 6.4 Secrets Management

    if "ACCESS_CODE" in st.secrets:
        ACCESS_CODE = st.secrets["ACCESS_CODE"]
    else:
        ACCESS_CODE = "HIREME2026"

- `st.secrets` reads from `.streamlit/secrets.toml` locally, or from Streamlit Cloud's dashboard in production
- Falls back to a default value if no secret is configured

### 6.5 System Prompt

    SYSTEM_PROMPT = """
    You are a strict university professor. Analyze the text and generate 10 difficult
    multiple-choice questions. Return ONLY a raw JSON array...
    """

- This is the instruction we send to the AI along with the PDF text
- The AI follows these instructions to produce structured output
- The quality of the output depends on how well this prompt is written

### 6.6 Session State Initialization

    def init_session_state():
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'questions' not in st.session_state:
            st.session_state['questions'] = None
        if 'quiz_generated' not in st.session_state:
            st.session_state['quiz_generated'] = False

- Sets up persistent variables that survive page reruns
- Without this, data would be lost every time the user clicks anything

### 6.7 PDF Text Extraction

    def extract_text_from_pdf(uploaded_file):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

- Creates a PDF reader from the uploaded file
- Loops through every page and extracts the text
- Returns all page texts combined as one string

### 6.8 Quiz Generation (AI Call)

    def generate_quiz(text, api_key):
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[SYSTEM_PROMPT, text],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        content = response.text
        quiz_data = json.loads(content)
        return quiz_data

- Creates a Gemini API client with the API key
- Sends the system prompt and PDF text to the AI
- `response_mime_type="application/json"` forces the AI to output valid JSON
- `json.loads()` converts the JSON string to a Python list

### 6.9 Authentication

    def check_password():
        if st.session_state['password_input'] == ACCESS_CODE:
            st.session_state['authenticated'] = True

- Simple string comparison against the access code
- Sets `authenticated = True` in session state so the main page shows on next rerun

### 6.10 Quiz Display

    user_choice = st.radio(
        f"Q{i+1} Options",
        options,
        key=radio_key,
        index=None,
        label_visibility="collapsed"
    )

- `st.radio()` creates single-select radio buttons
- `key=radio_key` gives each question a unique identifier
- `index=None` means no option is pre-selected
- `label_visibility="collapsed"` hides the redundant label

### 6.11 CSV Export

    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Quiz as CSV", data=csv, ...)

- Converts quiz data into a Pandas DataFrame (a table)
- Exports it as a CSV string, encoded to bytes
- `st.download_button()` gives the user a one-click download

### 6.12 Main Entry Point

    init_session_state()
    if st.session_state['authenticated']:
        main_app()
    else:
        login_page()

- Initializes session variables
- Routes to login or main page based on authentication status

---

## 7. CSS Styling Explained (style.css)

| CSS Rule | What It Styles |
|---|---|
| `.main` | Background gradient (light gray to light blue) |
| `h1` | Title text — dark blue (#1e3a8a), bold |
| `div[data-testid="stRadio"]` | Answer option boxes — fixed 220px height, light gray, rounded |
| `.stButton > button` | All buttons — dark blue, white text, rounded, hover effects |
| `.stDownloadButton > button` | Download button — green to differentiate |
| `section[data-testid="stSidebar"]` | Hides the sidebar completely |

**`!important` keyword:** Forces our styles to override Streamlit's built-in styles, which are otherwise difficult to change.

**`data-testid` selectors:** Streamlit adds `data-testid` attributes to its HTML elements. We use these to precisely target specific Streamlit components in CSS.

---

## 8. Deployment

**Platform:** Streamlit Community Cloud (free)

**How deployment works:**
1. Code is pushed to GitHub
2. On Streamlit Cloud, you connect the GitHub repo
3. Streamlit Cloud installs packages from `requirements.txt`
4. It runs `app.py` and gives you a public URL
5. Secrets (API key, access code) are set in the dashboard — encrypted, never in code

**URL format:** `https://yourname-appname.streamlit.app`

---

## 9. Interview Questions and Answers

**Q: What problem does this project solve?**

A: "Students often have lecture slide PDFs but no practice questions. Manually creating quizzes is time-consuming. This app automates quiz generation using AI, saving hours of work."

**Q: Why did you choose Streamlit over Flask or Django?**

A: "Streamlit is designed for data and AI apps. It lets you build a full UI using only Python — no HTML templates or JavaScript needed. For a focused tool like a quiz generator, Streamlit is much faster to develop and deploy compared to Flask or Django."

**Q: Why Gemini 2.5 Flash instead of GPT-4 or other models?**

A: "Three reasons: (1) It has a generous free tier. (2) It is optimized for speed — the 'Flash' variant responds very quickly. (3) It natively supports structured JSON output via `response_mime_type`, which means we can guarantee the AI always returns valid, parseable data."

**Q: How do you handle errors in the application?**

A: "All risky operations — PDF reading, API calls, JSON parsing — are wrapped in try/except blocks. If anything fails, the user sees a friendly error message via `st.error()` instead of the app crashing with a stack trace."

**Q: How do you ensure the AI returns valid, parseable data?**

A: "Two mechanisms: First, the system prompt explicitly instructs the AI to return only a JSON array with specific fields. Second, we set `response_mime_type='application/json'` in the API configuration, which is a hard constraint that forces the model to output syntactically valid JSON."

**Q: How are secrets and API keys managed securely?**

A: "API keys are never hardcoded in the source code. Locally, they are stored in `.streamlit/secrets.toml`, which is excluded from Git via `.gitignore`. In production on Streamlit Cloud, secrets are configured through an encrypted dashboard and injected at runtime via `st.secrets`."

**Q: What is session state and why do you need it?**

A: "Streamlit reruns the entire Python script on every user interaction. Without session state, all variables would reset on each rerun — the quiz data would disappear every time someone clicks a button. `st.session_state` is a persistent dictionary that lets us store the login status, quiz data, and other state across reruns."

**Q: Is this app scalable? What would you improve?**

A: "Currently it is a single-user stateless app. To scale, I would add: (1) a database for user accounts and quiz history, (2) caching with `@st.cache_data` to avoid re-processing the same PDFs, (3) support for more file types like DOCX and PPTX, (4) difficulty level selection, (5) a timed quiz mode, and (6) deployment on a cloud platform like GCP or AWS with load balancing for handling many concurrent users."

**Q: What is the difference between `google-generativeai` and `google-genai`?**

A: "They are both Python SDKs for Google's Gemini AI, but `google-generativeai` is the old, deprecated version. `google-genai` is the new official SDK with a different API structure — instead of `genai.configure()` and `genai.GenerativeModel()`, it uses a `Client` object pattern: `genai.Client()` and `client.models.generate_content()`. The old models like `gemini-pro` have also been retired and replaced with newer models like `gemini-2.5-flash`."

**Q: Walk me through what happens when a user uploads a PDF and clicks Generate Quiz.**

A: "Step by step: (1) The user selects a PDF file via `st.file_uploader()`. (2) When they click Generate Quiz, PyPDF2 reads the file and extracts all text from every page. (3) This text, along with a system prompt, is sent to Google's Gemini 2.5 Flash API. (4) The API processes the content and returns 10 multiple-choice questions as a JSON array. (5) We parse this JSON into Python objects and store them in `st.session_state`. (6) The page reruns and renders each question with radio buttons using `st.radio()`. (7) The user can check answers, see explanations, and download the quiz as a CSV."
