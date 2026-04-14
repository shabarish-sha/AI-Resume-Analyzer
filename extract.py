import PyPDF2
import re

def clean_text(text):
    """
    Cleans the extracted text by converting it to lowercase,
    removing special characters, and removing extra whitespace.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters (keep alphanumeric characters and spaces)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Replace multiple whitespaces (spaces, tabs, newlines) with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_skills(text, skills_list):
    """
    Extracts predefined skills from the text by searching for exact word matches.
    """
    matched_skills = []
    text_lower = text.lower()
    
    for skill in skills_list:
        # Use regex word boundaries (\b) to prevent partial matching 
        # (e.g., matching "java" inside "javascript")
        if re.search(rf'\b{re.escape(skill.lower())}\b', text_lower):
            matched_skills.append(skill)
            
    return matched_skills

def calculate_match_percentage(resume_skills, job_skills):
    """
    Calculates the match percentage of resume skills against job description skills.
    Returns a float representing the percentage.
    """
    if not job_skills:
        return 0.0
        
    resume_set = set(resume_skills)
    job_set = set(job_skills)
    
    # Find overlapping skills
    matched = resume_set.intersection(job_set)
    
    # Calculate percentage
    percentage = (len(matched) / len(job_set)) * 100
    return round(percentage, 2)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file using PyPDF2.
    
    Args:
        pdf_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text from the PDF.
    """
    try:
        text = ""
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get the total number of pages
            num_pages = len(pdf_reader.pages)
            print(f"Processing PDF with {num_pages} pages...")
            
            # Iterate through each page and extract text
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                # Add extracted text to the overall text string
                if page_text:
                    text += page_text + "\n\n"
                    
        return text
    except FileNotFoundError:
        return f"Error: The file at '{pdf_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Specify the path to the resume PDF
    resume_path = "sample_resume.pdf"
    
    print(f"--- Starting text extraction for {resume_path} ---")
    extracted_text = extract_text_from_pdf(resume_path)
    
    print("\n--- Cleaning Extracted Text ---")
    cleaned_text = clean_text(extracted_text)
    
    print("\n--- Cleaned Text ---")
    print(cleaned_text)
    
    print("\n--- Extracting Skills from Resume ---")
    predefined_skills = ["python", "machine learning", "data analysis", "sql", "java"]
    found_skills = extract_skills(cleaned_text, predefined_skills)
    
    print("\n--- Matched Skills (Resume) ---")
    if found_skills:
        print(", ".join(found_skills))
    else:
        print("No predefined skills found.")

    # Job description section
    print("\n\n" + "="*40)
    print("--- Processing Job Description ---")
    
    # A sample job description
    job_description = """
    We are looking for a Data Scientist who is proficient in Python and SQL. 
    Experience with Machine Learning models and strong data analysis skills are required.
    Knowledge of Java is a plus but not mandatory.
    """
    
    print("\n--- Original Job Description ---")
    print(job_description.strip())
    
    job_desc_cleaned = clean_text(job_description)
    job_desc_skills = extract_skills(job_desc_cleaned, predefined_skills)
    
    print("\n--- Matched Skills (Job Description) ---")
    if job_desc_skills:
        print(", ".join(job_desc_skills))
    else:
        print("No predefined skills found.")
        
    print("\n\n" + "="*40)
    print("--- Skill Match Analysis ---")
    match_percentage = calculate_match_percentage(found_skills, job_desc_skills)
    print(f"Match Percentage: {match_percentage}%")
