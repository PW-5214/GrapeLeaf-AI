import React, { useState } from 'react';
import { OCTOBER_STANDARDS_CONFIG } from '../config/standards';
import { BookOpen, CheckCircle2 } from 'lucide-react';

export const StandardsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'ALL' | 'MACRO' | 'MICRO' | 'IONS'>('ALL');

  const macroKeys = ['N', 'NO3', 'NH4_N', 'P', 'K', 'Ca', 'Mg', 'S'];
  const microKeys = ['Fe', 'Mn', 'Zn', 'Cu', 'Boron', 'Mo'];
  const ionKeys = ['Na', 'Cl'];

  const filteredStandards = OCTOBER_STANDARDS_CONFIG.filter((s) => {
    if (activeTab === 'MACRO') return macroKeys.includes(s.key);
    if (activeTab === 'MICRO') return microKeys.includes(s.key);
    if (activeTab === 'IONS') return ionKeys.includes(s.key);
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* ── HEADER BANNER ── */}
      <div className="bg-[#54245F] text-white rounded-3xl p-8 sm:p-10 shadow-lg relative overflow-hidden">
        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-xs font-semibold text-[#98D65F] uppercase tracking-wider">
            <BookOpen size={14} />
            <span>Benchmark Library</span>
          </div>
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-white">
            Petiole Reference Standards
          </h1>
          <p className="text-sm sm:text-base text-white/80 leading-relaxed">
            Standard petiole nutrient concentration guidelines used for nutritional diagnosis in grape vineyards.
          </p>
        </div>
      </div>

      {/* ── EXPERT VALIDATION NOTICE ── */}
      <div className="rounded-2xl bg-[#EAF3E2] border border-[#4F772D]/30 p-5 flex items-start gap-4 text-[#29232D] shadow-xs">
        <CheckCircle2 className="w-6 h-6 text-[#4F772D] shrink-0 mt-0.5" />
        <div className="space-y-1 text-xs sm:text-sm leading-relaxed">
          <h3 className="font-bold text-[#385620]">
            Agricultural Expert Validation Note
          </h3>
          <p className="text-[#29232D]/85">
            These reference standards provide a baseline framework for petiole evaluation. <strong>Reference standards should be reviewed and validated periodically by qualified agricultural experts</strong> and extension specialists to match specific cultivar genetics, rootstock graft combinations, and localized micro-climates.
          </p>
        </div>
      </div>

      {/* ── STANDARDS TABLE WITH CATEGORY TABS ── */}
      <div className="bg-white rounded-3xl border border-gray-200 shadow-xs overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-[#54245F]">
              Official Reference Table
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              16 essential parameters including primary, secondary, micronutrients, and toxicity indicators.
            </p>
          </div>

          {/* Category Filter */}
          <div className="flex items-center gap-1.5 bg-gray-100 p-1 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setActiveTab('ALL')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === 'ALL'
                  ? 'bg-white text-[#54245F] shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              All (16)
            </button>
            <button
              onClick={() => setActiveTab('MACRO')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === 'MACRO'
                  ? 'bg-white text-[#54245F] shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Macronutrients (8)
            </button>
            <button
              onClick={() => setActiveTab('MICRO')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === 'MICRO'
                  ? 'bg-white text-[#54245F] shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Micronutrients (6)
            </button>
            <button
              onClick={() => setActiveTab('IONS')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeTab === 'IONS'
                  ? 'bg-white text-[#54245F] shadow-xs'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Salinity / Toxicity (2)
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#F6F1F8]/80 text-[#54245F] text-xs uppercase font-bold tracking-wider border-b border-gray-200">
              <tr>
                <th className="py-3.5 px-6">Nutrient Parameter</th>
                <th className="py-3.5 px-4">Chemical Symbol</th>
                <th className="py-3.5 px-3">Unit</th>
                <th className="py-3.5 px-6">Configured Reference Range</th>
                <th className="py-3.5 px-6">Classification Rule</th>
                <th className="py-3.5 px-6">Biological Role in Grapevines</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredStandards.map((std) => (
                <tr key={std.key} className="hover:bg-gray-50/70 transition-colors">
                  <td className="py-4 px-6 font-bold text-[#29232D]">
                    {std.displayName}
                  </td>
                  <td className="py-4 px-4 font-mono font-semibold text-xs text-[#7B3F98]">
                    {std.key}
                  </td>
                  <td className="py-4 px-3 text-xs text-gray-500 font-mono">
                    {std.unit}
                  </td>
                  <td className="py-4 px-6">
                    <span className="font-bold text-[#54245F] bg-[#F6F1F8] px-2.5 py-1 rounded-md text-xs border border-[#7B3F98]/20">
                      {std.referenceRange}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-xs text-gray-600">
                    {std.isSafeLimit ? (
                      <span className="text-gray-700">
                        &lt; {std.safeLimit}%: <strong className="text-[#4F772D]">Safe</strong> | &ge; {std.safeLimit}%: <strong className="text-red-600">Above Safe Limit</strong>
                      </span>
                    ) : (
                      <span className="text-gray-700">
                        &lt; {std.refMin}: <strong className="text-amber-600">Low</strong> | {std.refMin}–{std.refMax}: <strong className="text-[#4F772D]">Optimum</strong> | &gt; {std.refMax}: <strong className="text-orange-600">High</strong>
                      </span>
                    )}
                  </td>
                  <td className="py-4 px-6 text-xs text-gray-600 leading-relaxed max-w-sm">
                    {std.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* ── FACTORS INFLUENCING REFERENCE STANDARDS ── */}
      <div className="bg-white rounded-3xl p-8 border border-gray-200 shadow-xs space-y-6">
        <div>
          <h2 className="text-xl font-bold text-[#54245F]">
            Factors Influencing Petiole Nutrient Standards
          </h2>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Why rigid single numbers cannot replace qualified agronomic judgment:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="p-4 rounded-2xl bg-[#FFFDF8] border border-gray-200 space-y-2">
            <h3 className="text-sm font-bold text-[#54245F]">🍇 Grape Variety</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Table grape varieties (Thompson Seedless, Manik Chaman, Sharad Seedless) have different crop loads and nutrient partitioning than wine varieties (Cabernet Sauvignon, Shiraz, Sauvignon Blanc).
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FFFDF8] border border-gray-200 space-y-2">
            <h3 className="text-sm font-bold text-[#54245F]">🌱 Growth Stage</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Nutrient levels fluctuate across growth cycles from bloom to veraison. These standards strictly calibrate petiole tissue diagnostic sampling.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FFFDF8] border border-gray-200 space-y-2">
            <h3 className="text-sm font-bold text-[#54245F]">📍 Regional & Soil Factors</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Black cotton soils, calcareous soils with high free calcium carbonate, and red gravelly loams across Maharashtra influence micronutrient fixation and potassium-magnesium balance.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FFFDF8] border border-gray-200 space-y-2">
            <h3 className="text-sm font-bold text-[#54245F]">💧 Irrigation & Water Quality</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              High bicarbonate or sodium in borewell water causes salinity stress, competing with potassium and calcium uptake in petiole tissues.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FFFDF8] border border-gray-200 space-y-2">
            <h3 className="text-sm font-bold text-[#54245F]">🌤️ Climate & Temperature</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Transpiration rates, night temperatures, and humidity govern calcium translocation and nitrate reductase enzyme activity.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FFFDF8] border border-gray-200 space-y-2">
            <h3 className="text-sm font-bold text-[#54245F]">🧪 Laboratory Procedures</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Methods of petiole washing (distilled water wash), drying temperature (65°C), and digestion reagents (di-acid vs tri-acid) determine analytical precision.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
