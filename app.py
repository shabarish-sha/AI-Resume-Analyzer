"""
AI Resume Analyzer — app.py
A complete, self-contained Streamlit app.
Run with: streamlit run app.py
"""

import re
import time
import streamlit as st
import PyPDF2


# ─────────────────────────────────────────────
# SECTION 1: CORE FUNCTIONS
# ─────────────────────────────────────────────

# Comprehensive predefined skills list
PREDEFINED_SKILLS = [
    "python", "machine learning", "data analysis", "sql", "java",
    "c++", "c#", "javascript", "react", "node.js", "docker",
    "kubernetes", "aws", "azure", "gcp", "tableau", "power bi",
    "excel", "tensorflow", "pytorch", "scikit-learn", "git",
    "agile", "scrum", "html", "css", "linux", "bash", "go",
    "rust", "ruby", "php", "swift", "kotlin", "spring boot",
    "deep learning", "nlp", "computer vision", "statistics",
    "big data", "spark", "hadoop", "mongodb", "postgresql",
    "flask", "django", "fastapi", "rest api", "microservices"
]


def clean_text(text: str) -> str:
    """Lowercase, remove special characters, collapse extra whitespace."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_text_from_pdf(pdf_file) -> str:
    """Read an uploaded PDF and return all the text it contains."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        return f"ERROR:{e}"
    return text


def extract_skills(text: str, skills_list: list) -> list:
    """Return skills from the list that appear as whole words in text."""
    found = []
    for skill in skills_list:
        pattern = rf'\b{re.escape(skill.lower())}\b'
        if re.search(pattern, text):
            found.append(skill)
    return found


def calculate_match(resume_skills: list, job_skills: list) -> tuple:
    """
    Compare resume skills against job skills.
    Returns (match_score %, matched_skills set, missing_skills set).
    """
    if not job_skills:
        return 0.0, set(), set()
    resume_set = set(resume_skills)
    job_set    = set(job_skills)
    matched    = resume_set & job_set
    missing    = job_set - resume_set
    score      = round((len(matched) / len(job_set)) * 100, 1)
    return score, matched, missing


# ─────────────────────────────────────────────
# SECTION 2: PAGE CONFIG & STYLING
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Gradient hero title */
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2e86de, #0ABFBC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        text-align: center;
        color: #888;
        font-size: 1.05rem;
        margin-bottom: 8px;
    }

    /* Skill badge styles */
    .badge-matched {
        display: inline-block;
        background: #E6F4EA;
        color: #137333;
        border: 1px solid #CEEAD6;
        border-radius: 20px;
        padding: 5px 14px;
        margin: 5px 4px;
        font-size: 13px;
        font-weight: 600;
    }
    .badge-missing {
        display: inline-block;
        background: #FCE8E6;
        color: #C5221F;
        border: 1px solid #FAD2CF;
        border-radius: 20px;
        padding: 5px 14px;
        margin: 5px 4px;
        font-size: 13px;
        font-weight: 600;
    }
    .badge-neutral {
        display: inline-block;
        background: #EEF2FF;
        color: #3730A3;
        border: 1px solid #C7D2FE;
        border-radius: 20px;
        padding: 5px 14px;
        margin: 5px 4px;
        font-size: 13px;
        font-weight: 600;
    }

    /* Card-style container */
    .skill-card {
        background: #FAFAFA;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 3: SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📌 How to Use")
    st.markdown("""
1. **Upload** your PDF resume  
2. **Paste** the job description  
3. Click **Analyze Resume**  
4. Review your **score & gaps**
""")
    st.divider()
    st.markdown("### 🎯 Skills Database")
    st.markdown(f"Tracking **{len(PREDEFINED_SKILLS)} skills** across cloud, ML, data, and dev categories.")
    st.divider()
    st.info("💡 **Tip:** Your PDF must have selectable text (not a scanned image) for best results.")


# ─────────────────────────────────────────────
# SECTION 4: HERO HEADER
# ─────────────────────────────────────────────

st.markdown("<div class='hero-title'>✨ AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Upload your resume, paste a job description, and get an instant match report.</div>", unsafe_allow_html=True)
st.divider()


# ─────────────────────────────────────────────
# SECTION 5: INPUT AREA
# ─────────────────────────────────────────────

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader(
        "Select your PDF resume",
        type=["pdf"],
        help="Only text-based PDFs are supported."
    )

with col2:
    st.subheader("💼 Job Description")
    job_desc_input = st.text_area(
        "Paste the full job description below",
        height=220,
        placeholder="e.g. We are looking for a Data Scientist with expertise in Python, SQL, and Machine Learning..."
    )

st.divider()

# ─────────────────────────────────────────────
# SECTION 6: ANALYZE BUTTON & RESULTS
# ─────────────────────────────────────────────

analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True, type="primary")

