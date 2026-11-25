"""
AI Resume Analyzer - Backend API
FastAPI backend for analyzing resumes and providing skill gap analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pdfplumber
import docx
import re
import json
from datetime import datetime
import os

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample job descriptions for analysis
JOB_DESCRIPTIONS = {
    "backend-developer": """Senior Backend Developer - Requirements:
- Python, Django, FastAPI, SQLAlchemy, PostgreSQL
- REST API design, GraphQL, WebSockets
- Microservices, Docker, Kubernetes
- AWS (EC2, S3, Lambda), CI/CD (GitHub Actions, Jenkins)
- Redis, Celery, RabbitMQ, Message Queues
- Testing (pytest, unittest), TDD
- Git, Linux, Agile, Scrum""",

    "frontend-developer": """Senior Frontend Developer - Requirements:
- JavaScript (ES6+), TypeScript
- React.js, Vue.js, or Angular
- HTML5, CSS3, SCSS/SASS, Tailwind CSS
- State Management (Redux, Vuex, Context API)
- Webpack, Vite, Build Tools
- Responsive Design, Cross-browser compatibility
- Testing (Jest, React Testing Library, Cypress)
- REST/GraphQL APIs, WebSocket
- Accessibility (WCAG), Performance Optimization
- Git, CI/CD, Agile""",

    "fullstack-developer": """Full Stack Developer - Requirements:
- Frontend: JavaScript, TypeScript, React/Vue/Angular, HTML/CSS
- Backend: Node.js, Python, Java, or C#
- Databases: SQL (PostgreSQL, MySQL), NoSQL (MongoDB, Redis)
- APIs: REST, GraphQL
- Cloud: AWS, Azure, GCP
- DevOps: Docker, Kubernetes, CI/CD
- Testing: Unit, Integration, E2E tests
- Version Control: Git, GitHub/GitLab
- Agile methodologies""",

    "data-scientist": """Data Scientist - Requirements:
- Python (pandas, numpy, scikit-learn, tensorflow/pytorch)
- Statistics, Machine Learning, Deep Learning
- SQL (PostgreSQL, MySQL, BigQuery)
- Data Visualization (matplotlib, seaborn, plotly, Tableau)
- Big Data (Spark, Hadoop, Kafka)
- Cloud (AWS, GCP, Azure)
- Experimentation, A/B Testing
- Jupyter Notebooks, Git
- Statistics, Probability, Linear Algebra""",

    "mobile-developer": """Mobile Developer - Requirements:
- iOS: Swift, Objective-C, SwiftUI, UIKit
- Android: Kotlin, Java, Jetpack Compose
- Cross-platform: React Native, Flutter, Xamarin
- RESTful APIs, GraphQL
- SQLite, CoreData, Room Database
- App Store, Google Play deployment
- Testing, Debugging, Performance Optimization
- Version Control (Git)
- Agile methodologies""",

    "devops-engineer": """DevOps Engineer - Requirements:
- Linux/Unix, Shell scripting, Python
- Virtualization (Docker, Vagrant, VMware)
- CI/CD (Jenkins, GitHub Actions, GitLab CI)
- Cloud: AWS, Azure, GCP
- Infrastructure as Code (Terraform, CloudFormation)
- Configuration Management (Ansible, Chef, Puppet)
- Monitoring (Prometheus, Grafana, ELK Stack)
- Kubernetes, Docker Swarm, ECS
- Networking, Security, High Availability""",

    "product-manager": """Product Manager - Requirements:
- Product strategy, Roadmapping
- Market research, Competitive analysis
- User stories, Requirements gathering
- Agile, Scrum, Kanban
- Data analysis (SQL, Excel, BI tools)
- A/B testing, Experimentation
- Stakeholder management
- Communication, Leadership
- Tools: Jira, Asana, Trello, Confluence
- UX/UI principles""",

    "machine-learning-engineer": """Machine Learning Engineer - Requirements:
