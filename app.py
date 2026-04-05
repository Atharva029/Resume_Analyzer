import os
import re
import pdfplumber
import pymysql
import boto3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sarvesh@2025")
DB_NAME = os.getenv("DB_NAME", "resume_analyzer")

# --- DATABASE LOGIC ---

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def save_to_db(filename, skills, score, word_count):
    """Saves analysis results to the MySQL database."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO resumes (filename, skills, score, word_count, timestamp) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (filename, ", ".join(skills), score, word_count, datetime.now()))
            connection.commit()
        finally:
            connection.close()

# --- AWS S3 PLACEHOLDER ---

def upload_to_s3(file_path, filename):
    """Placeholder for AWS S3 upload logic."""
    # To implement: Use boto3.client('s3') and s3.upload_file()
    print(f"[AWS S3] Placeholder: Uploading {filename} to S3 bucket...")
    pass

# --- CORE LOGIC ---

def allowed_file(filename):
    """Checks if the uploaded file is a PDF."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text(pdf_file):
    """Extracts text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

def load_skills():
    """Loads skills from skills.txt."""
    skills_list = []
    if os.path.exists('skills.txt'):
        with open('skills.txt', 'r') as f:
            skills_list = [line.strip().lower() for line in f if line.strip()]
    return list(set(skills_list))

def analyze_resume(text):
    """Cleans text, searches for skills, and calculates word count."""
    # Clean text: lowercase and remove non-alphanumeric chars (keep spaces)
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    words = cleaned_text.split()
    word_count = len(words)
    
    # Match skills
    all_known_skills = load_skills()
    detected_skills = []
    
    # Simple keyword matching
    for skill in all_known_skills:
        if skill in cleaned_text:
            detected_skills.append(skill.title())
            
    # Sort and remove duplicates
    detected_skills = sorted(list(set(detected_skills)))
    
    # Identify missing important skills (Bonus feature)
    # Let's define some 'universal' core skills that are often expected
    important_keywords = ["Python", "Java", "SQL", "Git", "AWS", "Docker", "Machine Learning", "REST API"]
    missing_skills = [s for s in important_keywords if s not in detected_skills]
    
    return detected_skills, word_count, missing_skills

def calculate_score(skills_count):
    """Calculates score based on number of skills matched."""
    # Score = (number of matched skills * 10), capped at 100
    score = skills_count * 10
    return min(score, 100)

def get_feedback(score):
    """Returns a feedback message based on the score."""
    if score >= 80:
        return "Excellent! Your resume matches many key skills."
    elif score >= 50:
        return "Good. You have a solid foundation, but there's room for more skills."
    else:
        return "Needs Improvement. Consider adding more relevant skills to your resume."

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # 1. Save file locally
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 2. Upload to S3 (Placeholder)
            upload_to_s3(file_path, filename)
            
            # 3. Extract Text
            text = extract_text(file_path)
            
            if not text.strip():
                return jsonify({'error': 'Could not extract text from PDF. Ensure it\'s not an image-only PDF.'}), 400
            
            # 4. Analyze Resume
            detected_skills, word_count, missing_skills = analyze_resume(text)
            
            # 5. Calculate Score & Get Feedback
            score = calculate_score(len(detected_skills))
            feedback = get_feedback(score)
            
            # 6. Save to Database (Placeholder for credentials)
            save_to_db(filename, detected_skills, score, word_count)
            
            return jsonify({
                'filename': filename,
                'skills': detected_skills,
                'missing_skills': missing_skills,
                'score': score,
                'word_count': word_count,
                'feedback': feedback
            })
        
        return jsonify({'error': 'Invalid file format. Only PDF allowed.'}), 400

    return render_template('index.html')

if __name__ == '__main__':
    # Cloud-ready port configuration
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host=host, port=port, debug=True)
