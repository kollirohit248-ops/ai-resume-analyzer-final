# AI Resume Analyzer

A web application that analyzes resumes against job descriptions and provides skill gap analysis.

## Features

- Resume analysis from PDF, DOCX, or TXT files
- Skill gap detection and recommendations
- Multiple job role templates (Backend Developer, Frontend Developer, Full Stack Developer, etc.)
- Custom job description support
- Experience level awareness (Junior, Mid, Senior)

## Deployment

### Using Docker

```bash
docker-compose up
```

### Using Render.com

1. Fork this repository
2. Create a new Web Service on Render
3. Set the build command to `cd backend && pip install -r requirements.txt`
4. Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`

## API Endpoints

- `GET /` - Root endpoint
- `GET /jobs` - Get available job titles
- `POST /analyze` - Analyze resume against standard job description
- `POST /analyze-custom` - Analyze resume against custom job description

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will proxy API requests to the backend automatically during development.
