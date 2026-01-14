<<<<<<< HEAD
<<<<<<< HEAD
AI Interview Preparation System 🎤🤖
An AI-powered interview preparation web app built with Streamlit, LangChain-style RAG, LLaMA 3, and Whisper.
It generates domain-specific interview questions, evaluates candidate answers (text/voice), and provides personalized AI feedback.
The system supports resume-based tailoring, session history tracking, and PDF export for offline review.
<img width="1919" height="927" alt="Screenshot 2025-09-04 153401" src="https://github.com/user-attachments/assets/56d27c47-178d-41f2-a4b1-d7ea5ea96ac5" />



AI Interview Preparation System
An interactive AI-powered interview preparation web app built with Streamlit. It supports text and voice inputs, allows users to upload resumes for personalized domain-specific questions, evaluates answers with AI-generated feedback, and keeps session history with PDF export.

## 🧠 Overview
The **AI Interview Preparation System** is an interactive **AI-powered web app** built with **Streamlit, LangChain-style RAG, LLaMA 3, and Whisper**.  
It generates **domain-specific interview questions**, evaluates answers (text/voice), and provides **personalized AI-driven feedback**.  

📄 Upload your **resume**, 🎤 practice answers via **voice or text**, and 📊 export your full interview session as **PDF**.  

---

## ✨ Key Features
- 🎓 **Domain Selection** → DSA, DBMS, OOP, ML, HR, Cloud  
- 📑 **Resume Upload** (PDF/DOCX) → Tailored, domain-specific questions  
- 🔄 **Non-repetitive Question Generation**  
- 🎙️ **Answer via Text or Voice** (Whisper API for STT)  
- 📈 **AI-powered Evaluation** → Scoring + detailed feedback  
- 🕒 **Session History Tracking**  
- 📤 **Export Conversations as PDF**  
- 🎨 **Clean, intuitive Streamlit UI** with sidebar instructions  

---

## ⚙️ Installation & Setup

### 🔹 Prerequisites
- Python **3.8+**
- API Keys:
  - [Groq API](https://groq.com) → AI question generation & evaluation  
  - [Hugging Face API](https://huggingface.co) → Whisper speech-to-text  

### 🔹 Clone Repository
```bash
git clone https://github.com/yourusername/ai-interview-prep.git
cd ai-interview-prep


🔹 Virtual Environment
python -m venv venv


Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

🔹 Install Dependencies
pip install -r requirements.txt

🔹 API Configuration

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here
HF_API_TOKEN=your_huggingface_api_token_here


Update modules/whisper_stt.py:

headers = {"Authorization": "Bearer YOUR_HF_ACCESS_TOKEN"}

▶️ Usage

Run the app:

streamlit run app.py


Open in browser → http://localhost:8501

📝 Workflow

Select an interview domain from sidebar.

(Optional) Upload resume for personalized questions.

Click Generate Question.

Answer by typing or uploading a voice recording (WAV/MP3).

Click Evaluate Answer → Get AI score & feedback.

Export session as PDF.

Review session history anytime.

📂 Project Structure
ai-interview-prep/
│── app.py
│── requirements.txt
│── .env
│
├── modules/
│   ├── question_generator.py   # Generates domain-specific questions
│   ├── evaluator.py            # Evaluates answers
│   ├── feedback.py             # AI feedback system
│   ├── whisper_stt.py          # Voice-to-text using Whisper
│
├── utils/
│   ├── pdf_export.py           # Export session as PDF
│   ├── resume_extract.py       # Extracts resume details
│
├── dashboard/
│   └── history.py              # Session tracking & dashboard
│
├── data/
│   └── question_bank.yaml      # Predefined question set
│
├── static/
│   ├── logo.png
│   └── style.css               # Custom UI styles


It is aslo evaluted 
<img width="1909" height="908" alt="Screenshot 2025-09-04 153345" src="https://github.com/user-attachments/assets/e402ee3e-a196-4dea-82fa-f8adc519e4d1" />



=======
# AI-Powerd-Interview-preparation-system
clint college project two
>>>>>>> ef75871a2216fcc067fc25cb338ba59f44d83328
=======
# AI-Powerd-Interview-preparation-system
clint college project two
>>>>>>> ef75871a2216fcc067fc25cb338ba59f44d83328
