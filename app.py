import streamlit as st
from question_generator import generate_question, generate_questions_from_resume
from evaluator import evaluate_answer
from feedback import format_feedback
from history import show_history
from pdf_export import export_interview_session
import whisper_stt
from io import BytesIO
from gtts import gTTS
import tempfile
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import io
import wave
import resume_extract as rext
import resume_scorer
import random

# Map UI languages to gtts language codes
LANG_CODE_MAP = {'English': 'en', 'Hindi': 'hi', 'Odia': 'or'}

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp.read(), format='audio/mp3')

def audio_frame_callback(frame):
    audio = frame.to_ndarray(format="s16", layout="mono")
    return av.AudioFrame.from_ndarray(audio, layout="mono")

# App configuration
st.set_page_config(page_title="AI Interview Preparation System", layout="wide")

# App heading
st.markdown("<h1 style='text-align: center;'>AI Interview Preparation System</h1>", unsafe_allow_html=True)

# Sidebar instructions and logo
st.sidebar.image("logo.png", width=120)
st.sidebar.markdown("""
# Instructions
- Select a domain
- Optionally upload resume (.pdf/.docx)
- Select interview round and language
- Click Generate Question
- Type your answer
- Click Evaluate!
""")

# Sidebar controls
DOMAIN_LIST = ["DSA", "DBMS", "OOP", "ML", "HR", "Cloud", "Python", "Java"]
domain = st.sidebar.selectbox("Select Domain", DOMAIN_LIST, index=0)

ROUNDS = ["Technical", "HR"]
round_type = st.sidebar.selectbox("Select Interview Round", ROUNDS, index=0)

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
difficulty = st.sidebar.selectbox("Select Difficulty", DIFFICULTY_LEVELS, index=1)

# Default language to English (User requested removal of language selection)
language = "English"

resume_file = st.sidebar.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
if resume_file:
    resume_text = rext.extract_resume_text(resume_file)
    st.sidebar.success("Resume uploaded!")
    
    # Resume Scoring
    score_data = resume_scorer.calculate_resume_score(resume_text, domain, difficulty)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Resume Score")
    st.sidebar.progress(score_data['resume_score'] / 100)
    st.sidebar.markdown(f"**Score: {score_data['resume_score']}/100**")
    
    if score_data['resume_score'] >= 80:
        st.sidebar.success("Excellent match!")
    elif score_data['resume_score'] >= 50:
        st.sidebar.warning("Good match, room for improvement.")
    else:
        st.sidebar.error("Low match.")
        
    with st.sidebar.expander("Detailed Analysis"):
        if score_data['strengths']:
            st.write("**Strengths:**")
            for s in score_data['strengths']:
                st.write(f"- {s}")
        if score_data['gaps']:
            st.write("**Gaps:**")
            for g in score_data['gaps']:
                st.write(f"- {g}")
        if score_data['suggestions']:
            st.write("**Suggestions:**")
            for s in score_data['suggestions']:
                st.write(f"- {s}")
        st.write(f"**Recommended Difficulty:** {score_data['recommended_difficulty']}")

    st.sidebar.write("Resume preview:", resume_text[:300])
else:
    resume_text = ""

# Session state initialization
if "asked_questions" not in st.session_state:
    st.session_state["asked_questions"] = {}
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "answer_stt" not in st.session_state:
    st.session_state["answer_stt"] = ""

# Question generation
if st.button("Generate Question"):
    if resume_text:
        questions = generate_questions_from_resume(domain, resume_text, difficulty=difficulty, language=language, round_type=round_type)
    else:
        questions = generate_question(domain, difficulty=difficulty, return_all=True)
    asked = st.session_state["asked_questions"].get(domain, set())
    available = [q for q in questions if q not in asked]
    if not available:
        st.session_state["asked_questions"][domain] = set()
        available = questions
    
    # Automatically pick a random question (User requested removal of selection)
    question = random.choice(available)
    
    st.session_state["question"] = question
    st.session_state["asked_questions"].setdefault(domain, set()).add(question)
    st.session_state["questions"] = questions
    st.session_state["answer_stt"] = ""  # reset STT answer on new question

if "question" in st.session_state:
    st.subheader("Question")
    st.write(st.session_state["question"])

    gtts_lang_code = LANG_CODE_MAP.get(language, 'en')
    if st.button("🔊 Listen to Question"):
        speak_text(st.session_state["question"], lang=gtts_lang_code)

    # Get typed answer, default from STT if present
    typed_answer = st.text_area(
        "Type your answer (or paste STT):",
        value=st.session_state.get("answer_stt", ""),
        key="typed_answer"
    )

    # TTS for user's answer
    if typed_answer:
        if st.button("🔊 Listen to Your Answer"):
            speak_text(typed_answer, lang=gtts_lang_code)

    # Evaluate using latest answer in typed_answer box
    if st.button("Evaluate Answer"):
        currently_typed = st.session_state.get("typed_answer", "").strip()
        if not currently_typed:
            st.warning("Please provide your answer before evaluation.")
        else:
            with st.spinner("Evaluating your answer..."):
                feedback = evaluate_answer(st.session_state["question"], currently_typed, language=language, round_type=round_type, difficulty=difficulty, domain=domain)
                feedback = format_feedback(feedback)
                st.session_state.setdefault("history", []).append({
                    "question": st.session_state["question"],
                    "answer": currently_typed,
                    "feedback": feedback,
                })
                st.subheader("Feedback & Score")
                st.write(feedback)

            if st.button("Export as PDF"):
                export_interview_session(st.session_state["history"])
                st.success("Exported to PDF!")

st.markdown("---")
st.subheader("Session History")
show_history()
