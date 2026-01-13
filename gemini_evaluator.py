# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

# def evaluate_with_gemini(question, answer):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     prompt = f"Rate and review this answer:\nQuestion: {question}\nAnswer: {answer}"
#     response = model.generate_content(prompt)
#     return response.text


import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def evaluate_answer(question, answer):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = (
        f"You are an expert interviewer. Rate the answer for clarity, depth, and relevance. "
        f"Give a score out of 10 and constructive feedback.\n"
        f"Question: {question}\nAnswer: {answer}"
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content
