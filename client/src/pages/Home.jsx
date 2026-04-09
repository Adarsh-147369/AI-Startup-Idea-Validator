import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Home() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    idea_name: '',
    idea_description: ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      console.log('Submitting to /api/ideas with data:', formData)
      const response = await api.post('/ideas', formData)
      console.log('Response received:', response.data)
      navigate(`/report/${response.data.id}`)
    } catch (err) {
      console.error('Error submitting idea:', err)
      console.error('Error response:', err.response)
      console.error('Error message:', err.message)
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to analyze idea. Please try again.'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="max-w-3xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Validate Your Startup Idea with AI
          </h1>
          <p className="text-xl text-gray-600">
            Just enter your idea name and description. AI will analyze everything else!
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-4 text-sm text-gray-500">
            <span className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Problem Analysis
            </span>
            <span className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Market Research
            </span>
            <span className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Competitor Analysis
            </span>
            <span className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Tech Stack
            </span>
            <span className="flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Risk Assessment
            </span>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-2xl p-8 md:p-12">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="idea_name" className="block text-sm font-semibold text-gray-700 mb-2">
                Startup Idea Name *
              </label>
              <input
                type="text"
                id="idea_name"
                name="idea_name"
                value={formData.idea_name}
                onChange={handleChange}
                placeholder="e.g. EcoDelivery, HealthTrack, SmartHome AI"
                required
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all text-lg"
              />
            </div>

            <div>
              <label htmlFor="idea_description" className="block text-sm font-semibold text-gray-700 mb-2">
                Describe Your Idea *
              </label>
              <textarea
                id="idea_description"
                name="idea_description"
                value={formData.idea_description}
                onChange={handleChange}
                placeholder="Describe your startup idea in a few sentences. What problem does it solve? Who is it for? What makes it unique?"
                rows="6"
                required
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all text-lg resize-none"
              />
              <p className="mt-2 text-sm text-gray-500">
                💡 Tip: Be specific about the problem you're solving and your target audience
              </p>
            </div>

            {error && (
              <div className="text-red-600 text-sm p-4 bg-red-50 rounded-lg border border-red-200">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 focus:ring-4 focus:ring-indigo-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-lg"
            >
              {loading ? (
                <LoadingSpinner message="AI is analyzing your idea..." />
              ) : (
                <>
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Analyze My Idea with AI
                </>
              )}
            </button>
          </form>

          <div className="mt-8 pt-8 border-t border-gray-200">
            <p className="text-center text-sm text-gray-600">
              Our AI will automatically generate:
            </p>
            <div className="mt-4 grid grid-cols-2 md:grid-cols-3 gap-3 text-sm text-gray-700">
              <div className="flex items-center">
                <span className="text-indigo-600 mr-2">✓</span> Problem Statement
              </div>
              <div className="flex items-center">
                <span className="text-indigo-600 mr-2">✓</span> Target Customer
              </div>
              <div className="flex items-center">
                <span className="text-indigo-600 mr-2">✓</span> Market Analysis
              </div>
              <div className="flex items-center">
                <span className="text-indigo-600 mr-2">✓</span> Competitors
              </div>
              <div className="flex items-center">
                <span className="text-indigo-600 mr-2">✓</span> Tech Stack
              </div>
              <div className="flex items-center">
                <span className="text-indigo-600 mr-2">✓</span> Risk Level
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
