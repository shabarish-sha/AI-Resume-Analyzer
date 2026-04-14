# ✨ AI Resume Analyzer

> A smart, Python-powered web app that compares your resume against any job description and instantly identifies matched skills, missing keywords, and actionable improvement suggestions.

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-blue)](https://share.streamlit.io)

---

## 🎯 What It Does

Paste a job description and upload your PDF resume — the app will:

- 📋 **Extract** all text from your resume using `PyPDF2`
- 🔍 **Identify** technical skills from a database of 50+ industry keywords
- 📊 **Calculate** a match score (%) against the job requirements
- ✅ **Highlight** skills you already have (green badges)
- ❌ **Flag** missing skills the employer expects (red badges)
- 💡 **Recommend** exactly what to add to boost your ATS ranking

---

## 🖥️ Live Demo

> 🔗 [Try it on Streamlit Cloud](https://share.streamlit.io) *(deploy your own instance using the guide below)*

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py              # Complete Streamlit application (self-contained)
├── utils.py            # Modular helper functions (optional standalone use)
├── extract.py          # Original CLI-based extraction script
├── requirements.txt    # Project dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [PyPDF2](https://pypdf2.readthedocs.io) | PDF text extraction |
| [Python `re`](https://docs.python.org/3/library/re.html) | Regex-based skill matching |

---

## ✨ Features at a Glance

- 🎨 **Modern UI** with custom CSS, gradient title, and Inter font
- 🏷️ **Color-coded badges** — green for matched, red for missing, blue for all detected
- 📈 **4-metric dashboard** — Match %, Resume skills, JD skills, Missing count
- 🔄 **Loading spinner** for smooth UX
- 💬 **Actionable recommendations** for each missing skill
- 🧹 **Clean architecture** — logic separated from UI

---

## 📦 Dependencies

```
streamlit>=1.32.0
PyPDF2>=3.0.1
```

---

## ☁️ Deploying for Free

### Streamlit Community Cloud (Easiest)
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the main file
4. Click **Deploy** 🚀

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

Built with ❤️ as a portfolio project.  
> *Feel free to star ⭐ the repo if you found it useful!*
