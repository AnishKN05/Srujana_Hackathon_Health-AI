import React from 'react'
import { Link } from 'react-router-dom'
import { Heart, Shield, AlertCircle, ExternalLink } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 gradient-health rounded-lg flex items-center justify-center">
                <Heart className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Health AI Platform</span>
            </div>
            <p className="text-sm text-gray-400">
              AI-powered preliminary health assessment with symptom analysis and image recognition.
            </p>
          </div>

          {/* Important Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Important Information</h3>
            <div className="space-y-2">
              <Link 
                to="/disclaimer" 
                className="flex items-center space-x-2 text-sm hover:text-white transition-colors"
              >
                <Shield className="w-4 h-4" />
                <span>Medical Disclaimer</span>
              </Link>
              <div className="flex items-center space-x-2 text-sm text-orange-400">
                <AlertCircle className="w-4 h-4" />
                <span>Educational Use Only</span>
              </div>
              <div className="text-xs text-gray-500 mt-2">
                This platform does not provide medical advice, diagnosis, or treatment.
              </div>
            </div>
          </div>

          {/* Emergency Resources */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Emergency Resources</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center space-x-2">
                <span className="font-medium text-red-400">Emergency Services:</span>
                <span>911 (US)</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="font-medium">Poison Control:</span>
                <span>1-800-222-1222</span>
              </div>
              <a 
                href="https://www.cdc.gov/healthyyouth/emergency/index.htm"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-1 text-primary-400 hover:text-primary-300 transition-colors"
              >
                <span>CDC Emergency Resources</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-sm text-gray-400">
              © 2024 Health AI Platform. Built for educational purposes.
            </div>
            <div className="flex items-center space-x-6 text-sm">
              <span className="text-gray-400">Powered by OpenAI & Computer Vision</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
