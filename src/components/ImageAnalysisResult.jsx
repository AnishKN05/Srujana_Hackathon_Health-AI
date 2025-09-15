import React from 'react'
import { motion } from 'framer-motion'
import { 
  AlertTriangle, 
  CheckCircle, 
  Camera, 
  TrendingUp,
  Shield,
  Heart,
  Activity,
  Info,
  Eye,
  Clock
} from 'lucide-react'

const ImageAnalysisResult = ({ result }) => {
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

  const getConditionTypeLabel = (type) => {
    switch (type) {
      case 'wound':
        return 'Wound'
      case 'rash':
        return 'Rash'
      case 'skin_condition':
        return 'Skin Condition'
      case 'infection':
        return 'Infection'
      case 'allergic_reaction':
        return 'Allergic Reaction'
      default:
        return 'Other'
    }
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
          <h2 className="text-2xl font-bold text-gray-900">Image Analysis Results</h2>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Activity className="w-5 h-5 text-primary-600" />
              <span className="text-sm text-gray-600">
                {formatConfidence(result.analysis_result.confidence_score)}% confidence
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-5 h-5 text-gray-500" />
              <span className="text-sm text-gray-600">
                {result.processing_time?.toFixed(1)}s
              </span>
            </div>
          </div>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Analysis Type:</span>
              <p className="text-gray-600">{getConditionTypeLabel(result.analysis_result.condition_type)}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Severity:</span>
              <p className="text-gray-600 capitalize">{result.analysis_result.severity_assessment}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Image Quality:</span>
              <p className="text-gray-600 capitalize">{result.analysis_result.image_quality}</p>
            </div>
          </div>
          <p className="text-sm text-gray-700 mt-2">
            Analysis completed on {new Date(result.timestamp).toLocaleString()}
          </p>
        </div>
      </motion.div>

      {/* Detected Features */}
      {result.analysis_result.detected_features && result.analysis_result.detected_features.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Eye className="w-6 h-6 text-primary-600 mr-2" />
            Detected Visual Features
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {result.analysis_result.detected_features.map((feature, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-gray-900 capitalize">
                    {feature.feature_type.replace('_', ' ')}
                  </h4>
                  <span className="text-sm font-medium text-primary-600">
                    {formatConfidence(feature.confidence)}% confidence
                  </span>
                </div>
                <p className="text-sm text-gray-700">{feature.description}</p>
                {feature.location && (
                  <div className="mt-2 text-xs text-gray-500">
                    Location: {feature.location.x}, {feature.location.y} 
                    ({feature.location.width}×{feature.location.height})
                  </div>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Possible Conditions */}
      {result.analysis_result.possible_conditions && result.analysis_result.possible_conditions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="w-6 h-6 text-primary-600 mr-2" />
            Possible Conditions
          </h3>
          
          <div className="space-y-4">
            {result.analysis_result.possible_conditions.map((condition, index) => (
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
                    <p className="text-xs font-medium mb-1">Matching features:</p>
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

      {/* Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <CheckCircle className="w-6 h-6 text-health-600 mr-2" />
            Recommendations
          </h3>
          
          <ul className="space-y-2">
            {result.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start space-x-3">
                <CheckCircle className="w-4 h-4 text-health-500 mt-1 flex-shrink-0" />
                <span className="text-sm text-gray-700">{recommendation}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* First Aid Advice */}
      {result.first_aid_advice && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
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
          transition={{ delay: 0.5 }}
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
        transition={{ delay: 0.6 }}
        className="bg-orange-50 border border-orange-200 rounded-lg p-4"
      >
        <div className="flex items-start">
          <AlertTriangle className="w-5 h-5 text-orange-500 mr-3 mt-1" />
          <div>
            <h4 className="font-semibold text-orange-900 mb-2">Important Medical Disclaimer</h4>
            <p className="text-sm text-orange-800">
              {result.disclaimer || 'This image analysis is for educational purposes only and is not a substitute for professional medical diagnosis.'}
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default ImageAnalysisResult
