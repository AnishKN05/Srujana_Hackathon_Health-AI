import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Send, 
  MessageCircle, 
  AlertCircle, 
  Clock,
  CheckCircle,
  User,
  Bot,
  Loader
} from 'lucide-react'
import { useHealth } from '../context/HealthContext'
import { chatWithBot, analyzeSymptoms } from '../services/api'
import SymptomAnalysisResult from '../components/SymptomAnalysisResult'

const SymptomCheckerPage = () => {
  const { chatHistory, isLoading, dispatch } = useHealth()
  const [message, setMessage] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [showQuickStart, setShowQuickStart] = useState(true)
  const messagesEndRef = useRef(null)

  const quickStartOptions = [
    "I have a headache and feel tired",
    "I have a rash on my arm",
    "I'm experiencing chest pain",
    "I have a fever and sore throat",
    "I have stomach pain and nausea"
  ]

  useEffect(() => {
    scrollToBottom()
  }, [chatHistory])

  useEffect(() => {
    // Generate session ID on component mount
    setSessionId(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async (messageText = message) => {
    if (!messageText.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString()
    }

    // Add user message to chat history
    dispatch({ type: 'ADD_CHAT_MESSAGE', payload: userMessage })
    dispatch({ type: 'SET_LOADING', payload: true })
    setMessage('')
    setShowQuickStart(false)

    try {
      const response = await chatWithBot({
        user_id: sessionId,
        message: messageText,
        conversation_history: chatHistory,
        session_id: sessionId
      })

      // Add AI response to chat history
      const aiMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        suggested_questions: response.suggested_questions,
        confidence_level: response.confidence_level,
        requires_consultation: response.requires_professional_consultation
      }

      dispatch({ type: 'ADD_CHAT_MESSAGE', payload: aiMessage })

      // If the conversation seems complete, offer detailed analysis
      if (chatHistory.length >= 4) {
        setTimeout(() => {
          setShowAnalysisOption(true)
        }, 2000)
      }

    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      
      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'I apologize, but I\'m having trouble processing your message right now. Please try again or consult with a healthcare professional.',
        timestamp: new Date().toISOString(),
        isError: true
      }
      dispatch({ type: 'ADD_CHAT_MESSAGE', payload: errorMessage })
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  const handleQuickStart = (option) => {
    handleSendMessage(option)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const requestDetailedAnalysis = async () => {
    if (chatHistory.length === 0) return

    dispatch({ type: 'SET_LOADING', payload: true })

    try {
      // Extract symptoms from chat history
      const symptoms = extractSymptomsFromChat(chatHistory)
      
      const analysisRequest = {
        user_id: sessionId,
        symptoms: symptoms,
        duration: null, // Could be extracted from chat
        severity: null, // Could be extracted from chat
        additional_info: chatHistory.map(msg => msg.content).join(' ')
      }

      const result = await analyzeSymptoms(analysisRequest)
      setAnalysisResult(result)
      dispatch({ type: 'ADD_SYMPTOM_RESULT', payload: result })

    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  const extractSymptomsFromChat = (history) => {
    // Enhanced extraction with better symptom detection
    const userMessages = history.filter(msg => msg.role === 'user')
    const allText = userMessages.map(msg => msg.content).join(' ').toLowerCase()
    
    // Expanded symptom dictionary
    const symptomKeywords = {
      'headache': ['headache', 'head pain', 'head ache', 'migraine', 'head hurts'],
      'fever': ['fever', 'temperature', 'hot', 'chills', 'sweating'],
      'cough': ['cough', 'coughing', 'hacking', 'dry cough', 'wet cough'],
      'sore throat': ['sore throat', 'throat pain', 'throat hurts', 'scratchy throat'],
      'nausea': ['nausea', 'nauseous', 'queasy', 'sick to stomach'],
      'vomiting': ['vomiting', 'throwing up', 'puking', 'vomit'],
      'diarrhea': ['diarrhea', 'loose stools', 'watery stools', 'bowel issues'],
      'fatigue': ['fatigue', 'tired', 'exhausted', 'weak', 'lethargic'],
      'dizziness': ['dizzy', 'dizziness', 'lightheaded', 'vertigo'],
      'chest pain': ['chest pain', 'chest hurts', 'chest discomfort', 'heart pain'],
      'shortness of breath': ['shortness of breath', 'breathing problems', 'can\'t breathe', 'breathless'],
      'rash': ['rash', 'skin rash', 'red spots', 'skin irritation'],
      'itching': ['itching', 'itchy', 'pruritus', 'scratching'],
      'swelling': ['swelling', 'swollen', 'inflammation', 'puffy'],
      'pain': ['pain', 'hurts', 'ache', 'sore', 'tender'],
      'abdominal pain': ['stomach pain', 'belly ache', 'abdominal pain', 'cramps'],
      'back pain': ['back pain', 'back ache', 'spine pain'],
      'joint pain': ['joint pain', 'arthritis', 'stiff joints'],
      'muscle pain': ['muscle pain', 'muscle ache', 'sore muscles'],
      'runny nose': ['runny nose', 'nasal congestion', 'stuffy nose'],
      'sneezing': ['sneezing', 'sneezes', 'allergies']
    }
    
    const detectedSymptoms = []
    
    for (const [symptom, keywords] of Object.entries(symptomKeywords)) {
      if (keywords.some(keyword => allText.includes(keyword))) {
        detectedSymptoms.push(symptom)
      }
    }
    
    // If no specific symptoms found, extract general health complaints
    if (detectedSymptoms.length === 0) {
      const generalTerms = ['sick', 'unwell', 'not feeling well', 'ill', 'under the weather']
      if (generalTerms.some(term => allText.includes(term))) {
        detectedSymptoms.push('general malaise')
      }
    }
    
    return detectedSymptoms.length > 0 ? detectedSymptoms : ['general health concern']
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center">
              <MessageCircle className="w-8 h-8 text-primary-600" />
            </div>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            AI Symptom Checker
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Describe your symptoms and I'll ask follow-up questions to provide preliminary health insights and first-aid guidance.
          </p>
          
          {/* Medical Disclaimer */}
          <div className="bg-orange-100 border-l-4 border-orange-500 p-4 mt-6 max-w-2xl mx-auto">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-orange-500 mr-2" />
              <p className="text-orange-700 text-sm">
                This is for educational purposes only. For medical emergencies, call 911 immediately.
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col h-96 lg:h-[600px]">
              {/* Chat Header */}
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <Bot className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Health AI Assistant</h3>
                    <p className="text-sm text-gray-500">Ready to help with your symptoms</p>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {/* Welcome Message */}
                {chatHistory.length === 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-start space-x-3"
                  >
                    <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                      <Bot className="w-5 h-5 text-primary-600" />
                    </div>
                    <div className="chat-message chat-message-ai max-w-lg">
                      <p>Hello! I'm here to help you understand your symptoms. Please describe what you're experiencing, and I'll ask follow-up questions to provide better guidance.</p>
                    </div>
                  </motion.div>
                )}

                {/* Chat Messages */}
                {chatHistory.map((msg, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`flex items-start space-x-3 ${
                      msg.role === 'user' ? 'justify-end' : ''
                    }`}
                  >
                    {msg.role === 'assistant' && (
                      <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                        <Bot className="w-5 h-5 text-primary-600" />
                      </div>
                    )}
                    
                    <div className={`chat-message ${
                      msg.role === 'user' ? 'chat-message-user' : 'chat-message-ai'
                    } ${msg.isError ? 'bg-red-100 text-red-800' : ''}`}>
                      <p>{msg.content}</p>
                      
                      {/* Suggested Questions */}
                      {msg.suggested_questions && msg.suggested_questions.length > 0 && (
                        <div className="mt-3 space-y-2">
                          <p className="text-xs font-medium opacity-75">Suggested questions:</p>
                          {msg.suggested_questions.map((question, qIndex) => (
                            <button
                              key={qIndex}
                              onClick={() => handleSendMessage(question)}
                              className="block text-xs bg-white bg-opacity-50 hover:bg-opacity-75 px-2 py-1 rounded transition-colors text-left w-full"
                            >
                              {question}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>

                    {msg.role === 'user' && (
                      <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                        <User className="w-5 h-5 text-gray-600" />
                      </div>
                    )}
                  </motion.div>
                ))}

                {/* Loading Message */}
                {isLoading && (
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                      <Bot className="w-5 h-5 text-primary-600" />
                    </div>
                    <div className="chat-message chat-message-ai">
                      <div className="flex items-center space-x-2">
                        <Loader className="w-4 h-4 animate-spin" />
                        <span>Analyzing your symptoms...</span>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Message Input */}
              <div className="px-6 py-4 border-t border-gray-200">
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Describe your symptoms..."
                    className="flex-1 input-field"
                    disabled={isLoading}
                  />
                  <button
                    onClick={() => handleSendMessage()}
                    disabled={!message.trim() || isLoading}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Quick Start Options */}
            {showQuickStart && chatHistory.length === 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Start Options:</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {quickStartOptions.map((option, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickStart(option)}
                      className="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
                    >
                      <p className="text-sm text-gray-700">{option}</p>
                    </button>
                  ))}
                </div>
              </motion.div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Analysis Button */}
            {chatHistory.length >= 3 && !analysisResult && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="card"
              >
                <h3 className="font-semibold text-gray-900 mb-3">Ready for Analysis</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Get a detailed symptom analysis with possible conditions and first-aid advice.
                </p>
                <button
                  onClick={requestDetailedAnalysis}
                  disabled={isLoading}
                  className="w-full btn-primary disabled:opacity-50"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <Loader className="w-4 h-4 animate-spin mr-2" />
                      Analyzing...
                    </div>
                  ) : (
                    'Get Detailed Analysis'
                  )}
                </button>
              </motion.div>
            )}

            {/* Tips */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-3">Tips for Better Results</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-health-500 mt-0.5 flex-shrink-0" />
                  <span>Be specific about your symptoms</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-health-500 mt-0.5 flex-shrink-0" />
                  <span>Mention when symptoms started</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-health-500 mt-0.5 flex-shrink-0" />
                  <span>Describe severity (mild, moderate, severe)</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-4 h-4 text-health-500 mt-0.5 flex-shrink-0" />
                  <span>Include relevant medical history</span>
                </li>
              </ul>
            </div>

            {/* Emergency Warning */}
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <AlertCircle className="w-5 h-5 text-red-500" />
                <h3 className="font-semibold text-red-900">Emergency Signs</h3>
              </div>
              <p className="text-sm text-red-700 mb-2">
                Call 911 immediately if you experience:
              </p>
              <ul className="text-sm text-red-700 space-y-1">
                <li>• Chest pain or pressure</li>
                <li>• Difficulty breathing</li>
                <li>• Severe allergic reaction</li>
                <li>• Loss of consciousness</li>
                <li>• Severe bleeding</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Analysis Result */}
        {analysisResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8"
          >
            <SymptomAnalysisResult result={analysisResult} />
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default SymptomCheckerPage
