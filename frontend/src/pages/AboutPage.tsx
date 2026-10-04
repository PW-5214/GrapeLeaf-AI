import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  Cpu,
  Lock,
  FlaskConical,
  Sparkles,
} from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      {/* ── HEADER BANNER ── */}
      <div className="bg-[#54245F] text-white rounded-3xl p-8 sm:p-12 shadow-lg relative overflow-hidden">
        <div className="max-w-3xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-white/10 text-xs font-semibold text-[#98D65F] uppercase tracking-wider">
            <Sparkles size={14} />
            <span>Viticulture Technology & Advisory</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            About GrapeLeaf AI
          </h1>
          <p className="text-sm sm:text-base text-white/85 leading-relaxed">
            GrapeLeaf AI is a modern agricultural decision-support system built to bridge laboratory chemical analysis and practical vineyard management for grape growers.
          </p>
        </div>
      </div>

      {/* ── MISSION & APPROACH ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <div className="lg:col-span-6 space-y-5">
          <span className="text-xs font-bold uppercase tracking-wider text-[#4F772D] bg-[#EAF3E2] px-3 py-1 rounded-full">
            Our Mission
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#54245F]">
            Democratizing Precision Viticulture for Every Grower
          </h2>
          <p className="text-sm text-gray-700 leading-relaxed">
            Every season, grape farmers invest in comprehensive petiole and leaf tissue testing. However, interpreting multi-element lab sheets with disparate units (percentages and ppm) and complex ionic ratios often proves overwhelming without immediate expert guidance.
          </p>
          <p className="text-sm text-gray-700 leading-relaxed">
            GrapeLeaf AI simplifies this by instantly classifying measured laboratory values against established <strong>October Pruning Reference Standards</strong>, presenting visual indicators, non-technical explanations, and downloadable reports designed for direct farmer-agronomist collaboration.
          </p>
        </div>

        <div className="lg:col-span-6">
          <div className="rounded-3xl overflow-hidden shadow-xl border-4 border-white">
            <img
              src="/leaf_petiole.jpg"
              alt="Healthy grape leaf and petiole structure"
              className="w-full h-80 object-cover"
            />
          </div>
        </div>
      </div>

      {/* ── ARCHITECTURAL PRINCIPLES ── */}
      <div className="space-y-6">
        <div className="text-center max-w-2xl mx-auto">
          <span className="text-xs font-bold uppercase tracking-wider text-[#7B3F98] bg-[#F6F1F8] px-3 py-1 rounded-full">
            Core Philosophy
          </span>
          <h2 className="text-2xl font-extrabold text-[#54245F] mt-2">
            System Architecture & Privacy Principles
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Principle 1: Transparent Rule Engine */}
          <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-xs space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-[#EAF3E2] text-[#4F772D] flex items-center justify-center">
              <Cpu size={24} />
            </div>
            <h3 className="text-base font-bold text-[#29232D]">
              Transparent Rule-Based Classification
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              No black-box algorithms or opaque probabilistic guesswork. Every parameter is compared strictly against configured reference limits with inclusive boundary handling and safe-limit thresholds.
            </p>
          </div>

          {/* Principle 2: Data Privacy & Security */}
          <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-xs space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-[#F6F1F8] text-[#54245F] flex items-center justify-center">
              <Lock size={24} />
            </div>
            <h3 className="text-base font-bold text-[#29232D]">
              Complete Data Privacy
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Internal research datasets remain strictly isolated within private backend storage. The farmer’s submitted sample is processed only for advisory computation and PDF rendering, never logged or commingled.
            </p>
          </div>

          {/* Principle 3: Responsible Decision Support */}
          <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-xs space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-700 flex items-center justify-center">
              <ShieldCheck size={24} />
            </div>
            <h3 className="text-base font-bold text-[#29232D]">
              Responsible Decision Support
            </h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              The application provides educational orientation, not prescriptive fertilizer recipes or curative chemical claims. Growers are always directed to verify findings with accredited agricultural specialists.
            </p>
          </div>
        </div>
      </div>

      {/* ── TECH STACK BREAKDOWN ── */}
      <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-xs space-y-6">
        <h2 className="text-xl font-bold text-[#54245F]">
          Technology Stack
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 text-xs text-gray-600">
          <div className="p-4 rounded-2xl bg-gray-50 space-y-1.5 border border-gray-100">
            <span className="font-bold text-[#54245F] text-sm block">Frontend</span>
            <p>React 19 + TypeScript + Vite</p>
            <p>Tailwind CSS (Custom Grape Palette)</p>
            <p>Lucide React Icons</p>
          </div>
          <div className="p-4 rounded-2xl bg-gray-50 space-y-1.5 border border-gray-100">
            <span className="font-bold text-[#54245F] text-sm block">Backend API</span>
            <p>Python 3.11 + FastAPI</p>
            <p>Pydantic v2 Type Schemas</p>
            <p>Uvicorn ASGI Server</p>
          </div>
          <div className="p-4 rounded-2xl bg-gray-50 space-y-1.5 border border-gray-100">
            <span className="font-bold text-[#54245F] text-sm block">Document Generation</span>
            <p>ReportLab Engine</p>
            <p>3-Page Structured Layout</p>
            <p>Automated Summary Tables</p>
          </div>
          <div className="p-4 rounded-2xl bg-gray-50 space-y-1.5 border border-gray-100">
            <span className="font-bold text-[#54245F] text-sm block">Quality & Testing</span>
            <p>Pytest Unit & API Suite (41 Tests)</p>
            <p>Boundary & Zero-Safety Verifications</p>
            <p>TypeScript Static Type Checking</p>
          </div>
        </div>
      </div>

      {/* ── CALL TO ACTION ── */}
      <div className="text-center py-6">
        <Link
          to="/analyze"
          className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-[#4F772D] hover:bg-[#3f6024] text-white font-bold text-base shadow-lg transition-all"
        >
          <FlaskConical size={18} />
          <span>Analyze Your Grape Sample</span>
        </Link>
      </div>
    </div>
  );
};
