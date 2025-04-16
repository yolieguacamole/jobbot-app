import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2:
            keywords.add(token.text.lower())
    return sorted(keywords)

def extract_skills(text):
    # You can replace this with a smarter model later
    skills_list = [
        'python', 'sql', 'oracle', 'excel', 'reconciliation', 'erp',
        'lookml', 'automation', 'finance', 'data', 'reporting', 'bi', 'quickbooks'
    ]
    found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return sorted(set(found))

def extract_job_titles(text):
    # Searches for common job titles
    titles = re.findall(r'\b(?:analyst|consultant|developer|engineer|manager|specialist|architect|coordinator|director)\b', text, re.IGNORECASE)
    return sorted(set(title.capitalize() for title in titles))


