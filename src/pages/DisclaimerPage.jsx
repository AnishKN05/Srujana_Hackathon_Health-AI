import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  ExternalLink,
  Heart,
  Loader
} from 'lucide-react'
import { getDisclaimers } from '../services/api'

const DisclaimerPage = () => {
  const [disclaimers, setDisclaimers] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchDisclaimers = async () => {
      try {
        const data = await getDisclaimers()
        setDisclaimers(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchDisclaimers()
  }, [])

  const emergencyContacts = [
    { name: 'Emergency Services', number: '911', description: 'For life-threatening emergencies' },
    { name: 'Poison Control', number: '1-800-222-1222', description: '24/7 poison emergency hotline' },
    { name: 'National Suicide Prevention', number: '988', description: 'Crisis support and suicide prevention' },
    { name: 'National Domestic Violence', number: '1-800-799-7233', description: '24/7 domestic violence hotline' }
  ]

  const importantPoints = [
    'This platform is for educational and informational purposes only',
    'AI analysis should never replace professional medical consultation',
    'Always seek advice from qualified healthcare professionals',
    'In case of medical emergency, call 911 immediately',
    'The accuracy of AI assessments cannot be guaranteed',
    'Your privacy and data security are our top priorities'
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-primary-600" />
          <p className="text-gray-600">Loading disclaimers...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-8 h-8 mx-auto mb-4 text-red-500" />
          <p className="text-red-600">Error loading disclaimers: {error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-orange-100 rounded-2xl flex items-center justify-center">
              <Shield className="w-12 h-12 text-orange-600" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Medical Disclaimers & Terms
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Important information about the use of this AI health assessment platform
          </p>
        </div>

        {/* Critical Warning */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 border-l-4 border-red-500 p-6 mb-8"
        >
          <div className="flex items-start">
            <AlertTriangle className="w-6 h-6 text-red-500 mr-3 mt-1" />
            <div>
              <h2 className="text-lg font-bold text-red-900 mb-2">
                CRITICAL MEDICAL DISCLAIMER
              </h2>
              <p className="text-red-800 font-medium">
                This AI platform is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.
              </p>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Main Disclaimers */}
          <div className="space-y-6">
            {/* Medical Disclaimer */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="card"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <Shield className="w-6 h-6 text-primary-600 mr-2" />
                Medical Disclaimer
              </h2>
              <div className="prose prose-sm max-w-none">
                <p className="text-gray-700 leading-relaxed">
                  {disclaimers?.medical_disclaimer || 'Loading...'}
                </p>
              </div>
            </motion.div>

            {/* Data Privacy */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="card"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <CheckCircle className="w-6 h-6 text-health-600 mr-2" />
                Data Privacy Notice
              </h2>
              <div className="prose prose-sm max-w-none">
                <p className="text-gray-700 leading-relaxed">
                  {disclaimers?.data_privacy || 'Loading...'}
                </p>
              </div>
            </motion.div>

            {/* Terms of Use */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="card"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <AlertTriangle className="w-6 h-6 text-warning-600 mr-2" />
                Terms of Use
              </h2>
              <div className="prose prose-sm max-w-none">
                <p className="text-gray-700 leading-relaxed">
                  {disclaimers?.terms_of_use || 'Loading...'}
                </p>
              </div>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Important Points */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="card"
            >
              <h3 className="text-lg font-bold text-gray-900 mb-4">Key Points to Remember</h3>
              <ul className="space-y-3">
                {importantPoints.map((point, index) => (
                  <li key={index} className="flex items-start space-x-3">
                    <CheckCircle className="w-5 h-5 text-health-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{point}</span>
                  </li>
                ))}
              </ul>
            </motion.div>

            {/* Emergency Contacts */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
              className="card"
            >
              <h3 className="text-lg font-bold text-gray-900 mb-4">Emergency Contacts</h3>
              <div className="space-y-4">
                {emergencyContacts.map((contact, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-semibold text-gray-900 text-sm">{contact.name}</h4>
                        <p className="text-xs text-gray-600 mt-1">{contact.description}</p>
                      </div>
                      <a
                        href={`tel:${contact.number}`}
                        className="bg-primary-600 text-white px-3 py-1 rounded text-sm font-medium hover:bg-primary-700 transition-colors"
                      >
                        {contact.number}
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* When to Seek Help */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
              className="bg-blue-50 border border-blue-200 rounded-lg p-4"
            >
              <h3 className="text-lg font-bold text-blue-900 mb-3">When to Seek Professional Help</h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li>• Symptoms worsen or persist</li>
                <li>• New symptoms develop</li>
                <li>• You have concerns about your health</li>
                <li>• You need a definitive diagnosis</li>
                <li>• You require treatment or medication</li>
                <li>• You have a chronic condition</li>
              </ul>
            </motion.div>

            {/* AI Limitations */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 }}
              className="bg-yellow-50 border border-yellow-200 rounded-lg p-4"
            >
              <h3 className="text-lg font-bold text-yellow-900 mb-3">AI Limitations</h3>
              <ul className="space-y-2 text-sm text-yellow-800">
                <li>• Cannot perform physical examinations</li>
                <li>• Cannot access medical history</li>
                <li>• Cannot provide definitive diagnoses</li>
                <li>• Cannot prescribe medications</li>
                <li>• May miss subtle or complex conditions</li>
                <li>• Accuracy depends on input quality</li>
              </ul>
            </motion.div>
          </div>
        </div>

        {/* Footer Note */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-12 text-center"
        >
          <div className="bg-gray-100 rounded-lg p-6">
            <div className="flex justify-center mb-4">
              <Heart className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Your Health Matters</h3>
            <p className="text-gray-600 max-w-2xl mx-auto">
              While this AI platform can provide helpful preliminary insights, your health and safety are our top priorities. 
              Always consult with qualified healthcare professionals for proper medical care.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default DisclaimerPage
