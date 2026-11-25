import axios from 'axios'

// Default to Render backend URL for production, VITE_API_URL can override
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://ai-resume-analyzer-api.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
})

export const getJobTitles = () => api.get('/jobs')
export const analyze = (file, jobTitle, experienceLevel) => {
  const formData = new FormData()
  formData.append('job_title', jobTitle)
  if (experienceLevel) formData.append('experience_level', experienceLevel)
  formData.append('file', file)
  return api.post('/analyze', formData)
}
export const analyzeCustom = (file, jobTitle, jobDescription, experienceLevel) => {
  const formData = new FormData()
  formData.append('job_title', jobTitle)
  formData.append('job_description', jobDescription)
  if (experienceLevel) formData.append('experience_level', experienceLevel)
  formData.append('file', file)
  return api.post('/analyze-custom', formData)
}

export default { getJobTitles, analyze, analyzeCustom }