- Python (numpy, pandas, scikit-learn, tensorflow, pytorch)
- ML Algorithms (supervised, unsupervised, deep learning)
- Data preprocessing, Feature engineering
- Model evaluation, Hyperparameter tuning
- MLOps (MLflow, Kubeflow, Sagemaker)
- Big Data (Spark, Hadoop)
- Cloud ML platforms (AWS SageMaker, GCP Vertex AI)
- APIs, Microservices
- Git, CI/CD for ML
- Statistics, Linear Algebra, Calculus"""
}

# General job description for analysis when no specific role is selected
GENERAL_JOB_DESCRIPTION = """General Professional Position - Requirements:
- Core technical skills relevant to the role
- Strong problem-solving abilities
- Communication and collaboration skills
- Experience with relevant tools and technologies
- Relevant certifications or education
- Project management and organizational abilities"""

# Job descriptions for the specific role
JOB_LEVEL_DESCRIPTIONS = {
    "junior": "Entry-level position - Basic understanding of core technologies, willingness to learn, ability to work under guidance",
    "mid": "Mid-level position - Proficient in core technologies, can work independently, some experience with advanced concepts",
    "senior": "Senior-level position - Expert in technologies, can lead projects, mentoring capability, deep understanding of architecture"
}

# Sample skills database
COMMON_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "C#", "Go", "Rust",
    "React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js",
    "Node.js", "Express", "Django", "Flask", "Spring Boot", "FastAPI",
    "HTML", "CSS", "Sass", "Less", "Tailwind CSS", "Bootstrap",
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitHub Actions",
    "Git", "GitHub", "GitLab", "Linux", "Windows", "MacOS",
    "REST API", "GraphQL", "WebSocket", "gRPC",
    "Microservices", "Serverless", "Monolithic",
    "Testing", "TDD", "CI/CD", "DevOps",
    "Machine Learning", "Deep Learning", "AI", "NLP", "Computer Vision",
    "Data Science", "Data Analysis", "Big Data", "Spark", "Hadoop",
    "Security", "Authentication", "Authorization", "OAuth", "JWT",
    "Agile", "Scrum", "Kanban", "Project Management", "Jira"
]


class AnalysisResult(BaseModel):
    """Response model for resume analysis"""
    job_title: str
    detected_skills: List[str]
    missing_skills: List[str]
    skill_match_percentage: float
    matched_count: int
    total_count: int
    experience_level: Optional[str] = None
    years_of_experience: Optional[int] = None
    recommendations: List[str]
    raw_data: Dict[str, Any]


class JobApplication(BaseModel):
    """Request model for job application analysis"""
    job_title: str
    job_description: Optional[str] = None
    experience_level: Optional[str] = None


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text content from PDF file"""
    from io import BytesIO
    print(f"[PDF] Starting PDF extraction, file size: {len(file_content)} bytes")
    try:
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                text += page_text
                print(f"[PDF] Extracted {len(page_text)} chars from page {i + 1}")
            print(f"[PDF] Total extracted text: {len(text)} characters")
            return text
    except Exception as e:
        print(f"[PDF] Error extracting PDF: {type(e).__name__}: {str(e)}")
        raise ValueError(f"Error parsing PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text content from DOCX file"""
    try:
        from io import BytesIO
        doc = docx.Document(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Error parsing DOCX: {str(e)}")


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text content from plain text file"""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        return file_content.decode('latin-1')


def parse_resume(text: str) -> Dict[str, Any]:
    """Parse resume text and extract structured information"""
    text = text.lower()

    # Extract skills
    detected_skills = []
    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()
        # Handle special cases for multi-word skills
        if ' ' in skill_lower:
            if skill_lower in text:
                detected_skills.append(skill)
        else:
            # Use word boundaries for single-word skills
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text):
                detected_skills.append(skill)

    # Remove duplicates while preserving order
    detected_skills = list(dict.fromkeys(detected_skills))

    # Extract years of experience
    years_match = re.search(r'(\d+)\s*(?:years?|yrs?|experience)', text)
    years_of_experience = int(years_match.group(1)) if years_match else None

    # Extract contact info
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_pattern, text)

    phone_pattern = r'\b(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'
    phones = re.findall(phone_pattern, text)

    # Extract name (usually first line)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = lines[0] if lines else ""

    return {
        "skills": detected_skills,
        "years_of_experience": years_of_experience,
        "email": emails[0] if emails else "",
        "phone": phones[0] if phones else "",
        "name": name,
        "raw_text": text
    }


def parse_job_description(jd_text: str) -> Dict[str, Any]:
    """Parse job description and extract required skills"""
    jd_text = jd_text.lower()

    # Extract skills from job description
    required_skills = []
    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()
        if ' ' in skill_lower:
            if skill_lower in jd_text:
                required_skills.append(skill)
        else:
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, jd_text):
                required_skills.append(skill)

    required_skills = list(dict.fromkeys(required_skills))

    # Extract experience level mention
    level = None
    if 'senior' in jd_text or 'expert' in jd_text:
        level = 'senior'
    elif 'junior' in jd_text or 'entry-level' in jd_text or 'intern' in jd_text:
        level = 'junior'
    elif 'mid' in jd_text or 'intermediate' in jd_text:
        level = 'mid'

    return {
        "skills": required_skills,
        "level": level
    }


def calculate_skill_match(resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
    """Calculate skill match between resume and job"""
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    matched = resume_set.intersection(job_set)
    missing = job_set - resume_set

    # Preserve original casing for matched skills
    matched_with_casing = [s for s in resume_skills if s.lower() in matched]
    missing_with_casing = [s for s in job_skills if s.lower() in missing]

    if not job_skills:
        match_percentage = 100.0
    else:
        match_percentage = (len(matched) / len(job_skills)) * 100

    return {
        "matched_skills": matched_with_casing,
        "missing_skills": missing_with_casing,
        "match_percentage": round(match_percentage, 2),
        "matched_count": len(matched),
        "total_count": len(job_skills)
    }


def generate_recommendations(
    resume_skills: List[str],
    missing_skills: List[str],
    experience_level: Optional[str] = None
) -> List[str]:
    """Generate personalized recommendations based on analysis"""
    recommendations = []

    if missing_skills:
        # Categorize missing skills
        technical = [s for s in missing_skills if s in ['Python', 'Java', 'C#', 'JavaScript', 'TypeScript',
                              'React', 'Vue.js', 'Angular', 'Django', 'Flask', 'Node.js', 'AWS',
                              'Docker', 'Kubernetes', 'SQL', 'PostgreSQL', 'MongoDB', 'Machine Learning']]
        tools = [s for s in missing_skills if s in ['Git', 'GitHub', 'GitLab', 'Jira', 'Docker',
                           'Jenkins', 'CI/CD', 'Linux', 'REST API', 'GraphQL']]
        soft = [s for s in missing_skills if s in ['Agile', 'Scrum', 'Communication', 'Leadership']]

        if technical:
            recommendations.append(f"Focus on learning: {', '.join(technical[:3])}{'...' if len(technical) > 3 else ''}")
        if tools:
            recommendations.append(f"Set up practice environment for: {', '.join(tools[:3])}")
        if soft:
            recommendations.append(f"Work on: {', '.join(soft)}")

        recommendations.append("Consider building projects to demonstrate missing skills")

    if experience_level == 'junior':
        recommendations.append("As a junior developer, focus on mastering fundamentals before advanced concepts")

    recommendations.append("Tailor your resume keywords to match job requirements exactly")

    return recommendations


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Resume Analyzer API", "version": "1.0.0"}


@app.get("/jobs")
async def get_job_titles():
    """Get available job titles for analysis"""
    return {"job_titles": list(JOB_DESCRIPTIONS.keys())}


@app.post("/analyze")
async def analyze_resume(
    job_title: str = "general-analysis",
    file: UploadFile = File(...),
    experience_level: Optional[str] = None
):
    """
    Analyze a resume against a job description

    Parameters:
    - job_title: The target job title
    - file: Resume file (PDF, DOCX, or TXT)
    - experience_level: Optional - junior, mid, or senior
    """
    print(f"[ANALYZE] Received /analyze request - job_title: {job_title}")

    # Validate job title (only validate predefined roles, allow custom/general-analysis)
    if job_title not in JOB_DESCRIPTIONS and job_title != "general-analysis":
        raise HTTPException(
            status_code=400,
            detail=f"Job title '{job_title}' not found. Available: {list(JOB_DESCRIPTIONS.keys())}"
        )

    # Read file content
    try:
        content = await file.read()
        print(f"[ANALYZE] File read successfully, {len(content)} bytes")
    except Exception as e:
        print(f"[ANALYZE] Error reading file: {e}")
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Validate file type
    file_ext = file.filename.lower().split('.')[-1] if file.filename else ''
    if file_ext not in ['pdf', 'docx', 'txt']:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, or TXT files"
        )

    # Extract text based on file type
    try:
        if file_ext == 'pdf':
            text = extract_text_from_pdf(content)
        elif file_ext == 'docx':
            text = extract_text_from_docx(content)
        else:
            text = extract_text_from_txt(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Check if text was extracted
    if not text or len(text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Could not extract meaningful text from resume. Please ensure it's a valid document."
        )

    # Parse resume and job description
    resume_data = parse_resume(text)
    # Use general description for general-analysis, otherwise use role-specific description
    if job_title == "general-analysis":
        job_description = GENERAL_JOB_DESCRIPTION
    else:
        job_description = JOB_DESCRIPTIONS[job_title]
    job_data = parse_job_description(job_description)

    # Use provided experience level or detect from resume
    exp_level = experience_level or resume_data.get('years_of_experience')

    # Calculate skill match
    match_result = calculate_skill_match(
        resume_data['skills'],
        job_data['skills']
    )

    # Generate recommendations
    recommendations = generate_recommendations(
        resume_data['skills'],
        match_result['missing_skills'],
        exp_level
    )

    # Build response
    result = AnalysisResult(
        job_title=job_title,
        detected_skills=resume_data['skills'],
        missing_skills=match_result['missing_skills'],
        skill_match_percentage=match_result['match_percentage'],
        matched_count=match_result['matched_count'],
        total_count=match_result['total_count'],
        experience_level=exp_level,
        years_of_experience=resume_data.get('years_of_experience'),
        recommendations=recommendations,
        raw_data={
            "contact": {
                "name": resume_data.get('name', ''),
                "email": resume_data.get('email', ''),
                "phone": resume_data.get('phone', '')
            },
            "job_description": job_description,
            "required_skills_count": len(job_data['skills'])
        }
    )

    return result


@app.post("/analyze-custom")
async def analyze_with_custom_jd(
    job_title: str = "general-analysis",
    job_description: str = "",
    file: UploadFile = File(...),
    experience_level: Optional[str] = None
):
    """
    Analyze a resume against a custom job description

    Parameters:
    - job_title: The target job title
    - job_description: Custom job description
    - file: Resume file (PDF, DOCX, or TXT)
    - experience_level: Optional - junior, mid, or senior
    """
    print(f"[ANALYZE-CUSTOM] Received /analyze-custom request - job_title: {job_title}")

    # Read file content
    try:
        content = await file.read()
        print(f"[ANALYZE-CUSTOM] File read successfully, {len(content)} bytes")
    except Exception as e:
        print(f"[ANALYZE-CUSTOM] Error reading file: {e}")
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Validate file type
    file_ext = file.filename.lower().split('.')[-1] if file.filename else ''
    if file_ext not in ['pdf', 'docx', 'txt']:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, or TXT files"
        )

    # Extract text based on file type
    try:
        if file_ext == 'pdf':
            text = extract_text_from_pdf(content)
        elif file_ext == 'docx':
            text = extract_text_from_docx(content)
        else:
            text = extract_text_from_txt(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Check if text was extracted
    if not text or len(text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Could not extract meaningful text from resume. Please ensure it's a valid document."
        )

    # Parse resume and custom job description
    resume_data = parse_resume(text)
    # Use general description if no job description provided
    if not job_description:
        job_description = GENERAL_JOB_DESCRIPTION
    job_data = parse_job_description(job_description)

    # Use provided experience level or detect from resume
    exp_level = experience_level or 'mid'

    # Calculate skill match
    match_result = calculate_skill_match(
        resume_data['skills'],
        job_data['skills']
    )

    # Generate recommendations
    recommendations = generate_recommendations(
        resume_data['skills'],
        match_result['missing_skills'],
        exp_level
    )

    # Build response
    result = AnalysisResult(
        job_title=job_title,
        detected_skills=resume_data['skills'],
        missing_skills=match_result['missing_skills'],
        skill_match_percentage=match_result['match_percentage'],
        matched_count=match_result['matched_count'],
        total_count=match_result['total_count'],
        experience_level=exp_level,
        years_of_experience=resume_data.get('years_of_experience'),
        recommendations=recommendations,
        raw_data={
            "contact": {
                "name": resume_data.get('name', ''),
                "email": resume_data.get('email', ''),
                "phone": resume_data.get('phone', '')
            }
        }
    )

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
