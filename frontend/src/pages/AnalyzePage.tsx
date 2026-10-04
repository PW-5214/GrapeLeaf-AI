import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { OCTOBER_STANDARDS_CONFIG } from '../config/standards';
import { NutrientInput } from '../components/NutrientInput';
import { LoadingSpinner } from '../components/LoadingSpinner';
import type { AnalysisResponse, ModelType, ModelInfo } from '../types';
import {
  FlaskConical,
  RotateCcw,
  AlertTriangle,
  ChevronRight,
  Sparkles,
  Cpu,
  Trees,
  CheckCircle2,
  Info,
} from 'lucide-react';

interface AnalyzePageProps {
  onAnalysisComplete: (data: AnalysisResponse, formData: any) => void;
}

const MODEL_DETAILS: Record<
  ModelType,
  {
    label: string;
    shortLabel: string;
    icon: React.ReactNode;
    color: string;
    bg: string;
    ring: string;
    badge: string;
    description: string;
    pros: string[];
  }
> = {
  rf: {
    label: 'Random Forest',
    shortLabel: 'RF',
    icon: <Trees size={20} />,
    color: 'text-[#4F772D]',
    bg: 'bg-[#EAF3E2]',
    ring: 'ring-[#4F772D]',
    badge: 'bg-[#4F772D] text-white',
    description: 'Ensemble of 200 decision trees. Robust, interpretable, and industry-trusted.',
    pros: ['High interpretability', 'Handles missing values gracefully', '99.78% CV accuracy'],
  },
  xgb: {
    label: 'XGBoost',
    shortLabel: 'XGB',
    icon: <Cpu size={20} />,
    color: 'text-[#54245F]',
    bg: 'bg-[#F6F1F8]',
    ring: 'ring-[#54245F]',
    badge: 'bg-[#54245F] text-white',
    description: 'Gradient-boosted trees (300 estimators). State-of-the-art accuracy on tabular data.',
    pros: ['Highest accuracy (99.94% CV)', 'Captures complex interactions', 'Perfect test score 100%'],
  },
};

