# Setup Guide for AI Resume Analyzer

## Prerequisites
- Node.js (v16+) - https://nodejs.org/
- Python (3.9+) - https://python.org/
- pip (Python package manager)
- VS Code with these extensions recommended:
  - Python
  - Pylance
  - ES6+ React Snippets
  - Tailwind CSS IntelliSense

## Quick Start (Recommended)

### Option 1: Using Docker (Easiest)
```bash
# Install Docker Desktop if not already installed
# Download from: https://www.docker.com/products/docker-desktop

# In your terminal, navigate to the project folder:
cd ai-resume-analyzer

# Start both backend and frontend
docker-compose up

# Wait for both to start:
# Backend API: http://localhost:8000
# Frontend App: http://localhost:3000
```

### Option 2: Manual Setup

## Backend Setup

### 1. Navigate to backend directory
```bash
cd ai-resume-analyzer/backend
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the backend server
```bash
uvicorn main:app --reload --port 8000
```

### 5. Verify backend is running
Open browser to: http://localhost:8000
You should see: `{"message": "AI Resume Analyzer API", "version": "1.0.0"}`

## Frontend Setup

### 1. Open VS Code and navigate to frontend folder
In VS Code terminal:
```bash
cd ../frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start the development server
```bash
npm run dev
```

### 4. Open the app
The frontend usually opens automatically at http://localhost:3000
If not, open browser to: http://localhost:3000

## Testing the Application

### Test 1: Check Available Job Titles
Open browser to: http://localhost:8000/jobs
You should see a JSON list of available job titles.

### Test 2: Upload a Test Resume
1. Create a simple text file `test_resume.txt`:
```
John Doe
Email: john@example.com
Phone: 123-456-7890

Experience: 5 years

Skills:
- Python
- Django
- PostgreSQL
- REST API
- Git
- Docker
- AWS
- Testing (pytest)
- Agile
```

2. In the web app:
   - Select "Backend Developer" role
   - Upload `test_resume.txt`
   - Click "Analyze Resume"
   - You should see the analysis results with matched and missing skills

### Test 3: Test with Custom Job Description
1. Select "Backend Developer" (or any role)
2. Click "Use custom job description instead"
3. Paste a custom job description:
```
Senior Backend Engineer - Requirements:
- Python, FastAPI, SQLAlchemy, PostgreSQL
- REST API, GraphQL
- Docker, Kubernetes, AWS
- CI/CD, GitHub Actions
- Testing, TDD
- Linux, Git, Agile
```
4. Upload your resume
5. Click "Analyze Resume"

## Troubleshooting

### Backend Issues
- **Port in use**: Change port: `uvicorn main:app --port 8001`
- **Import errors**: Make sure you installed all requirements: `pip install -r requirements.txt`
- **PDF/DOCX parsing fails**: Install system dependency:
  ```bash
  # Ubuntu/Debian:
  sudo apt-get install poppler-utils python3-dev
  ```

### Frontend Issues
- **Port in use**: Change port in vite.config.js
- **CORS errors**: Backend has CORS enabled, check the middleware code
- **API not connecting**: Check vite.config.js proxy settings

### Docker Issues
- Make sure Docker Desktop is running
- If build fails, try: `docker-compose build --no-cache`
- To rebuild: `docker-compose down && docker-compose up --build`

## Project Structure
```
ai-resume-analyzer/
├── backend/
│   ├── main.py          # FastAPI server
│   └── requirements.txt # Python packages
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main React component
│   │   ├── main.jsx     # Entry point
│   │   └── index.css    # Global styles
│   ├── index.html       # HTML template
│   ├── package.json     # NPM config
│   └── vite.config.js   # Vite config
├── Dockerfile.backend   # Backend Docker config
├── Dockerfile.frontend  # Frontend Docker config
├── docker-compose.yml   # Docker compose file
├── README.md            # Documentation
└── SETUP_GUIDE.md       # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/jobs` | GET | Get available job titles |
| `/analyze` | POST | Analyze resume against job description |
| `/analyze-custom` | POST | Analyze with custom job description |

## Sample Request
POST http://localhost:8000/analyze
Body (multipart/form-data):
- job_title: "backend-developer"
- file: (your resume file)
- experience_level: "mid" (optional)

## Deployment for Production

### Render.com
1. Push code to GitHub
2. Create 2 Web Services on Render
3. Backend: Use Dockerfile.backend
4. Frontend: Use Dockerfile.frontend, set VITE_API_URL to backend URL

### Self-Host
Follow the Docker instructions above - containers are production-ready!
