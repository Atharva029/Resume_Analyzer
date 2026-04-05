# Walkthrough - Smart Resume Analyzer (Mini ATS)

The **Smart Resume Analyzer** is now fully implemented with a Python Flask backend and a modern, premium frontend. It analyzes PDF resumes, extracts text, matches skills against a predefined list, calculates a score, and is ready for MySQL and AWS integration.

## Key Features Implemented

- **Resume Upload**: Drag-and-drop or file selection for PDF files.
- **Text Extraction**: Uses `pdfplumber` for robust text extraction (including multi-page).
- **Skill Detection**: Matching logic against a huge `skills.txt` file (200+ skills).
- **Scoring System**: Score = (Matched Skills × 10), capped at 100, with automated feedback.
- **Modern UI**: A premium "Deep Ocean" dark theme with glassmorphism, animations, and responsive design.
- **Database Ready**: Integrated `pymysql` support.
- **Cloud Ready**: Configured for S3 placeholders and environment-managed credentials.

---

## Core Components

### 1. Backend (`app.py`)
The backend handles the core logic:
- `extract_text()`: Opens and reads PDF content.
- `analyze_resume()`: Cleans text and matches keywords from `skills.txt`.
- `save_to_db()`: Stores results in MySQL (designed to fail gracefully if no DB is connected).

### 2. Frontend (`index.html` & `style.css`)
- **Theme**: Dark mode with gradients and blur effects.
- **Animations**: Staggered skill tag appearance and smooth section transitions.
- **Responsive**: Fully optimized for mobile and desktop.

### 3. Database Schema
Run this SQL in your MySQL environment to create the necessary table:

```sql
CREATE DATABASE IF NOT EXISTS resume_analyzer;
USE resume_analyzer;

CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    skills TEXT,
    score INT,
    word_count INT,
    timestamp DATETIME
);
```

---

## How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
Rename `.env.example` to `.env` and fill in your MySQL credentials (if available):
```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=resume_analyzer
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access the App
Open your browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Technical Details & AWS Readiness
- **Port**: Runs on `0.0.0.0:5000` (ideal for AWS EC2).
- **S3**: `upload_to_s3` placeholder function is ready for `boto3` integration.
- **Secrets**: Uses `python-dotenv` to avoid hardcoding credentials.

> [!TIP]
> To further improve accuracy, you can add more specific keywords to `skills.txt` or use NLP libraries like `spaCy` for even deeper semantic analysis.
