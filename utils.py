"""
utils.py - Utility functions for the AI Resume Analyzer.

Contains all core logic:
- Text cleaning
- Skill extraction
- Match percentage calculation
- PDF text extraction
"""

import re
import PyPDF2


# --- Predefined Skills Vault ---
PREDEFINED_SKILLS = [
    "python", "machine learning", "data analysis", "sql", "java",
    "c++", "c#", "javascript", "react", "node.js", "docker",
    "kubernetes", "aws", "azure", "gcp", "tableau", "power bi",
    "excel", "tensorflow", "pytorch", "scikit-learn", "git",
    "agile", "scrum", "html", "css", "linux", "bash", "go",
    "rust", "ruby", "php", "swift", "kotlin", "spring boot"
]


def clean_text(text):
    """Cleans the extracted text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_skills(text, skills_list):
    """Extracts predefined skills from the text."""
    matched_skills = []
    text_lower = text.lower()
    for skill in skills_list:
        if re.search(rf'\b{re.escape(skill.lower())}\b', text_lower):
            matched_skills.append(skill)
    return matched_skills


def calculate_match_percentage(resume_skills, job_skills):
    """Calculates the match percentage."""
    if not job_skills:
        return 0.0
    resume_set = set(resume_skills)
    job_set = set(job_skills)
    matched = resume_set.intersection(job_set)
    percentage = (len(matched) / len(job_set)) * 100
    return round(percentage, 2)


def extract_text_from_pdf_stream(pdf_file):
    """Extracts text from an in-memory PDF file uploaded via Streamlit."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
        return text
    except Exception as e:
        return f"ERROR: {e}"
