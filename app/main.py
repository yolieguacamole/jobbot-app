from app.parser import extract_text
from app.extractor import extract_skills, extract_job_titles

resume_path = 'uploads/sample_resume.pdf'  # You can update this
text = extract_text(resume_path)

skills = extract_skills(text)
titles = extract_job_titles(text)

print(f"Extracted Skills: {skills}")
print(f"Job Titles: {titles}")
