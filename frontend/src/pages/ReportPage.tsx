import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import type { AnalysisResponse } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { SummaryCard } from '../components/SummaryCard';
import {
  FileDown,
  ArrowLeft,
  Calendar,
  MapPin,
  Tag,
  AlertTriangle,
  CheckCircle2,
  TrendingDown,
  TrendingUp,
  ShieldCheck,
  AlertCircle,
  Clock,
  FlaskConical,
  Cpu,
} from 'lucide-react';

interface ReportPageProps {
  analysis: AnalysisResponse | null;
  formData?: any;
}

export const ReportPage: React.FC<ReportPageProps> = ({ analysis }) => {
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'ALL' | 'ATTENTION' | 'OPTIMUM'>('ALL');

  if (!analysis) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-6">
        <div className="w-20 h-20 rounded-3xl bg-[#F6F1F8] flex items-center justify-center text-[#54245F] mx-auto">
          <FlaskConical size={36} />
        </div>
        <h2 className="text-2xl font-extrabold text-[#54245F]">
          No Active Sample Analysis Found
        </h2>
        <p className="text-sm text-gray-600 max-w-md mx-auto leading-relaxed">
          Please input your laboratory petiole test values on the Analyze page to view your structured results and generate a PDF advisory report.
        </p>
        <Link
          to="/analyze"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#4F772D] hover:bg-[#3f6024] text-white font-bold text-sm shadow transition-all"
        >
          <FlaskConical size={16} />
          <span>Go to Analyze Sample</span>
        </Link>
      </div>
    );
  }

  const { summary, results } = analysis;

  const filteredResults = results.filter((r) => {
    if (filter === 'ATTENTION') {
      return r.status === 'Low' || r.status === 'High' || r.status === 'Above Safe Limit';
    }
    if (filter === 'OPTIMUM') {
      return r.status === 'Optimum' || r.status === 'Safe';
    }
    return true;
  });

  const handleDownloadPDF = async () => {
    setDownloading(true);
    setDownloadError(null);
    try {
      const parsedNutrients: Record<string, number | null> = {};
      results.forEach((r) => {
        parsedNutrients[r.nutrient_key] = r.entered_value;
      });

      const payload = {
        sample_id: analysis.sample_id,
        crop: analysis.crop,
        location: analysis.location,
        season: analysis.season,
        nutrients: parsedNutrients,
      };

      const response = await axios.post('/api/report/pdf', payload, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `GrapeLeafAI_Report_${analysis.sample_id || 'sample'}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error('PDF download error:', err);
      setDownloadError('Failed to generate PDF. Please verify backend service.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* ── TOP BANNER & ACTIONS ── */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Link
              to="/analyze"
              className="text-xs text-[#54245F] hover:underline font-semibold flex items-center gap-1"
            >
              <ArrowLeft size={13} />
              <span>Back to Form</span>
            </Link>
            <span className="text-gray-300">•</span>
            <span className="text-xs font-semibold uppercase tracking-wider text-[#4F772D] bg-[#EAF3E2] px-2.5 py-0.5 rounded-full">
              Petiole Reference Benchmark
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#54245F]">
            Nutrient Analysis Results & Advisory
          </h1>

          <div className="flex flex-wrap items-center gap-y-1 gap-x-4 text-xs text-gray-600 pt-1">
            <span className="flex items-center gap-1">
              <Tag size={14} className="text-gray-400" />
              <span>Sample: <strong>{analysis.sample_id || 'Not Specified'}</strong></span>
            </span>
            <span className="flex items-center gap-1">
              <MapPin size={14} className="text-gray-400" />
              <span>Location: <strong>{analysis.location || 'Not Specified'}</strong></span>
            </span>
            <span className="flex items-center gap-1">
              <Calendar size={14} className="text-gray-400" />
              <span>Season: <strong>{analysis.season}</strong></span>
            </span>
            <span className="flex items-center gap-1">
              <Clock size={14} className="text-gray-400" />
              <span>Analyzed: <strong>{new Date(analysis.analyzed_at).toLocaleDateString()}</strong></span>
            </span>
          </div>
        </div>

        {/* Action Button */}
        <div className="w-full md:w-auto flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="px-6 py-3.5 rounded-xl bg-[#54245F] hover:bg-[#431c4c] text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {downloading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Building PDF...</span>
              </>
            ) : (
              <>
                <FileDown size={18} />
                <span>Download PDF Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      {downloadError && (
        <div className="rounded-xl bg-red-50 border border-red-300 p-4 text-xs text-red-700">
          {downloadError}
        </div>
      )}

      {/* Season Warning if applicable */}
      {analysis.season_warning && (
        <div className="rounded-2xl bg-amber-50 border border-amber-300 p-5 flex items-start gap-3 text-amber-900 shadow-xs">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <p className="text-xs sm:text-sm leading-relaxed">
            <strong>Non-Standard Season Alert:</strong> This analysis was performed with season set to <strong>{analysis.season}</strong>, but reference thresholds are calibrated for standard petiole sampling. Please verify interpretations with a local viticulturist.
          </p>
        </div>
      )}

      {/* ── MACHINE LEARNING OVERALL VINE CLASSIFICATION CARD ── */}
      {analysis.ml_prediction && (
        <div className="bg-gradient-to-r from-[#54245F] via-[#6a2b79] to-[#54245F] rounded-3xl p-6 sm:p-8 text-white shadow-lg border border-purple-300/20">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center border border-white/20">
                  <Cpu className="w-4 h-4 text-[#98D65F]" />
                </div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#98D65F]">
                  ML Overall Classification Engine
                </span>
                {/* Model-used badge */}
                <span className={`inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${
                  (analysis.ml_prediction as any).model_key === 'xgb'
                    ? 'bg-[#98D65F]/20 text-[#98D65F] border-[#98D65F]/40'
                    : 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30'
                }`}>
                  <Cpu size={10} />
                  {analysis.ml_prediction.model_name}
                </span>
              </div>

              <h2 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-3">
                <span>{analysis.ml_prediction.predicted_class}</span>
              </h2>

              <p className="text-xs sm:text-sm text-white/80 max-w-2xl leading-relaxed">
                Trained on 5,000 petiole laboratory records to synthesize multi-element interactions into an overall vine nutritional health category.
              </p>
            </div>

            {/* Confidence metric */}
            <div className="bg-white/10 backdrop-blur-xs rounded-2xl p-4 sm:p-5 border border-white/15 text-center min-w-[180px]">
              <span className="text-xs font-semibold uppercase tracking-wider text-white/70 block mb-1">
                Model Confidence
              </span>
              <div className="text-3xl font-black text-[#98D65F]">
                {(analysis.ml_prediction.confidence_score * 100).toFixed(1)}%
              </div>
              <span className="text-[11px] text-white/60 block mt-1">
                {analysis.ml_prediction.model_name}
              </span>
            </div>
          </div>

          {/* Probability distribution breakdown */}
          <div className="mt-6 pt-5 border-t border-white/15">
            <p className="text-xs font-semibold uppercase tracking-wider text-white/70 mb-3">
              Class Probability Distribution
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {Object.entries(analysis.ml_prediction.class_probabilities).map(([className, prob]) => {
                const isSelected = className === analysis.ml_prediction?.predicted_class;
                return (
                  <div
                    key={className}
                    className={`rounded-xl p-3 border transition-all ${
                      isSelected
                        ? 'bg-white/20 border-[#98D65F] shadow-sm'
                        : 'bg-white/5 border-white/10'
                    }`}
                  >
                    <div className="flex justify-between items-center text-xs mb-1">
                      <span className={`font-semibold ${isSelected ? 'text-white' : 'text-white/70'}`}>
                        {className}
                      </span>
                      <span className="font-mono font-bold text-[#98D65F]">
                        {(prob * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-white/20 overflow-hidden">
                      <div
                        className="h-full bg-[#98D65F] rounded-full transition-all duration-500"
                        style={{ width: `${Math.max(prob * 100, 2)}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ── SUMMARY CARDS GRID ── */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-[#54245F]">Summary of Parameters</h2>
          <span className="text-xs text-gray-500">
            Total Valid Measurements: {summary.total_analyzed} of 16
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
          <SummaryCard
            title="Total Analyzed"
            count={summary.total_analyzed}
            icon={FlaskConical}
            variant="default"
            subtitle="/16"
          />
          <SummaryCard
            title="Optimum"
            count={summary.optimum}
            icon={CheckCircle2}
            variant="optimum"
          />
          <SummaryCard
            title="Safe Limit"
            count={summary.safe}
            icon={ShieldCheck}
            variant="safe"
            subtitle="Na/Cl"
          />
          <SummaryCard
            title="Low"
            count={summary.low}
            icon={TrendingDown}
            variant="low"
          />
          <SummaryCard
            title="High"
            count={summary.high}
            icon={TrendingUp}
            variant="high"
          />
          <SummaryCard
            title="Above Safe"
            count={summary.above_safe_limit}
            icon={AlertTriangle}
            variant="alert"
          />
        </div>

        {/* Prominent Attention Callout */}
        {summary.attention_required > 0 ? (
          <div className="mt-4 p-4 rounded-2xl bg-[#F6F1F8] border border-[#7B3F98]/20 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#54245F] text-white flex items-center justify-center">
                <AlertCircle size={20} />
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#54245F]">
                  {summary.attention_required} Parameter{summary.attention_required > 1 ? 's' : ''} Requiring Agronomic Attention
                </h4>
                <p className="text-xs text-gray-600">
                  Values falling outside optimum bounds or exceeding safe ionic limits should be verified before making soil or foliar amendments.
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="mt-4 p-4 rounded-2xl bg-[#EAF3E2] border border-[#4F772D]/20 flex items-center gap-3 text-[#385620]">
            <CheckCircle2 size={22} className="text-[#4F772D] shrink-0" />
            <p className="text-xs sm:text-sm font-medium">
              All measured nutrients fall within the configured reference ranges and safe thresholds.
            </p>
          </div>
        )}
      </div>

      {/* ── DETAILED RESULTS TABLE ── */}
      <div className="bg-white rounded-3xl border border-gray-200 shadow-xs overflow-hidden">
        {/* Table Controls */}
        <div className="p-6 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-lg font-bold text-[#54245F]">
              Comprehensive Nutrient Breakdown
            </h3>
            <p className="text-xs text-gray-500 mt-0.5">
              Exact measured laboratory values compared to Petiole Reference Standards.
            </p>
          </div>

          <div className="flex items-center gap-1.5 bg-gray-100 p-1 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setFilter('ALL')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                filter === 'ALL'
                  ? 'bg-white text-[#54245F] shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              All ({results.length})
            </button>
            <button
              onClick={() => setFilter('ATTENTION')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                filter === 'ATTENTION'
                  ? 'bg-white text-red-700 shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Needs Attention ({summary.attention_required})
            </button>
            <button
              onClick={() => setFilter('OPTIMUM')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                filter === 'OPTIMUM'
                  ? 'bg-white text-[#4F772D] shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Optimum / Safe ({summary.optimum + summary.safe})
            </button>
          </div>
        </div>

        {/* Table Content */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#F6F1F8]/80 text-[#54245F] text-xs uppercase font-bold tracking-wider border-b border-gray-200">
              <tr>
                <th className="py-3.5 px-6">Nutrient</th>
                <th className="py-3.5 px-4">Measured Value</th>
                <th className="py-3.5 px-3">Unit</th>
                <th className="py-3.5 px-4">Reference Range</th>
                <th className="py-3.5 px-4">Status</th>
                <th className="py-3.5 px-6">Explanation & Guidance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredResults.map((item) => {
                return (
                  <tr
                    key={item.nutrient_key}
                    className="hover:bg-gray-50/70 transition-colors"
                  >
                    <td className="py-4 px-6 font-bold text-[#29232D]">
                      {item.display_name}
                    </td>
                    <td className="py-4 px-4 font-mono font-bold text-base text-[#54245F]">
                      {item.entered_value !== null ? item.entered_value : '—'}
                    </td>
                    <td className="py-4 px-3 text-xs text-gray-500 font-mono">
                      {item.unit}
                    </td>
                    <td className="py-4 px-4 text-xs font-semibold text-gray-700">
                      {item.reference_range}
                    </td>
                    <td className="py-4 px-4">
                      <StatusBadge status={item.status} size="sm" />
                    </td>
                    <td className="py-4 px-6 text-xs text-gray-600 max-w-xs leading-relaxed">
                      <p className="font-medium text-[#29232D]">{item.explanation}</p>
                      <p className="text-gray-500 mt-1 italic text-[11px]">
                        Guidance: {item.recommendation}
                      </p>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* ── EDUCATIONAL GUIDANCE PANELS ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Panel 1: Recommended Next Steps */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-[#54245F] flex items-center gap-2">
            <span>Recommended Agronomic Next Steps</span>
          </h3>
          <ol className="space-y-3 text-xs sm:text-sm text-gray-700 leading-relaxed list-decimal list-inside">
            <li>
              <strong>Review flagged nutrients with a specialist:</strong> Share this report with your qualified agricultural consultant or viticulturist before adjusting fertigation programs.
            </li>
            <li>
              <strong>Cross-check with soil and water tests:</strong> If Sodium or Chloride is elevated, verify electrical conductivity (EC) of your irrigation source and soil profile.
            </li>
            <li>
              <strong>Confirm vegetative vigor in field:</strong> Inspect leaf color, shoot length, and internode spacing to correlate analytical findings with visible canopy phenotype.
            </li>
            <li>
              <strong>Maintain fertilization logs:</strong> Record all basal and foliar applications to trace nutrient mobility and avoid nutrient antagonisms (e.g. excess Potassium suppressing Magnesium).
            </li>
          </ol>
        </div>

        {/* Panel 2: Safety & Educational Notice */}
        <div className="bg-[#FFFDF8] rounded-3xl p-6 sm:p-8 border border-amber-200/80 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-amber-900 flex items-center gap-2">
            <span>Safety Guidance & Decision Support</span>
          </h3>
          <p className="text-xs sm:text-sm text-amber-950/85 leading-relaxed">
            In compliance with safe agricultural advisory practices:
          </p>
          <ul className="space-y-2 text-xs text-amber-950/80">
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>No prescriptive chemical doses:</strong> This system does not issue chemical quantities or exact fertilizer weights, as field moisture, soil texture, and vine age require personalized calculation.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>Avoid hasty corrective applications:</strong> Elevated readings should first be confirmed by checking spray residues on unwashed leaves or re-sampling before applying antagonists.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>Regional variability:</strong> Local agro-climatic conditions across Maharashtra (Nashik, Sangli, Solapur, Pune) may justify minor adjustments to standard target thresholds.</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
