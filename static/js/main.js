const resumeInput = document.getElementById('resume-input');
const dropArea = document.getElementById('drop-area');
const analyzeBtn = document.getElementById('analyze-btn');
const fileInfo = document.getElementById('file-info');

const uploadSection = document.getElementById('upload-section');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');

// --- EVENT LISTENERS ---

// File selection change
resumeInput.addEventListener('change', handleFileSelect);

// Drag & Drop
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropArea.classList.add('active');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropArea.classList.remove('active');
    }, false);
});

dropArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        resumeInput.files = files;
        handleFileSelect();
    }
}, false);

// Analyze Button click
analyzeBtn.addEventListener('click', uploadAndAnalyze);

// --- HANDLERS ---

function handleFileSelect() {
    const file = resumeInput.files[0];
    if (file) {
        if (file.type !== 'application/pdf') {
            alert('Please select a PDF file.');
            resumeInput.value = '';
            analyzeBtn.disabled = true;
            fileInfo.innerHTML = '';
            return;
        }
        
        fileInfo.innerHTML = `<strong>Selected:</strong> ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
        analyzeBtn.disabled = false;
        
        // Add a nice animation effect
        fileInfo.style.opacity = '0';
        setTimeout(() => {
            fileInfo.style.transition = 'opacity 0.5s ease';
            fileInfo.style.opacity = '1';
        }, 50);
    }
}

async function uploadAndAnalyze() {
    const file = resumeInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('resume', file);

    // Switch to Loading
    uploadSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');

    try {
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            alert(data.error || 'An error occurred during analysis.');
            resetUI();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the server. Please try again.');
        resetUI();
    }
}

function displayResults(data) {
    // Fill data
    document.getElementById('res-score').innerText = data.score;
    document.getElementById('res-feedback').innerText = data.feedback;
    document.getElementById('res-wordcount').innerText = data.word_count;
    document.getElementById('res-filename').innerText = data.filename;

    // Progress Bar
    const progressBar = document.getElementById('score-bar');
    progressBar.style.width = '0%';
    setTimeout(() => {
        progressBar.style.width = data.score + '%';
    }, 100);

    // Detected Skills
    const skillsList = document.getElementById('skills-list');
    skillsList.innerHTML = '';
    if (data.skills && data.skills.length > 0) {
        data.skills.forEach((skill, index) => {
            const span = document.createElement('span');
            span.className = 'skill-tag';
            span.innerText = skill;
            span.style.animationDelay = `${index * 0.05}s`;
            skillsList.appendChild(span);
        });
    } else {
        skillsList.innerHTML = '<p class="text-secondary">No skills found.</p>';
    }

    // Missing Skills
    const missingList = document.getElementById('missing-skills-list');
    missingList.innerHTML = '';
    if (data.missing_skills && data.missing_skills.length > 0) {
        data.missing_skills.forEach((skill, index) => {
            const span = document.createElement('span');
            span.className = 'skill-tag';
            span.innerText = skill;
            span.style.animationDelay = `${index * 0.05}s`;
            missingList.appendChild(span);
        });
    } else {
        missingList.innerHTML = '<p class="text-secondary">Great! You have all core skills.</p>';
    }

    // Update score circle color based on score
    const scoreCircle = document.querySelector('.score-circle');
    if (data.score >= 80) {
        scoreCircle.style.borderColor = 'var(--success)';
        scoreCircle.style.boxShadow = '0 0 20px rgba(16, 185, 129, 0.3)';
    } else if (data.score >= 50) {
        scoreCircle.style.borderColor = 'var(--primary)';
        scoreCircle.style.boxShadow = '0 0 20px rgba(99, 102, 241, 0.3)';
    } else {
        scoreCircle.style.borderColor = 'var(--danger)';
        scoreCircle.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.3)';
    }

    // Switch to Results
    loadingSection.classList.add('hidden');
    resultSection.classList.remove('hidden');
}

function resetUI() {
    resumeInput.value = '';
    fileInfo.innerHTML = '';
    analyzeBtn.disabled = true;
    
    resultSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
}