if analyze_btn:
    # ── Validation ──────────────────────────
    if not uploaded_file:
        st.warning("⚠️ Please upload a PDF resume to continue.")
        st.stop()
    if not job_desc_input.strip():
        st.warning("⚠️ Please paste a job description to continue.")
        st.stop()

    # ── Processing ──────────────────────────
    with st.spinner("🤖 Analyzing your resume..."):
        time.sleep(0.8)

        raw_text = extract_text_from_pdf(uploaded_file)

        if raw_text.startswith("ERROR:"):
            st.error(f"Could not read the PDF. {raw_text}")
            st.stop()

        if not raw_text.strip():
            st.error("The PDF appears to be empty or image-only. Please use a text-based PDF.")
            st.stop()

        # Clean & extract
        resume_clean    = clean_text(raw_text)
        jd_clean        = clean_text(job_desc_input)
        resume_skills   = extract_skills(resume_clean, PREDEFINED_SKILLS)
        jd_skills       = extract_skills(jd_clean, PREDEFINED_SKILLS)
        score, matched, missing = calculate_match(resume_skills, jd_skills)

    st.success("✅ Analysis complete!")
    st.header("📊 Results")

    # ── Row 1: Score + Skill counts ─────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎯 Match Score",    f"{score}%")
    m2.metric("📋 Resume Skills",  len(resume_skills))
    m3.metric("📌 Job Skills",     len(jd_skills))
    m4.metric("❌ Missing Skills", len(missing))

    st.progress(int(score))
    st.divider()

    # ── Row 2: Skill detail columns ─────────
    left, right = st.columns(2, gap="large")

    with left:
        st.subheader("✅ Matched Skills")
        if matched:
            badges = "".join(
                f"<span class='badge-matched'>✔ {s.title()}</span>" for s in sorted(matched)
            )
            st.markdown(f"<div class='skill-card'>{badges}</div>", unsafe_allow_html=True)
        else:
            st.warning("No skills matched the job description.")

        st.subheader("🔵 All Resume Skills Detected")
        if resume_skills:
            badges = "".join(
                f"<span class='badge-neutral'>{s.title()}</span>" for s in sorted(resume_skills)
            )
            st.markdown(f"<div class='skill-card'>{badges}</div>", unsafe_allow_html=True)
        else:
            st.info("No known skills detected in your resume.")

    with right:
        st.subheader("❌ Missing Skills")
        if missing:
            badges = "".join(
                f"<span class='badge-missing'>✗ {s.title()}</span>" for s in sorted(missing)
            )
            st.markdown(f"<div class='skill-card'>{badges}</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 Your resume covers all skills in the job description!")

        st.subheader("📋 Job Description Skills")
        if jd_skills:
            badges = "".join(
                f"<span class='badge-neutral'>{s.title()}</span>" for s in sorted(jd_skills)
            )
            st.markdown(f"<div class='skill-card'>{badges}</div>", unsafe_allow_html=True)
        else:
            st.info("No known skills detected in the job description. Try a more detailed JD.")

    # ── Row 3: Recommendations ─────────────
    st.divider()
    st.subheader("💡 Recommendations")
    if missing:
        st.warning("**To boost your ATS match score, consider adding these skills to your resume:**")
        for skill in sorted(missing):
            st.markdown(
                f"- **{skill.title()}** — Add this to your Skills section, "
                f"or weave it into your work experience with a specific example."
            )
        st.info("📌 **Pro Tip:** Don't just list skills. Show *how* you applied them to deliver measurable results.")
    else:
        st.success("🌟 Outstanding! Your resume already covers all the key skills for this role. Focus on quantifying your achievements to stand out.")
