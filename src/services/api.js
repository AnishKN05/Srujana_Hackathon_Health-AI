import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for image analysis
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Response Error:', error)
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || error.response.data?.error || 'Server error occurred'
      throw new Error(message)
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check your connection.')
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred')
    }
  }
)

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    throw new Error('Health check failed: ' + error.message)
  }
}

// Symptom analysis
export const analyzeSymptoms = async (symptomData) => {
  try {
    const response = await api.post('/api/symptoms/analyze', symptomData)
    return response.data
  } catch (error) {
    throw new Error('Symptom analysis failed: ' + error.message)
  }
}

// Chat with bot
export const chatWithBot = async (chatData) => {
  try {
    const response = await api.post('/api/chat', chatData)
    return response.data
  } catch (error) {
    throw new Error('Chat failed: ' + error.message)
  }
}

// Image analysis
export const analyzeImage = async (formData) => {
  try {
    const response = await api.post('/api/image/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 seconds for image analysis
    })
    return response.data
  } catch (error) {
    throw new Error('Image analysis failed: ' + error.message)
  }
}

// Get disclaimers
export const getDisclaimers = async () => {
  try {
    const response = await api.get('/api/disclaimers')
    return response.data
  } catch (error) {
    throw new Error('Failed to fetch disclaimers: ' + error.message)
  }
}

export default api
