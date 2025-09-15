import React, { useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { 
  Camera, 
  Upload, 
  AlertCircle, 
  CheckCircle,
  X,
  Loader,
  Image as ImageIcon,
  Info
} from 'lucide-react'
import { useHealth } from '../context/HealthContext'
import { analyzeImage } from '../services/api'
import ImageAnalysisResult from '../components/ImageAnalysisResult'

const ImageAnalysisPage = () => {
  const { isLoading, dispatch } = useHealth()
  const [uploadedFile, setUploadedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [description, setDescription] = useState('')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [uploadError, setUploadError] = useState(null)
  const sessionId = `img_session_${Date.now()}`

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setUploadError(null)
    
    if (rejectedFiles.length > 0) {
      setUploadError('Please upload a valid image file (JPG, PNG, WebP) under 5MB')
      return
    }

    const file = acceptedFiles[0]
    if (file) {
      setUploadedFile(file)
      
      // Create preview URL
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreviewUrl(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false
  })

  const handleAnalyze = async () => {
    if (!uploadedFile) {
      setUploadError('Please upload an image first')
      return
    }

    dispatch({ type: 'SET_LOADING', payload: true })
    dispatch({ type: 'CLEAR_ERROR' })

    try {
      const formData = new FormData()
      formData.append('file', uploadedFile)
      formData.append('user_id', sessionId)
      formData.append('description', description)

      const result = await analyzeImage(formData)
      setAnalysisResult(result)
      dispatch({ type: 'ADD_IMAGE_RESULT', payload: result })

    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      setUploadError(error.message)
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false })
    }
  }

  const clearImage = () => {
    setUploadedFile(null)
    setPreviewUrl(null)
    setDescription('')
    setAnalysisResult(null)
    setUploadError(null)
  }

  const imageQualityTips = [
    "Use good lighting - natural light works best",
    "Keep the camera steady to avoid blur",
    "Get close enough to show details clearly",
    "Include surrounding healthy skin for comparison",
    "Avoid shadows covering the area of interest"
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-health-100 rounded-2xl flex items-center justify-center">
              <Camera className="w-8 h-8 text-health-600" />
            </div>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            AI Image Analysis
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload a clear image of a wound, rash, or skin condition for AI-powered preliminary assessment.
          </p>
          
          {/* Medical Disclaimer */}
          <div className="bg-orange-100 border-l-4 border-orange-500 p-4 mt-6 max-w-2xl mx-auto">
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 text-orange-500 mr-2" />
              <p className="text-orange-700 text-sm">
                Image analysis is for educational purposes only. Consult healthcare professionals for actual diagnosis.
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Upload Section */}
          <div className="lg:col-span-2 space-y-6">
            {/* Image Upload */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Image</h3>
              
              {!previewUrl ? (
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                    isDragActive 
                      ? 'border-primary-400 bg-primary-50' 
                      : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                  }`}
                >
                  <input {...getInputProps()} />
                  <div className="space-y-4">
                    <div className="w-12 h-12 bg-gray-100 rounded-lg mx-auto flex items-center justify-center">
                      <Upload className="w-6 h-6 text-gray-400" />
                    </div>
                    {isDragActive ? (
                      <p className="text-primary-600 font-medium">Drop the image here...</p>
                    ) : (
                      <div>
                        <p className="text-gray-900 font-medium">
                          Drag & drop an image here, or click to select
                        </p>
                        <p className="text-gray-500 text-sm mt-1">
                          Supports JPG, PNG, WebP up to 5MB
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="relative">
                  <img
                    src={previewUrl}
                    alt="Uploaded image"
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <button
                    onClick={clearImage}
                    className="absolute top-2 right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              )}

              {uploadError && (
                <div className="mt-4 bg-red-100 border border-red-300 rounded-lg p-3">
                  <div className="flex items-center">
                    <AlertCircle className="w-4 h-4 text-red-500 mr-2" />
                    <p className="text-red-700 text-sm">{uploadError}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Description */}
            {previewUrl && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="card"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Additional Information (Optional)
                </h3>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe the condition, when it appeared, any symptoms, or other relevant details..."
                  rows={4}
                  className="w-full input-field resize-none"
                />
                <p className="text-sm text-gray-500 mt-2">
                  Additional context helps improve analysis accuracy
                </p>
              </motion.div>
            )}

            {/* Analyze Button */}
            {previewUrl && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-center"
              >
                <button
                  onClick={handleAnalyze}
                  disabled={isLoading}
                  className="btn-primary px-8 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="flex items-center">
                      <Loader className="w-5 h-5 animate-spin mr-2" />
                      Analyzing Image...
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <ImageIcon className="w-5 h-5 mr-2" />
                      Analyze Image
                    </div>
                  )}
                </button>
              </motion.div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Image Quality Tips */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Info className="w-5 h-5 mr-2 text-primary-600" />
                Image Quality Tips
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                {imageQualityTips.map((tip, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <CheckCircle className="w-4 h-4 text-health-500 mt-0.5 flex-shrink-0" />
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* What We Can Analyze */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-3">What We Can Analyze</h3>
              <div className="space-y-3">
                <div>
                  <h4 className="font-medium text-gray-900 text-sm">Skin Conditions</h4>
                  <p className="text-xs text-gray-600">Rashes, discoloration, texture changes</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 text-sm">Wounds</h4>
                  <p className="text-xs text-gray-600">Cuts, scrapes, burns, bruises</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 text-sm">Inflammatory Signs</h4>
                  <p className="text-xs text-gray-600">Redness, swelling, visible irritation</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 text-sm">Surface Features</h4>
                  <p className="text-xs text-gray-600">Bumps, lesions, unusual markings</p>
                </div>
              </div>
            </div>

            {/* Privacy Notice */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <CheckCircle className="w-5 h-5 text-blue-500" />
                <h3 className="font-semibold text-blue-900">Privacy Protected</h3>
              </div>
              <p className="text-sm text-blue-700">
                Your images are processed securely and not stored permanently. We prioritize your privacy and data security.
              </p>
            </div>

            {/* Emergency Warning */}
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <AlertCircle className="w-5 h-5 text-red-500" />
                <h3 className="font-semibold text-red-900">When to Seek Immediate Help</h3>
              </div>
              <ul className="text-sm text-red-700 space-y-1">
                <li>• Rapidly spreading infection</li>
                <li>• Severe allergic reactions</li>
                <li>• Deep or severe wounds</li>
                <li>• Signs of serious illness</li>
                <li>• Any concerning changes</li>
              </ul>
              <p className="text-xs text-red-600 mt-2 font-medium">
                Call 911 for medical emergencies
              </p>
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
            <ImageAnalysisResult result={analysisResult} />
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default ImageAnalysisPage
