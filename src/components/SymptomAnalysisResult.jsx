import React from 'react'
import { motion } from 'framer-motion'
import { 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  TrendingUp,
  Shield,
  Heart,
  Activity,
  Info
} from 'lucide-react'

const SymptomAnalysisResult = ({ result }) => {
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'low':
        return 'severity-low'
      case 'moderate':
        return 'severity-moderate'
      case 'high':
        return 'severity-high'
      case 'critical':
        return 'severity-critical'
      default:
        return 'severity-moderate'
    }
  }

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'low':
        return <CheckCircle className="w-5 h-5" />
      case 'moderate':
        return <Clock className="w-5 h-5" />
      case 'high':
        return <AlertTriangle className="w-5 h-5" />
      case 'critical':
        return <AlertTriangle className="w-5 h-5" />
      default:
        return <Info className="w-5 h-5" />
    }
  }

  const formatConfidence = (confidence) => {
    return Math.round(confidence * 100)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Symptom Analysis Results</h2>
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-primary-600" />
            <span className="text-sm text-gray-600">
              {formatConfidence(result.confidence_score)}% confidence
            </span>
          </div>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-700">
            Analysis completed on {new Date(result.timestamp).toLocaleString()}
          </p>
        </div>
      </motion.div>

      {/* Possible Conditions */}
      {result.possible_conditions && result.possible_conditions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="w-6 h-6 text-primary-600 mr-2" />
            Possible Conditions
          </h3>
          
          <div className="space-y-4">
            {result.possible_conditions.map((condition, index) => (
              <div
                key={index}
                className={`border rounded-lg p-4 ${getSeverityColor(condition.severity)}`}
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold text-lg">{condition.condition_name}</h4>
                  <div className="flex items-center space-x-2">
                    {getSeverityIcon(condition.severity)}
                    <span className="text-sm font-medium">
                      {Math.round(condition.probability * 100)}% probability
                    </span>
                  </div>
                </div>
                
                <p className="text-sm mb-3">{condition.description}</p>
                
                {condition.symptoms_match && condition.symptoms_match.length > 0 && (
                  <div>
                    <p className="text-xs font-medium mb-1">Matching symptoms:</p>
                    <div className="flex flex-wrap gap-1">
                      {condition.symptoms_match.map((symptom, sIndex) => (
                        <span
                          key={sIndex}
                          className="bg-white bg-opacity-50 px-2 py-1 rounded text-xs"
                        >
                          {symptom}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* First Aid Advice */}
      {result.first_aid_advice && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Heart className="w-6 h-6 text-health-600 mr-2" />
            First Aid Guidance
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Immediate Actions */}
            <div>
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <CheckCircle className="w-4 h-4 text-health-500 mr-2" />
                Immediate Actions
              </h4>
              <ul className="space-y-1">
                {result.first_aid_advice.immediate_actions?.map((action, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start">
                    <span className="w-1.5 h-1.5 bg-health-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                    {action}
                  </li>
                ))}
              </ul>
            </div>

            {/* Things to Avoid */}
            <div>
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <AlertTriangle className="w-4 h-4 text-red-500 mr-2" />
                Things to Avoid
              </h4>
              <ul className="space-y-1">
                {result.first_aid_advice.do_not_do?.map((item, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start">
                    <span className="w-1.5 h-1.5 bg-red-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* When to Seek Help */}
          <div className="mt-6">
            <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
              <Shield className="w-4 h-4 text-primary-500 mr-2" />
              When to Seek Professional Help
            </h4>
            <ul className="space-y-1">
              {result.first_aid_advice.when_to_seek_help?.map((item, index) => (
                <li key={index} className="text-sm text-gray-700 flex items-start">
                  <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Emergency Signs */}
          {result.first_aid_advice.emergency_signs && result.first_aid_advice.emergency_signs.length > 0 && (
            <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
              <h4 className="font-semibold text-red-900 mb-2 flex items-center">
                <AlertTriangle className="w-4 h-4 text-red-500 mr-2" />
                Emergency Warning Signs
              </h4>
              <p className="text-sm text-red-700 mb-2">
                Call 911 immediately if you experience any of these:
              </p>
              <ul className="space-y-1">
                {result.first_aid_advice.emergency_signs.map((sign, index) => (
                  <li key={index} className="text-sm text-red-700 flex items-start">
                    <span className="w-1.5 h-1.5 bg-red-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                    {sign}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </motion.div>
      )}

      {/* Follow-up Questions */}
      {result.follow_up_questions && result.follow_up_questions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4">Suggested Follow-up Questions</h3>
          <div className="space-y-2">
            {result.follow_up_questions.map((question, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-700">{question}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Medical Disclaimer */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-orange-50 border border-orange-200 rounded-lg p-4"
      >
        <div className="flex items-start">
          <AlertTriangle className="w-5 h-5 text-orange-500 mr-3 mt-1" />
          <div>
            <h4 className="font-semibold text-orange-900 mb-2">Important Medical Disclaimer</h4>
            <p className="text-sm text-orange-800">
              {result.disclaimer || 'This analysis is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.'}
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default SymptomAnalysisResult
