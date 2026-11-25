# AI Resume Analyzer

A web application that analyzes resumes against job descriptions and provides skill gap analysis.

## Features

- Resume analysis from PDF, DOCX, or TXT files
- Skill gap detection and recommendations
- Multiple job role templates (Backend Developer, Frontend Developer, Full Stack Developer, etc.)
- Custom job description support
- Experience level awareness (Junior, Mid, Senior)

## Deployment

### Live Demo
The application is deployed and available at:
- **Backend API:** `https://ai-resume-analyzer-api.onrender.com`
- **Frontend:** `https://ai-resume-analyzer.vercel.app` (or deploy the frontend to Vercel)

### GitHub Repository

```bash
# Clone the repository
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Run locally
# Terminal 1: Backend
cd ../backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd ../frontend
npm run dev
```

### Using Docker

```bash
docker-compose up
```

### Using Render.com

1. Create a new Web Service on Render
2. Set the build command to `cd backend && pip install -r requirements.txt`
3. Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `PYTHON_VERSION=3.11`

For the frontend:
1. Build the frontend locally: `npm run build` in the frontend directory
2. Deploy the `dist` folder to Render's static site service or use Vercel

### Using Vercel for Frontend

```bash
cd frontend
npm install -g vercel
vercel
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /jobs` - Get available job titles
- `POST /analyze` - Analyze resume against standard job description
- `POST /analyze-custom` - Analyze resume against custom job description

## Project Structure

```
ai-resume-analyzer/
├── backend/
│   ├── main.py          # FastAPI server
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main React component
│   │   ├── api.js       # API client with VITE_API_URL support
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── Dockerfile.backend
├── Dockerfile.frontend
├── render.yaml
└── docker-compose.yml
```

## Development

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

The frontend will proxy API requests to the backend automatically during development via Vite's proxy configuration.