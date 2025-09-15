import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  MessageCircle, 
  Camera, 
  Heart, 
  Shield,
  ArrowRight,
  CheckCircle,
  AlertTriangle,
  Users,
  Clock,
  Brain
} from 'lucide-react'

const HomePage = () => {
  const features = [
    {
      icon: MessageCircle,
      title: 'Conversational Symptom Checker',
      description: 'AI-powered chatbot that asks intelligent follow-up questions about your symptoms',
      benefits: ['Personalized questions', 'Multiple condition analysis', 'First-aid guidance']
    },
    {
      icon: Camera,
      title: 'Image-Based Analysis',
      description: 'Upload photos of wounds, rashes, or skin conditions for AI-driven assessment',
      benefits: ['Computer vision analysis', 'Confidence scoring', 'Visual feature detection']
    },
    {
      icon: Shield,
      title: 'Safe & Educational',
      description: 'Clear disclaimers and guidance on when to seek professional medical help',
      benefits: ['Educational focus', 'Safety guidelines', 'Professional referrals']
    }
  ]

  const stats = [
    { label: 'AI Confidence', value: '85%', description: 'Average analysis accuracy' },
    { label: 'Response Time', value: '<30s', description: 'Typical analysis speed' },
    { label: 'Safety First', value: '100%', description: 'Medical disclaimer coverage' }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 to-health-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-20 h-20 gradient-health rounded-2xl flex items-center justify-center">
                  <Heart className="w-12 h-12 text-white" />
                </div>
              </div>
              
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                Multi-Modal AI
                <span className="block text-primary-600">Health Assessment</span>
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Get preliminary health insights through intelligent symptom analysis and advanced image recognition. 
                Designed for educational use with safety-first approach.
              </p>

              {/* Important Disclaimer */}
              <div className="bg-orange-100 border-l-4 border-orange-500 p-4 mb-8 max-w-2xl mx-auto">
                <div className="flex items-center">
                  <AlertTriangle className="w-5 h-5 text-orange-500 mr-2" />
                  <p className="text-orange-700 font-medium">
                    For Educational Purposes Only - Not a Substitute for Medical Advice
                  </p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/symptom-checker"
                  className="inline-flex items-center px-8 py-4 bg-primary-600 text-white font-semibold rounded-xl hover:bg-primary-700 transition-colors shadow-lg"
                >
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Start Symptom Check
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
                <Link
                  to="/image-analysis"
                  className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-gray-50 transition-colors shadow-lg border border-primary-200"
                >
                  <Camera className="w-5 h-5 mr-2" />
                  Analyze Image
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Two-Pronged Assessment Approach
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Combining conversational AI and computer vision for comprehensive preliminary health insights
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="card hover:shadow-lg transition-shadow"
                >
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-primary-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {feature.description}
                  </p>
                  <ul className="space-y-2">
                    {feature.benefits.map((benefit) => (
                      <li key={benefit} className="flex items-center text-sm text-gray-600">
                        <CheckCircle className="w-4 h-4 text-health-500 mr-2" />
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-4xl font-bold text-primary-600 mb-2">
                  {stat.value}
                </div>
                <div className="text-lg font-semibold text-gray-900 mb-1">
                  {stat.label}
                </div>
                <div className="text-gray-600">
                  {stat.description}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Simple, intuitive process for getting AI-powered health insights
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            {/* Symptom Checker Flow */}
            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <h3 className="text-xl font-semibold">Describe Your Symptoms</h3>
              </div>
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <h3 className="text-xl font-semibold">AI Asks Follow-up Questions</h3>
              </div>
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <h3 className="text-xl font-semibold">Receive Analysis & Guidance</h3>
              </div>
            </div>

            {/* Image Analysis Flow */}
            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-health-600 text-white rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <h3 className="text-xl font-semibold">Upload Clear Image</h3>
              </div>
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-health-600 text-white rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <h3 className="text-xl font-semibold">AI Analyzes Visual Features</h3>
              </div>
              <div className="flex items-center space-x-4">
                <div className="w-8 h-8 bg-health-600 text-white rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <h3 className="text-xl font-semibold">Get Assessment with Confidence Score</h3>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Choose your preferred assessment method and get AI-powered health insights in minutes.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/symptom-checker"
                className="inline-flex items-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-gray-100 transition-colors"
              >
                <Brain className="w-5 h-5 mr-2" />
                Try Symptom Checker
              </Link>
              <Link
                to="/image-analysis"
                className="inline-flex items-center px-8 py-4 bg-primary-700 text-white font-semibold rounded-xl hover:bg-primary-800 transition-colors border border-primary-500"
              >
                <Camera className="w-5 h-5 mr-2" />
                Analyze Image
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
