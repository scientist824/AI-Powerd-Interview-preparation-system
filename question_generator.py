import yaml
import random

def load_questions():
    # Changed path from data/question_bank.yaml to question_bank.yaml
    with open('question_bank.yaml', 'r') as f:
        return yaml.safe_load(f)

QUESTION_BANK = load_questions()

def generate_question(domain, difficulty="Medium", return_all=False):
    """
    Generates a question based on domain and difficulty.
    Fallback to 'Medium' or generic if specific path not found.
    """
    if domain in QUESTION_BANK:
        domain_questions = QUESTION_BANK[domain]
        # Check if difficulty exists for this domain
        if difficulty in domain_questions:
            questions = domain_questions[difficulty]
            return questions if return_all else random.choice(questions)
        
        # Fallback: try to find any questions if difficulty key is missing (backward compatibility)
        # or if the structure is flat (list instead of dict)
        if isinstance(domain_questions, list):
             return domain_questions if return_all else random.choice(domain_questions)
             
        # Fallback: flatten all difficulties if specific one not found
        all_questions = []
        for diff in domain_questions:
            if isinstance(domain_questions[diff], list):
                all_questions.extend(domain_questions[diff])
        
        if all_questions:
            return all_questions if return_all else random.choice(all_questions)

    return ["Tell me about yourself."] if return_all else "Tell me about yourself."

def generate_questions_from_resume(domain, resume_text, difficulty="Medium", language='English', round_type='Technical'):
    from groq import Groq
    import os
    
    # Ensure API key is present
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Fallback if no API key
        return generate_question(domain, difficulty=difficulty, return_all=True)

    client = Groq(api_key=api_key)
    prompt = (
        f"Resume:\n{resume_text}\n\n"
        f"Based on this résumé, generate exactly 5 distinct, {difficulty} level {round_type} interview questions for the '{domain}' domain in {language}. "
        "Number each question from 1 to 5. Only output the questions."
    )
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        raw = response.choices[0].message.content
        questions = []
        for line in raw.split('\n'):
            line = line.strip()
            if line and line[0].isdigit() and '.' in line[:3]:
                q = line.split('.', 1)[1].strip()
                if len(q) > 10:
                    questions.append(q)
        if not questions:
            questions = [line.strip() for line in raw.split('\n') if len(line.strip()) > 20]
        return questions
    except Exception as e:
        print(f"Error generating questions: {e}")
        return generate_question(domain, difficulty=difficulty, return_all=True)
