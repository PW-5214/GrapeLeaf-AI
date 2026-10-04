import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { AnalyzePage } from './pages/AnalyzePage';
import { ReportPage } from './pages/ReportPage';
import { StandardsPage } from './pages/StandardsPage';
import { AboutPage } from './pages/AboutPage';
import type { AnalysisResponse } from './types';

export const App: React.FC = () => {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(() => {
    try {
      const saved = typeof window !== 'undefined' ? sessionStorage.getItem('grapeleaf_analysis') : null;
      if (saved) return JSON.parse(saved);
    } catch {
      // sessionStorage blocked or unavailable
    }
    return null;
  });

  const [formData, setFormData] = useState<any>(() => {
    try {
      const saved = typeof window !== 'undefined' ? sessionStorage.getItem('grapeleaf_form_data') : null;
      if (saved) return JSON.parse(saved);
    } catch {
      // sessionStorage blocked or unavailable
    }
    return null;
  });

  const handleAnalysisComplete = (data: AnalysisResponse, form: any) => {
    setAnalysis(data);
    setFormData(form);
    try {
      sessionStorage.setItem('grapeleaf_analysis', JSON.stringify(data));
      sessionStorage.setItem('grapeleaf_form_data', JSON.stringify(form));
    } catch {
      // ignore storage quota/security errors
    }
  };

  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-[#FFFDF8] text-[#29232D] selection:bg-[#7B3F98]/20 selection:text-[#54245F]">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route
              path="/analyze"
              element={<AnalyzePage onAnalysisComplete={handleAnalysisComplete} />}
            />
            <Route
              path="/report"
              element={<ReportPage analysis={analysis} formData={formData} />}
            />
            <Route path="/standards" element={<StandardsPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
