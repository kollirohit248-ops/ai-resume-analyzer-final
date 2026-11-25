import React, { useState } from 'react'
import axios from 'axios'
import { analyzeCustom } from './api.js'

const JOB_DESCRIPTIONS = {
  "backend-developer": `Senior Backend Developer - Requirements:
- Python, Django, FastAPI, SQLAlchemy, PostgreSQL
- REST API design, GraphQL, WebSockets
- Microservices, Docker, Kubernetes
- AWS (EC2, S3, Lambda), CI/CD (GitHub Actions, Jenkins)
- Redis, Celery, RabbitMQ, Message Queues
- Testing (pytest, unittest), TDD
- Git, Linux, Agile, Scrum`,

  "frontend-developer": `Senior Frontend Developer - Requirements:
- JavaScript (ES6+), TypeScript
- React.js, Vue.js, or Angular
- HTML5, CSS3, SCSS/SASS, Tailwind CSS
- State Management (Redux, Vuex, Context API)
- Webpack, Vite, Build Tools
- Responsive Design, Cross-browser compatibility
- Testing (Jest, React Testing Library, Cypress)
- REST/GraphQL APIs, WebSocket
- Accessibility (WCAG), Performance Optimization
- Git, CI/CD, Agile`,

  "fullstack-developer": `Full Stack Developer - Requirements:
- Frontend: JavaScript, TypeScript, React/Vue/Angular, HTML/CSS
- Backend: Node.js, Python, Java, or C#
- Databases: SQL (PostgreSQL, MySQL), NoSQL (MongoDB, Redis)
- APIs: REST, GraphQL
- Cloud: AWS, Azure, GCP
- DevOps: Docker, Kubernetes, CI/CD
- Testing: Unit, Integration, E2E tests
- Version Control: Git, GitHub/GitLab
- Agile methodologies`,

  "data-scientist": `Data Scientist - Requirements:
- Python (pandas, numpy, scikit-learn, tensorflow/pytorch)
- Statistics, Machine Learning, Deep Learning
- SQL (PostgreSQL, MySQL, BigQuery)
- Data Visualization (matplotlib, seaborn, plotly, Tableau)
- Big Data (Spark, Hadoop, Kafka)
- Cloud (AWS, GCP, Azure)
- Experimentation, A/B Testing
- Jupyter Notebooks, Git
- Statistics, Probability, Linear Algebra`,

  "mobile-developer": `Mobile Developer - Requirements:
- iOS: Swift, Objective-C, SwiftUI, UIKit
- Android: Kotlin, Java, Jetpack Compose
- Cross-platform: React Native, Flutter, Xamarin
- RESTful APIs, GraphQL
- SQLite, CoreData, Room Database
- App Store, Google Play deployment
- Testing, Debugging, Performance Optimization
- Version Control (Git)
- Agile methodologies`,

  "devops-engineer": `DevOps Engineer - Requirements:
- Linux/Unix, Shell scripting, Python
- Virtualization (Docker, Vagrant, VMware)
- CI/CD (Jenkins, GitHub Actions, GitLab CI)
- Cloud: AWS, Azure, GCP
- Infrastructure as Code (Terraform, CloudFormation)
- Configuration Management (Ansible, Chef, Puppet)
- Monitoring (Prometheus, Grafana, ELK Stack)
- Kubernetes, Docker Swarm, ECS
- Networking, Security, High Availability`,

  "product-manager": `Product Manager - Requirements:
- Product strategy, Roadmapping
- Market research, Competitive analysis
- User stories, Requirements gathering
- Agile, Scrum, Kanban
- Data analysis (SQL, Excel, BI tools)
- A/B testing, Experimentation
- Stakeholder management
- Communication, Leadership
- Tools: Jira, Asana, Trello, Confluence
- UX/UI principles`,

  "machine-learning-engineer": `Machine Learning Engineer - Requirements:
- Python (numpy, pandas, scikit-learn, tensorflow, pytorch)
- ML Algorithms (supervised, unsupervised, deep learning)
- Data preprocessing, Feature engineering
- Model evaluation, Hyperparameter tuning
- MLOps (MLflow, Kubeflow, Sagemaker)
- Big Data (Spark, Hadoop)
- Cloud ML platforms (AWS SageMaker, GCP Vertex AI)
- APIs, Microservices
- Git, CI/CD for ML
- Statistics, Linear Algebra, Calculus`
}

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [file, setFile] = useState(null)
  const [customJD, setCustomJD] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.size <= 10 * 1024 * 1024) {
      setFile(selectedFile)
    } else if (selectedFile) {
      alert('File size must be less than 10MB')
    }
  }

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!file) {
      alert('Please select a file')
      return
    }

    console.log('[FRONTEND] Starting analysis, file:', file.name, 'size:', file.size)
    console.log('[FRONTEND] Job title: general-analysis, Custom JD length:', customJD.length)

    setLoading(true)
    setError(null)
    setAnalysisResult(null)

    try {
      console.log('[FRONTEND] Sending request to /analyze-custom')
      const response = await analyzeCustom(file, 'general-analysis', customJD.trim())
      console.log('[FRONTEND] Response received:', response.data)
      setAnalysisResult(response.data)
    } catch (err) {
      console.error('[FRONTEND] Error:', err)
      const detail = err.response?.data?.detail
      if (Array.isArray(detail)) {
        setError(detail.map(d => d.msg || JSON.stringify(d)).join('; '))
      } else {
        setError(detail || 'Error analyzing resume')
      }
    } finally {
      setLoading(false)
      console.log('[FRONTEND] Loading set to false')
    }
  }

  const resetForm = () => {
    setFile(null)
    setCustomJD('')
    setAnalysisResult(null)
    setError(null)
    const fileInput = document.querySelector('input[type="file"]')
    if (fileInput) fileInput.value = ''
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">AI Resume Analyzer</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Analyze your resume against job requirements and identify skill gaps
          </p>
        </header>

        <div className="grid lg:grid-cols-12 gap-8">
          <div className="lg:col-span-5 space-y-6">
            <form onSubmit={handleAnalyze} className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Resume</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Resume File (PDF, DOCX, or TXT)
                  </label>
                  <div
                    onClick={() => document.querySelector('input[type="file"]').click()}
                    className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all ${
                      file ? 'border-green-300 bg-green-50' : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <input
                      type="file"
                      accept=".pdf,.docx,.txt"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                    {file ? (
                      <div className="flex flex-col items-center gap-2">
                        <span className="text-2xl">📄</span>
                        <p className="font-medium text-green-700">{file.name}</p>
                        <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center gap-2">
                        <span className="text-3xl">📁</span>
                        <p className="text-sm text-gray-600">Click to upload</p>
                        <p className="text-xs text-gray-400">PDF, DOCX, or TXT (max 10MB)</p>
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Description (optional)
                  </label>
                  <textarea
                    value={customJD}
                    onChange={(e) => setCustomJD(e.target.value)}
                    rows={5}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Paste the exact job description here. Include all required skills, technologies, and qualifications. Leave empty to use a general analysis template."
                  ></textarea>
                  <p className="text-xs text-gray-500 mt-1">
                    Leave empty for general resume analysis. Include ALL relevant skills and requirements for best results.
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={loading || !file}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                  {loading ? 'Analyzing...' : 'Analyze Resume'}
                </button>
              </div>
            </form>
          </div>

          <div className="lg:col-span-7">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">{error}</div>
            )}

            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
                <p className="mt-4 text-gray-600">Analyzing your resume...</p>
              </div>
            ) : analysisResult ? (
              <div className="space-y-6">
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-bold text-gray-800">Analysis Results</h2>
                    <div className="text-right">
                      <div className="text-sm text-gray-500">Skill Match</div>
                      <div className="text-3xl font-bold text-green-600">{analysisResult.skill_match_percentage}%</div>
                    </div>
                  </div>

                  <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                    <div
                      className="bg-green-500 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${analysisResult.skill_match_percentage}%` }}
                    ></div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-green-600">{analysisResult.matched_count}</div>
                      <div className="text-xs text-gray-500">Matched</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-gray-800">{analysisResult.total_count}</div>
                      <div className="text-xs text-gray-500">Required</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-red-600">{analysisResult.missing_skills?.length || 0}</div>
                      <div className="text-xs text-gray-500">Missing</div>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3">Detected Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {(analysisResult.detected_skills || []).map((skill, idx) => (
                      <span key={idx} className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {analysisResult.missing_skills && analysisResult.missing_skills.length > 0 && (
                  <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-red-500">
                    <h3 className="text-lg font-semibold text-gray-800 mb-3">Missing Skills</h3>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.missing_skills.map((skill, idx) => (
                        <span key={idx} className="px-3 py-1 bg-red-100 text-red-800 text-sm rounded-full">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3">Recommendations</h3>
                  <ul className="space-y-2">
                    {(analysisResult.recommendations || []).map((rec, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-blue-500 mt-1">•</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex gap-3">
                  <button onClick={resetForm} className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
                    Analyze Another
                  </button>
                  <button onClick={() => {
                    const text = `AI Resume Analysis for ${analysisResult.job_title}
Skill Match: ${analysisResult.skill_match_percentage}%
Matched: ${analysisResult.matched_count}/${analysisResult.total_count}
Skills: ${(analysisResult.detected_skills || []).join(', ')}
Missing: ${(analysisResult.missing_skills || []).join(', ')}`
                    navigator.clipboard.writeText(text).then(() => alert('Copied!'))
                  }} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                    Copy Summary
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-lg p-6 text-center text-gray-500">
                <p className="text-lg">Upload your resume to get started</p>
                <p className="text-sm mt-2">Paste a job description below for targeted analysis, or leave empty for general analysis</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
