import React, { createContext, useContext, useReducer } from 'react'

const HealthContext = createContext()

const initialState = {
  currentSession: null,
  chatHistory: [],
  imageAnalysisResults: [],
  symptomAnalysisResults: [],
  isLoading: false,
  error: null
}

const healthReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false }
    
    case 'CLEAR_ERROR':
      return { ...state, error: null }
    
    case 'ADD_CHAT_MESSAGE':
      return {
        ...state,
        chatHistory: [...state.chatHistory, action.payload]
      }
    
    case 'SET_CHAT_HISTORY':
      return {
        ...state,
        chatHistory: action.payload
      }
    
    case 'ADD_SYMPTOM_RESULT':
      return {
        ...state,
        symptomAnalysisResults: [...state.symptomAnalysisResults, action.payload]
      }
    
    case 'ADD_IMAGE_RESULT':
      return {
        ...state,
        imageAnalysisResults: [...state.imageAnalysisResults, action.payload]
      }
    
    case 'SET_CURRENT_SESSION':
      return {
        ...state,
        currentSession: action.payload
      }
    
    case 'CLEAR_SESSION':
      return {
        ...state,
        currentSession: null,
        chatHistory: [],
        error: null
      }
    
    default:
      return state
  }
}

export const HealthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(healthReducer, initialState)

  const value = {
    ...state,
    dispatch
  }

  return (
    <HealthContext.Provider value={value}>
      {children}
    </HealthContext.Provider>
  )
}

export const useHealth = () => {
  const context = useContext(HealthContext)
  if (!context) {
    throw new Error('useHealth must be used within a HealthProvider')
  }
  return context
}
