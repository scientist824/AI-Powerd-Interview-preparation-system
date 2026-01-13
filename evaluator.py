import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def evaluate_answer(question, answer, language="English", round_type="Technical", difficulty="Medium", domain="DSA"):
    """
    Evaluates a candidate's answer using an LLM, providing a score (out of 10) and detailed feedback.
    Supports multilingual feedback, round (HR/Technical) adaptation, difficulty-based scoring, and domain-specific checks.
    """
    if not GROQ_API_KEY:
        return f"Score: 5/10\nFeedback: (API Key missing) Please explain {question} in more detail."

    client = Groq(api_key=GROQ_API_KEY)
    
    # Define difficulty-specific evaluation criteria
    difficulty_criteria = ""
    if difficulty == "Easy":
        difficulty_criteria = "Score leniently. High score if the definition is correct and basic keywords are present."
    elif difficulty == "Medium":
        difficulty_criteria = "Score moderately. The answer must explain the concept clearly and ideally provide an example."
    elif difficulty == "Hard":
        difficulty_criteria = "Score strictly. The answer must explain internal workings, edge cases, trade-offs, or advanced details."
    
    # Define domain-specific evaluation criteria
    domain_criteria = ""
    if domain == "Python":
        domain_criteria = "Check for usage of correct Python terminology (e.g., list, dict, class, __init__, decorators, GIL). Ensure code snippets (if any) are Pythonic."
    elif domain == "Java":
        domain_criteria = "Check for usage of correct Java terminology (e.g., class, object, inheritance, JVM, Garbage Collection, interfaces). Ensure adherence to Java conventions."

    prompt = (
        f"You are an expert {round_type} interviewer evaluating a {difficulty} level question for the '{domain}' domain.\n"
        f"Question: {question}\n"
        f"Candidate Answer: {answer}\n\n"
        f"Difficulty Criteria: {difficulty_criteria}\n"
        f"Domain Criteria: {domain_criteria}\n\n"
        f"Provide the evaluation in {language} with the following strict format:\n"
        "Score: X/10\n"
        "Strengths: [Bullet points]\n"
        "Weaknesses: [Bullet points]\n"
        "Improvement Tips: [Bullet points]\n"
        "Feedback: [General summary]"
    )
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during evaluation: {e}"