export const AnalyzePage: React.FC<AnalyzePageProps> = ({ onAnalysisComplete }) => {
  const navigate = useNavigate();

  // Metadata form state
  const [sampleId, setSampleId] = useState('');
  const [crop, setCrop] = useState('Grape');
  const [location, setLocation] = useState('');
  const [season, setSeason] = useState<'October' | 'April' | 'Other'>('October');
  const [modelType, setModelType] = useState<ModelType>('xgb');
  const [availableModels, setAvailableModels] = useState<ModelInfo[]>([]);

  // Nutrient values state (string format for input typing)
  const [nutrients, setNutrients] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    OCTOBER_STANDARDS_CONFIG.forEach((s) => { initial[s.key] = ''; });
    return initial;
  });

  const [loading, setLoading] = useState(false);
  const [generalError, setGeneralError] = useState<string | null>(null);

  // Fetch available models on mount
  useEffect(() => {
    axios.get<{ models: ModelInfo[] }>('/api/models')
      .then((r) => setAvailableModels(r.data.models))
      .catch(() => {}); // silent fail – model selector still works via hardcoded defaults
  }, []);

  const handleNutrientChange = (key: string, value: string) => {
    setNutrients((prev) => ({ ...prev, [key]: value }));
    setGeneralError(null);
  };

  const handleReset = () => {
    const cleared: Record<string, string> = {};
    OCTOBER_STANDARDS_CONFIG.forEach((s) => { cleared[s.key] = ''; });
    setNutrients(cleared);
    setSampleId('');
    setLocation('');
    setSeason('October');
    setGeneralError(null);
  };

  const handleFillSampleValues = () => {
    setSampleId('SAMPLE-NAS-2026');
    setLocation('Nashik Vineyards - Plot 4B');
    setSeason('October');
    setNutrients({
      N: '1.85', NO3: '920', NH4_N: '640', P: '0.52', K: '1.65',
      Ca: '0.88', Mg: '0.62', S: '0.19', Fe: '64', Mn: '75',
      Zn: '58', Cu: '7.8', Boron: '48', Mo: '0.38', Na: '0.32', Cl: '0.28',
    });
    setGeneralError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGeneralError(null);

    const enteredEntries = Object.entries(nutrients).filter(([_, val]) => val.trim() !== '');
    if (enteredEntries.length === 0) {
      setGeneralError('Please enter at least one nutrient value to run the analysis.');
      return;
    }

    const parsedNutrients: Record<string, number | null> = {};
    for (const s of OCTOBER_STANDARDS_CONFIG) {
      const raw = nutrients[s.key]?.trim();
      parsedNutrients[s.key] = raw && !isNaN(Number(raw)) ? parseFloat(raw) : null;
    }

    const payload = {
      sample_id: sampleId.trim() || undefined,
      crop: crop.trim() || 'Grape',
      location: location.trim() || undefined,
      season,
      model_type: modelType,
      nutrients: parsedNutrients,
    };

    setLoading(true);
    try {
      const response = await axios.post<AnalysisResponse>('/api/analyze', payload);
      onAnalysisComplete(response.data, { sample_id: sampleId, crop, location, season, model_type: modelType, nutrients });
      navigate('/report');
    } catch (err: any) {
      console.error('Analysis error:', err);
      setGeneralError(
        err.response?.data?.detail ||
          'Failed to connect to the analysis service. Please ensure the backend server is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const getModelAccuracy = (key: ModelType) => {
    const found = availableModels.find((m) => m.key === key);
    return found ? found.cv_accuracy : (key === 'xgb' ? '99.9%' : '99.8%');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header Banner */}
      <div className="bg-[#54245F] text-white rounded-3xl p-8 sm:p-10 shadow-lg relative overflow-hidden">
        <div className="max-w-3xl relative z-10 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-xs font-semibold text-[#98D65F] uppercase tracking-wider">
            <FlaskConical size={14} />
            <span>Petiole Nutrient Entry Form</span>
          </div>
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-white">
            Analyze Your Grape Leaf Sample
          </h1>
          <p className="text-sm sm:text-base text-white/80 leading-relaxed">
            Enter your petiole lab values, choose your preferred ML classification engine, and get an instant advisory report.
          </p>
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={handleFillSampleValues}
            className="px-4 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-white text-xs font-semibold border border-white/20 transition-all flex items-center gap-1.5"
          >
            <Sparkles size={14} className="text-[#98D65F]" />
            <span>Fill Realistic Example Data</span>
          </button>
        </div>
      </div>

      {/* Season Warning Banner */}
      {season !== 'October' && (
        <div className="rounded-2xl bg-amber-50 border border-amber-300 p-5 flex items-start gap-4 text-amber-900 shadow-xs animate-in fade-in duration-300">
          <AlertTriangle className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h3 className="text-sm font-bold">Season Selection Warning</h3>
            <p className="text-xs sm:text-sm text-amber-900/90 leading-relaxed">
              The current reference configuration is based on <strong>October Pruning Standards</strong> and may not be
              suitable for the selected season ({season}). Consult an agricultural professional.
            </p>
          </div>
        </div>
      )}

      {/* General Error Display */}
      {generalError && (
        <div className="rounded-2xl bg-red-50 border border-red-300 p-5 flex items-start gap-3 text-red-900 shadow-xs">
          <AlertTriangle className="w-5 h-6 text-red-600 shrink-0 mt-0.5" />
          <p className="text-sm font-medium">{generalError}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Section 1: Sample Metadata */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-xs space-y-6">
          <div className="border-b border-gray-100 pb-4">
            <h2 className="text-lg font-bold text-[#54245F]">1. Sample Identification &amp; Field Details</h2>
            <p className="text-xs text-gray-500 mt-1">Metadata printed on your advisory report for record keeping.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label htmlFor="sample_id" className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1.5">
                Sample ID <span className="text-gray-400 font-normal">(Optional)</span>
              </label>
              <input
                id="sample_id"
                type="text"
                placeholder="e.g. LAB-2026-089"
                value={sampleId}
                onChange={(e) => setSampleId(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:border-[#7B3F98] focus:ring-2 focus:ring-[#7B3F98]/20 text-sm font-medium transition-all"
              />
            </div>
            <div>
              <label htmlFor="crop" className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1.5">Crop</label>
              <input
                id="crop"
                type="text"
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:border-[#7B3F98] focus:ring-2 focus:ring-[#7B3F98]/20 text-sm font-medium transition-all bg-gray-50"
              />
            </div>
            <div>
              <label htmlFor="location" className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1.5">
                Division / Location <span className="text-gray-400 font-normal">(Optional)</span>
              </label>
              <input
                id="location"
                type="text"
                placeholder="e.g. Sangli / Nashik / Pune"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:border-[#7B3F98] focus:ring-2 focus:ring-[#7B3F98]/20 text-sm font-medium transition-all"
              />
            </div>
            <div>
              <label htmlFor="season" className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1.5">Pruning Season</label>
              <select
                id="season"
                value={season}
                onChange={(e) => setSeason(e.target.value as any)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-gray-300 focus:border-[#7B3F98] focus:ring-2 focus:ring-[#7B3F98]/20 text-sm font-semibold text-[#54245F] transition-all bg-white"
              >
                <option value="October">October (Forward Pruning) — Recommended</option>
                <option value="April">April (Foundation Pruning)</option>
                <option value="Other">Other / Off-Season</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: ML Model Selector */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-xs space-y-5">
          <div className="border-b border-gray-100 pb-4 flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-[#54245F] flex items-center gap-2">
                <Cpu size={18} className="text-[#54245F]" />
                2. Choose ML Classification Engine
              </h2>
              <p className="text-xs text-gray-500 mt-1">
                Both models are trained on 5,000 petiole records using October Pruning Reference Standards.
              </p>
            </div>
            <span className="hidden sm:flex items-center gap-1.5 text-[11px] font-semibold text-[#4F772D] bg-[#EAF3E2] px-3 py-1.5 rounded-full whitespace-nowrap">
              <CheckCircle2 size={12} />
              Models Ready
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {(['rf', 'xgb'] as ModelType[]).map((key) => {
              const m = MODEL_DETAILS[key];
              const isSelected = modelType === key;
              const cvAcc = getModelAccuracy(key);
              return (
                <button
                  key={key}
                  type="button"
                  id={`model-selector-${key}`}
                  onClick={() => setModelType(key)}
                  className={`relative text-left rounded-2xl p-5 border-2 transition-all duration-200 ${
                    isSelected
                      ? `border-current ${m.ring} ring-2 ring-offset-2 ${m.bg} shadow-md`
                      : 'border-gray-200 hover:border-gray-300 bg-gray-50 hover:bg-white'
                  }`}
                >
                  {/* Selected check */}
                  {isSelected && (
                    <span className={`absolute top-3 right-3 w-6 h-6 rounded-full ${m.badge} flex items-center justify-center`}>
                      <CheckCircle2 size={14} />
                    </span>
                  )}

                  {/* Header */}
                  <div className="flex items-center gap-2.5 mb-3">
                    <div className={`w-10 h-10 rounded-xl ${isSelected ? m.bg : 'bg-white'} border border-gray-200 flex items-center justify-center ${m.color} shadow-xs`}>
                      {m.icon}
                    </div>
                    <div>
                      <p className={`text-sm font-extrabold ${isSelected ? m.color : 'text-gray-800'}`}>{m.label}</p>
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${isSelected ? m.badge : 'bg-gray-200 text-gray-600'}`}>
                        CV: {cvAcc}
                      </span>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-xs text-gray-600 leading-relaxed mb-3">{m.description}</p>

                  {/* Pros */}
                  <ul className="space-y-1">
                    {m.pros.map((pro) => (
                      <li key={pro} className={`text-[11px] font-medium flex items-center gap-1.5 ${isSelected ? m.color : 'text-gray-500'}`}>
                        <CheckCircle2 size={11} className="shrink-0" />
                        {pro}
                      </li>
                    ))}
                  </ul>
                </button>
              );
            })}
          </div>

          <p className="text-[11px] text-gray-400 flex items-center gap-1.5">
            <Info size={12} />
            You can switch models and re-run the same sample to compare predictions.
          </p>
        </div>

        {/* Section 3: Nutrient Parameters Grid */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-xs space-y-6">
          <div className="border-b border-gray-100 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-lg font-bold text-[#54245F]">3. Enter Nutrient Values</h2>
              <p className="text-xs text-gray-500 mt-1">
                Enter measured laboratory numbers. Values are validated numerically. Leave unknown fields blank.
              </p>
            </div>
            <div className="flex items-center gap-3 text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full bg-purple-400"></span> % (Percentage)
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> ppm (mg/kg)
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {OCTOBER_STANDARDS_CONFIG.map((std) => (
              <NutrientInput
                key={std.key}
                standard={std}
                value={nutrients[std.key]}
                onChange={handleNutrientChange}
              />
            ))}
          </div>
        </div>

        {/* Section 4: Action Buttons */}
        <div className="flex flex-col-reverse sm:flex-row items-center justify-between gap-4 pt-2">
          <button
            type="button"
            onClick={handleReset}
            disabled={loading}
            className="w-full sm:w-auto px-6 py-3 rounded-xl border border-gray-300 text-gray-700 hover:bg-gray-100 font-semibold text-sm transition-all flex items-center justify-center gap-2"
          >
            <RotateCcw size={16} />
            <span>Reset All Fields</span>
          </button>

          {/* Active model pill */}
          <div className={`hidden sm:flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-full ${MODEL_DETAILS[modelType].bg} ${MODEL_DETAILS[modelType].color}`}>
            {MODEL_DETAILS[modelType].icon}
            Using: {MODEL_DETAILS[modelType].label}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[#4F772D] hover:bg-[#3f6024] text-white font-bold text-base shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2.5 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Classifying Sample...</span>
              </>
            ) : (
              <>
                <FlaskConical size={18} />
                <span>Run Nutrient Analysis</span>
                <ChevronRight size={18} />
              </>
            )}
          </button>
        </div>
      </form>

      {loading && <LoadingSpinner message={`Running ${MODEL_DETAILS[modelType].label} classification...`} />}
    </div>
  );
};
