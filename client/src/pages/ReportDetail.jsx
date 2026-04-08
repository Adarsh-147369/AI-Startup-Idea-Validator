import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import api from '../api/axios'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ReportDetail() {
  const { id } = useParams()
  const [idea, setIdea] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchIdea()
  }, [id])

  const fetchIdea = async () => {
    try {
      const response = await api.get(`/ideas/${id}`)
      setIdea(response.data)
    } catch (err) {
      setError('Failed to load idea report')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPdf = async () => {
    try {
      const response = await api.get(`/export/${id}`, {
        responseType: 'blob',
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${idea.idea_name.replace(/\s+/g, '_')}_report.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      console.error('Failed to download PDF:', err)
      alert('Failed to download PDF')
    }
  }

  const getAiAnalysis = () => {
    if (!idea?.ai_analysis) return null
    try {
      return typeof idea.ai_analysis === 'string' 
        ? JSON.parse(idea.ai_analysis) 
        : idea.ai_analysis
    } catch (e) {
      return null
    }
  }

  const getRiskColor = (risk) => {
    if (!risk) return 'bg-gray-100 text-gray-800'
    const riskLower = risk.toLowerCase()
    if (riskLower === 'low') return 'bg-green-100 text-green-800'
    if (riskLower === 'medium') return 'bg-yellow-100 text-yellow-800'
    if (riskLower === 'high') return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-800'
  }

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoadingSpinner message="Loading report..." />
      </div>
    )
  }

  if (error || !idea) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
          <p className="text-gray-600">{error || 'Idea not found'}</p>
          <Link
            to="/dashboard"
            className="mt-4 inline-block text-indigo-600 hover:text-indigo-800"
          >
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  const aiAnalysis = getAiAnalysis()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link
          to="/dashboard"
          className="text-indigo-600 hover:text-indigo-800 mb-6 inline-flex items-center"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Dashboard
        </Link>

        {/* Header Card */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-xl p-8 mb-8 text-white">
          <h1 className="text-4xl font-bold mb-4">{idea.idea_name}</h1>
          <p className="text-lg text-indigo-100 mb-6">{idea.idea_description}</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <p className="text-sm text-indigo-100 mb-1">Profitability Score</p>
              <p className="text-4xl font-bold">{idea.profitability_score || 0}/100</p>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-lg p-4">
              <p className="text-sm text-indigo-100 mb-1">Risk Level</p>
              <p className="text-4xl font-bold">{idea.risk_level || 'Unknown'}</p>
            </div>
          </div>
        </div>

        {/* AI Generated Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Problem */}
          {idea.problem && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-start mb-4">
                <span className="text-3xl mr-3">🎯</span>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Problem</h2>
                  <p className="text-sm text-gray-500">What problem does this solve?</p>
                </div>
              </div>
              <p className="text-gray-700">{idea.problem}</p>
            </div>
          )}

          {/* Customer */}
          {idea.customer && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-start mb-4">
                <span className="text-3xl mr-3">👥</span>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Target Customer</h2>
                  <p className="text-sm text-gray-500">Who will use this?</p>
                </div>
              </div>
              <p className="text-gray-700">{idea.customer}</p>
            </div>
          )}
        </div>

        {/* Market */}
        {idea.market && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="flex items-start mb-4">
              <span className="text-3xl mr-3">📊</span>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Market Analysis</h2>
                <p className="text-sm text-gray-500">Market size and opportunity</p>
              </div>
            </div>
            <p className="text-gray-700">{idea.market}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Competitors */}
          {idea.competitors && idea.competitors.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-start mb-4">
                <span className="text-3xl mr-3">⚔️</span>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Competitors</h2>
                  <p className="text-sm text-gray-500">Who else is in this space?</p>
                </div>
              </div>
              <ul className="space-y-2">
                {idea.competitors.map((comp, index) => (
                  <li key={index} className="flex items-center text-gray-700">
                    <span className="w-2 h-2 bg-indigo-600 rounded-full mr-3"></span>
                    {comp}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Tech Stack */}
          {idea.tech_stack && idea.tech_stack.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-start mb-4">
                <span className="text-3xl mr-3">🛠️</span>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Recommended Tech Stack</h2>
                  <p className="text-sm text-gray-500">Technologies to build this</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                {idea.tech_stack.map((tech, index) => (
                  <span
                    key={index}
                    className="inline-block bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Additional AI Analysis */}
        {aiAnalysis && (
          <div className="space-y-6 mb-6">
            {aiAnalysis.strengths && aiAnalysis.strengths.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-start mb-4">
                  <span className="text-3xl mr-3">✅</span>
                  <h2 className="text-xl font-semibold text-gray-900">Strengths</h2>
                </div>
                <ul className="space-y-2">
                  {aiAnalysis.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start text-gray-700">
                      <span className="text-green-500 mr-2">•</span>
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {aiAnalysis.weaknesses && aiAnalysis.weaknesses.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-start mb-4">
                  <span className="text-3xl mr-3">⚠️</span>
                  <h2 className="text-xl font-semibold text-gray-900">Weaknesses</h2>
                </div>
                <ul className="space-y-2">
                  {aiAnalysis.weaknesses.map((weakness, index) => (
                    <li key={index} className="flex items-start text-gray-700">
                      <span className="text-yellow-500 mr-2">•</span>
                      {weakness}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {aiAnalysis.recommendations && aiAnalysis.recommendations.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-start mb-4">
                  <span className="text-3xl mr-3">💡</span>
                  <h2 className="text-xl font-semibold text-gray-900">Recommendations</h2>
                </div>
                <ul className="space-y-2">
                  {aiAnalysis.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start text-gray-700">
                      <span className="text-indigo-500 mr-2">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {aiAnalysis.overall_analysis && (
              <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl shadow-lg p-6">
                <div className="flex items-start mb-4">
                  <span className="text-3xl mr-3">📝</span>
                  <h2 className="text-xl font-semibold text-gray-900">Overall Analysis</h2>
                </div>
                <p className="text-gray-700 text-lg">{aiAnalysis.overall_analysis}</p>
              </div>
            )}
          </div>
        )}

        {/* Download PDF Button */}
        <div className="mt-8">
          <button
            onClick={handleDownloadPdf}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg flex items-center justify-center"
          >
            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download PDF Report
          </button>
        </div>
      </div>
    </div>
  )
}
