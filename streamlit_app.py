# 1. Let user upload resume
# 2. Display extracted info
# 3. Call matcher and show job matches
import streamlit as st
from dotenv import load_dotenv
import os

from app.parser import extract_text
from app.extractor import extract_skills, extract_job_titles, extract_keywords
from app.matcher import search_remote_ok, search_serpapi, rank_jobs

# Load API keys from .env
load_dotenv()

# Ensure upload directory exists
os.makedirs("uploads", exist_ok=True)

st.set_page_config(page_title="JobBot.ai", layout="wide")
st.title("📄 JobBot.ai — Resume-Based Job Matcher")
st.write("Upload your resume and instantly get job matches from across the web.")

# Upload section
uploaded_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file:
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded.")

    # Extract info
    with st.spinner("Parsing resume..."):
        text = extract_text(file_path)
        skills = extract_skills(text)
        job_titles = extract_job_titles(text)
        keywords = extract_keywords(text)

    st.subheader("📋 Extracted Data")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Skills:**")
        st.code(", ".join(skills))
    with col2:
        st.write("**Job Titles:**")
        st.code(", ".join(job_titles))

    st.write("**Keywords:**")
    st.code(", ".join(keywords[:20]))

    # Search customization
    st.subheader("🔍 Job Search Filters")
    default_keywords = ", ".join(keywords[:10])
    user_keywords = st.text_input("Additional Keywords", value=default_keywords)
    location = st.text_input("Location (city or 'remote')", value="Remote")
    remote_only = st.checkbox("Remote Only", value=True)

    search_terms = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]

    # Search button
    if st.button("Search Jobs"):
        with st.spinner("Searching jobs from RemoteOK and Google Jobs..."):
            jobs_remoteok = search_remote_ok(search_terms)
            jobs_serpapi = search_serpapi(search_terms, location)
            all_jobs = jobs_remoteok + jobs_serpapi
            ranked = rank_jobs(all_jobs, job_titles, skills)

        st.subheader(f"🚀 Top {min(10, len(ranked))} Matches")
        for job in ranked[:10]:
            st.markdown(f"""
            **[{job['title']} – {job['company']}]({job['url']})**  
            _Location:_ {job.get('location', 'N/A')} | _Source:_ {job.get('via', 'RemoteOK')}  
            **Match Score**: `{job['match_score'] * 100:.0f}%`
            ---
            """)
