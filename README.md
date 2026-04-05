# 📄 Resume Analyzer

A powerful and efficient **Resume Analyzer** built with Python and Flask. This application extracts text from PDF resumes, identifies key technical and soft skills, calculates a matching score, and provides actionable feedback for improvement.

---

## 🔥 Features

- **PDF Text Extraction**: Uses `pdfplumber` to accurately pull text from uploaded PDF files.
- **Skill Detection**: Matches resume content against a comprehensive list of 350+ skills (defined in `skills.txt`).
- **Dynamic Scoring**: Calculates a score based on skill density, capped at a perfect 100.
- **Missing Skills Identification**: Automatically checks for "Core Industrial Skills" like Python, AWS, Docker, and SQL that might be missing.
- **Data Persistence**: Saves analysis results (filename, detected skills, score, and word count) to a **MySQL** database for historical tracking.
- **Modern UI**: A clean, responsive interface for uploading resumes and viewing detailed analysis.
- **Cloud Ready**: Includes placeholders for **AWS S3** integration for scalable file storage.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
- **Database**: MySQL
- **Libraries**:
  - `pdfplumber` (Text extraction)
  - `PyMySQL` (Database connection)
  - `boto3` (AWS S3 integration)
  - `python-dotenv` (Environment management)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- MySQL Server installed and running

### 2. Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Atharva029/Resume_Analyzer.git
   cd Resume_Analyzer
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   Create a `.env` file in the root directory and add your credentials:
   ```env
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=resume_analyzer
   FLASK_PORT=5000
   ```

### 3. Database Setup
Create the database and table in your MySQL instance:
```sql
CREATE DATABASE resume_analyzer;
USE resume_analyzer;

CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    skills TEXT,
    score INT,
    word_count INT,
    timestamp DATETIME
);
```

### 4. Running the App
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```text
Resume_Analyzer/
├── static/               # UI Assets (CSS, JS)
├── templates/            # HTML views
├── uploads/              # Temporary storage for uploaded PDFs
├── app.py                # Core Flask application logic
├── skills.txt            # Data source for skill matching
├── requirements.txt      # Project dependencies
├── .env                  # Environment secrets (Local only)
└── README.md             # Project documentation
```

---

## 🛡️ Security Note
This project uses `.env` files to manage secrets. Ensure that `.env` is listed in your `.gitignore` to avoid leaking database credentials or API keys.

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📜 License
Internal use/Open Source under MIT License.
