import re

def calculate_resume_score(resume_text, domain, difficulty):
    """
    Calculates a Resume Score (0-100) based on domain keywords, experience, and difficulty.
    Returns a structured dictionary with score, feedback, and recommendations.
    """
    if not resume_text:
        return {
            "resume_score": 0,
            "strengths": [],
            "gaps": ["No resume text found"],
            "suggestions": ["Upload a valid PDF or DOCX file"],
            "recommended_difficulty": "Easy"
        }

    resume_text_lower = resume_text.lower()
    
    # 1. Define Keywords
    keywords = {
        "Python": [
            'list', 'dict', 'set', 'tuple', 'class', 'object', 'inheritance', 'polymorphism', 
            'encapsulation', 'abstraction', 'decorator', 'generator', 'lambda', 'exception', 
            'try', 'except', 'pandas', 'numpy', 'flask', 'django', 'fastapi', 'sqlalchemy', 
            'api', 'rest', 'json', 'pip', 'virtualenv', 'gil', 'threading', 'multiprocessing', 
            'asyncio', 'await', 'magic methods', 'pep8'
        ],
        "Java": [
            'class', 'object', 'interface', 'abstract', 'inheritance', 'polymorphism', 
            'encapsulation', 'override', 'overload', 'constructor', 'static', 'final', 
            'this', 'super', 'try', 'catch', 'throw', 'throws', 'collection', 'list', 
            'map', 'set', 'arraylist', 'hashmap', 'jvm', 'jdk', 'jre', 'thread', 'runnable', 
            'synchronize', 'spring', 'hibernate', 'maven', 'gradle', 'junit', 'stream api'
        ],
        "DSA": ['array', 'linked list', 'stack', 'queue', 'tree', 'graph', 'hashing', 'recursion', 'sorting', 'searching', 'complexity', 'big o'],
        "DBMS": ['sql', 'nosql', 'normalization', 'acid', 'transaction', 'index', 'primary key', 'foreign key', 'join', 'view', 'trigger'],
        "OOP": ['class', 'object', 'inheritance', 'polymorphism', 'encapsulation', 'abstraction', 'solid', 'design patterns'],
        "ML": ['regression', 'classification', 'clustering', 'neural network', 'deep learning', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
        "HR": ['communication', 'teamwork', 'leadership', 'problem solving', 'adaptability', 'time management', 'conflict resolution'],
        "Cloud": ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'serverless', 'ec2', 's3', 'lambda', 'devops', 'ci/cd']
    }

    domain_keywords = keywords.get(domain, [])
    if not domain_keywords:
        # Fallback for domains not strictly defined or if generic
        domain_keywords = keywords.get("Python") + keywords.get("Java")

    # 2. Scoring Logic
    
    # A. Keyword Matching (50 points max)
    found_keywords = [kw for kw in domain_keywords if kw in resume_text_lower]
    unique_keywords = set(found_keywords)
    keyword_score = min(50, len(unique_keywords) * 3)  # ~17 keywords to max out

    # B. Experience Indicators (30 points max)
    experience_keywords = ['experience', 'work', 'internship', 'project', 'developer', 'engineer', 'analyst', 'role', 'responsibilities']
    exp_matches = [w for w in experience_keywords if w in resume_text_lower]
    experience_score = min(30, len(set(exp_matches)) * 5) # 6 words to max out

    # C. Formatting/Structure/Readiness (20 points max)
    # Heuristic: Length of text (too short = bad, too long = maybe ok)
    word_count = len(resume_text.split())
    if word_count < 100:
        structure_score = 5
    elif word_count < 300:
        structure_score = 10
    else:
        structure_score = 20

    total_score = keyword_score + experience_score + structure_score

    # 3. Generate Feedback
    strengths = []
    gaps = []
    suggestions = []

    if keyword_score > 40:
        strengths.append(f"Strong usage of {domain} terminology")
    elif keyword_score > 20:
        strengths.append(f"Moderate familiarity with {domain} concepts")
    else:
        gaps.append(f"Limited {domain}-specific keywords found")
        suggestions.append(f"Add more {domain} technical terms (e.g., {', '.join(domain_keywords[:3])})")

    if experience_score > 20:
        strengths.append("Clear experience/project indicators")
    else:
        gaps.append("Resume might lack clear Project or Experience sections")
        suggestions.append("Highlight your projects and work experience clearly")

    # 4. Difficulty Readiness
    recommended_difficulty = "Easy"
    if total_score >= 80:
        recommended_difficulty = "Hard"
    elif total_score >= 50:
        recommended_difficulty = "Medium"
    
    # 5. Difficulty Alignment Check
    # If user selected 'Hard' but score is low, warn them.
    # If user selected 'Easy' but score is high, suggest moving up.
    if difficulty == "Hard" and recommended_difficulty != "Hard":
        suggestions.append("Consider starting with Medium questions first")
    elif difficulty == "Easy" and recommended_difficulty == "Hard":
        suggestions.append("You seem ready for Hard questions!")

    return {
        "resume_score": total_score,
        "strengths": strengths,
        "gaps": gaps,
        "suggestions": suggestions,
        "recommended_difficulty": recommended_difficulty,
        "found_keywords": list(unique_keywords)
    }
