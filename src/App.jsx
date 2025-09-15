import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import HomePage from './pages/HomePage'
import SymptomCheckerPage from './pages/SymptomCheckerPage'
import ImageAnalysisPage from './pages/ImageAnalysisPage'
import DisclaimerPage from './pages/DisclaimerPage'
import Header from './components/Header'
import Footer from './components/Footer'
import { HealthProvider } from './context/HealthContext'

function App() {
  return (
    <HealthProvider>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Header />
        
        <motion.main 
          className="flex-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/symptom-checker" element={<SymptomCheckerPage />} />
            <Route path="/image-analysis" element={<ImageAnalysisPage />} />
            <Route path="/disclaimer" element={<DisclaimerPage />} />
          </Routes>
        </motion.main>
        
        <Footer />
      </div>
    </HealthProvider>
  )
}

export default App
