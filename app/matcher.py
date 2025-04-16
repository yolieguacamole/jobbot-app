from serpapi import GoogleSearch
import os
from difflib import SequenceMatcher

def search_remote_ok(keywords):
    import requests
    url = "https://remoteok.com/api"
    headers = {'User-Agent': 'JobBot.ai'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    jobs = response.json()[1:]  # skip metadata
    filtered = []
    for job in jobs:
        if any(skill.lower() in job['position'].lower() for skill in keywords):
            filtered.append({
                'title': job['position'],
                'company': job['company'],
                'url': job['url'],
                'tags': job.get('tags', []),
                'location': 'Remote',
                'via': 'RemoteOK'
            })
    return filtered

def search_serpapi(keywords, location="Remote"):
    query = " ".join(keywords)
    params = {
        "engine": "google_jobs",
        "q": f"{query} in {location}",
        "api_key": os.getenv("SERPAPI_KEY"),
        "hl": "en"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])
    return [{
        'title': job['title'],
        'company': job['company_name'],
        'location': job.get('location', 'N/A'),
        'url': job.get('job_id', '#'),
        'via': job.get('via', 'Google Jobs'),
        'tags': []
    } for job in jobs]

def score_match(job_title, resume_titles, resume_skills, job_tags):
    title_score = max([SequenceMatcher(None, job_title.lower(), title.lower()).ratio() for title in resume_titles], default=0)
    skill_overlap = len(set(resume_skills).intersection(set(job_tags))) / len(resume_skills) if resume_skills else 0
    return round((title_score + skill_overlap) / 2, 2)

def rank_jobs(jobs, resume_titles, resume_skills):
    ranked = []
    for job in jobs:
        score = score_match(job['title'], resume_titles, resume_skills, job.get('tags', []))
        job['match_score'] = score
        ranked.append(job)
    return sorted(ranked, key=lambda x: x['match_score'], reverse=True)
