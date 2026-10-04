import React from 'react';
import { Link } from 'react-router-dom';
import {
  FlaskConical,
  FileCheck2,
  BookOpen,
  ArrowRight,
  ShieldAlert,
  Sparkles,
  Award,
  Compass,
  FileText,
  Leaf,
  CheckCircle2,
} from 'lucide-react';

export const HomePage: React.FC = () => {
  return (
    <div className="space-y-16 pb-16">
      {/* ── HERO SECTION ── */}
      <section className="relative overflow-hidden bg-gradient-to-b from-[#54245F] to-[#3a1842] text-white">
        {/* Background vineyard image overlay */}
        <div className="absolute inset-0 opacity-25 mix-blend-overlay pointer-events-none">
          <img
            src="/vineyard_hero.jpg"
            alt="Grape Vineyard Landscape"
            className="w-full h-full object-cover"
          />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Content */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 text-xs font-semibold tracking-wide uppercase text-[#98D65F]">
                <Leaf size={14} />
                <span>Petiole Analysis Decision Support for Viticulture</span>
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight text-white">
                Understand Your Grape Leaf Nutrients.{' '}
                <span className="text-[#98D65F]">Make Informed Decisions.</span>
              </h1>

              <p className="text-base sm:text-lg text-white/85 max-w-2xl leading-relaxed">
                Enter your petiole/leaf analysis values to understand nutrient status and receive clear educational guidance based on configured petiole reference standards.
              </p>

              <div className="flex flex-wrap gap-4 pt-2">
                <Link
                  to="/analyze"
                  className="px-6 py-3.5 rounded-xl bg-[#4F772D] hover:bg-[#436625] text-white font-semibold shadow-lg hover:shadow-xl transition-all flex items-center gap-2 border border-white/20 hover:scale-[1.02]"
                >
                  <FlaskConical size={18} />
                  <span>Analyze Your Sample</span>
                  <ArrowRight size={18} />
                </Link>

                <a
                  href="#how-it-works"
                  className="px-6 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold backdrop-blur-xs transition-all flex items-center gap-2 border border-white/20"
                >
                  <Compass size={18} />
                  <span>How It Works</span>
                </a>
              </div>

              {/* Quick stats / Highlights */}
              <div className="pt-6 grid grid-cols-3 gap-4 border-t border-white/15">
                <div>
                  <div className="text-2xl font-bold text-white">16</div>
                  <div className="text-xs text-white/70">Nutrient Parameters</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-[#98D65F]">100%</div>
                  <div className="text-xs text-white/70">Rule-Based Clarity</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">3-Page</div>
                  <div className="text-xs text-white/70">Printable Advisory PDF</div>
                </div>
              </div>
            </div>

            {/* Right Card / Visual */}
            <div className="lg:col-span-5">
              <div className="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-white/20 bg-white/5 backdrop-blur-xs group">
                <img
                  src="/vineyard_hero.jpg"
                  alt="Vineyard with ripe grapes"
                  className="w-full h-80 sm:h-96 object-cover transform group-hover:scale-105 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#29232D]/90 via-transparent to-transparent flex flex-col justify-end p-6">
                  <span className="text-xs font-semibold uppercase tracking-wider text-[#98D65F] mb-1">
                    Precision Viticulture
                  </span>
                  <h3 className="text-lg font-bold text-white">
                    Balanced Nutrients, Resilient Vines
                  </h3>
                  <p className="text-xs text-white/80 mt-1">
                    Calibrated specifically for grape petiole laboratory sampling.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS SECTION ── */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-[#4F772D] bg-[#EAF3E2] px-3 py-1 rounded-full">
            Simple 4-Step Process
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#54245F] mt-3">
            How GrapeLeaf AI Works
          </h2>
          <p className="text-sm sm:text-base text-gray-600 mt-2">
            No complicated jargon. Direct interpretation of laboratory results against established viticultural reference ranges.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            {
              step: '01',
              title: 'Enter Laboratory Data',
              desc: 'Input measured values from your petiole/leaf lab report. All 16 macronutrients, micronutrients, and ions are supported.',
              icon: FlaskConical,
            },
            {
              step: '02',
              title: 'Standard Alignment',
              desc: 'Values are benchmarked against official Petiole Reference Standards with transparent boundary rules.',
              icon: BookOpen,
            },
            {
              step: '03',
              title: 'Nutrient Status & Alerts',
              desc: 'Instant classification into Low, Optimum, High, Safe, or Above Safe Limit with contextual explanations.',
              icon: FileCheck2,
            },
            {
              step: '04',
              title: 'Educational PDF Report',
              desc: 'Download a clean, multi-page advisory report summarizing observations and next steps to share with your agronomist.',
              icon: FileText,
            },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.step}
                className="relative bg-white rounded-2xl p-6 border border-gray-200 shadow-xs hover:shadow-md transition-all flex flex-col justify-between group hover:border-[#7B3F98]/40"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-2xl font-black text-[#54245F]/20 group-hover:text-[#54245F] transition-colors">
                      {item.step}
                    </span>
                    <div className="w-10 h-10 rounded-xl bg-[#F6F1F8] flex items-center justify-center text-[#54245F] group-hover:bg-[#54245F] group-hover:text-white transition-all">
                      <Icon size={20} />
                    </div>
                  </div>
                  <h3 className="text-base font-bold text-[#29232D] mb-2">
                    {item.title}
                  </h3>
                  <p className="text-xs text-gray-600 leading-relaxed">
                    {item.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── PETIOLE STRUCTURE & SCIENCE SECTION ── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-[#F6F1F8] rounded-3xl p-8 lg:p-12 border border-[#7B3F98]/20">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            <div className="lg:col-span-5">
              <div className="rounded-2xl overflow-hidden shadow-md border-2 border-white">
                <img
                  src="/leaf_petiole.jpg"
                  alt="Grape leaf petiole structure"
                  className="w-full h-72 object-cover"
                />
              </div>
            </div>
            <div className="lg:col-span-7 space-y-4">
              <span className="text-xs font-bold uppercase tracking-wider text-[#7B3F98] bg-white px-3 py-1 rounded-full shadow-xs">
                Agronomic Context
              </span>
              <h3 className="text-2xl font-extrabold text-[#54245F]">
                Why Grape Petiole Analysis?
              </h3>
              <p className="text-sm text-[#29232D]/85 leading-relaxed">
                The leaf petiole (leaf stalk) serves as the primary conduit between the vine’s vascular system and photosynthetic tissue. During key diagnostic growth windows in major grape regions, petiole nutrient concentrations provide the most reliable snapshot of vine reserve status before fruit bud differentiation and cluster emergence.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <div className="flex items-start gap-2">
                  <CheckCircle2 size={16} className="text-[#4F772D] shrink-0 mt-0.5" />
                  <span className="text-xs text-gray-700">Detect hidden hunger before symptoms appear</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 size={16} className="text-[#4F772D] shrink-0 mt-0.5" />
                  <span className="text-xs text-gray-700">Monitor toxicity hazards like Sodium and Chloride</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 size={16} className="text-[#4F772D] shrink-0 mt-0.5" />
                  <span className="text-xs text-gray-700">Prevent over-fertilization and nitrate surges</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 size={16} className="text-[#4F772D] shrink-0 mt-0.5" />
                  <span className="text-xs text-gray-700">Calibrated for standard wine & table varieties</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── KEY FEATURES ── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-[#54245F] bg-[#F6F1F8] px-3 py-1 rounded-full">
            Engineered For Farmers
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#54245F] mt-3">
            Core Features of GrapeLeaf AI
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-xs space-y-3">
            <div className="w-12 h-12 rounded-xl bg-[#EAF3E2] text-[#4F772D] flex items-center justify-center">
              <Sparkles size={24} />
            </div>
            <h3 className="text-lg font-bold text-[#29232D]">Transparent Classification</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Every result is strictly computed with transparent rule-based logic against published petiole reference standards. No hidden black boxes or artificial guessing.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-xs space-y-3">
            <div className="w-12 h-12 rounded-xl bg-[#F6F1F8] text-[#54245F] flex items-center justify-center">
              <FileText size={24} />
            </div>
            <h3 className="text-lg font-bold text-[#29232D]">Comprehensive 3-Page PDF</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Generates an executive PDF report containing sample metadata, complete results table, observation grouping, and actionable advisory notes ready for printing.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-xs space-y-3">
            <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center">
              <Award size={24} />
            </div>
            <h3 className="text-lg font-bold text-[#29232D]">Salinity & Toxicity Guard</h3>
            <p className="text-xs text-gray-600 leading-relaxed">
              Specialized threshold checking for Sodium (Na) and Chloride (Cl) below 0.5% helps viticulturists detect salinity stress early before leaf scorch occurs.
            </p>
          </div>
        </div>
      </section>

      {/* ── PRECAUTIONS & LIMITATIONS ── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-amber-50/60 rounded-3xl p-8 border border-amber-200 space-y-4">
          <div className="flex items-center gap-2 text-amber-900 font-bold text-lg">
            <ShieldAlert className="text-amber-600 w-6 h-6 shrink-0" />
            <h3>Important Precautions and Agronomic Limitations</h3>
          </div>
          <p className="text-xs sm:text-sm text-amber-950/85 leading-relaxed">
            Nutrient concentrations in grape petioles are dynamic and influenced by multiple field factors:
          </p>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs text-amber-950/80">
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>Grape Variety & Rootstock:</strong> Varieties (Thompson Seedless, Sharad, Cabernet) and rootstocks (Dogridge, 110R) exhibit distinct nutrient uptake dynamics.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>Growth Stage:</strong> Current standards apply specifically to grape petiole diagnostic sampling.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>Soil & Irrigation:</strong> Soil pH, electrical conductivity, and water quality directly impact nutrient availability.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-600 font-bold">•</span>
              <span><strong>Lab Procedures:</strong> Sample washing, drying, and digestion techniques can introduce measurement variations.</span>
            </li>
          </ul>
        </div>
      </section>

      {/* ── CALL TO ACTION ── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="bg-[#54245F] rounded-3xl p-10 lg:p-14 text-white shadow-xl space-y-6">
          <h2 className="text-2xl sm:text-3xl font-extrabold">
            Ready to Evaluate Your Vineyard’s Nutrient Balance?
          </h2>
          <p className="text-sm sm:text-base text-white/80 max-w-xl mx-auto leading-relaxed">
            Have your laboratory analysis sheet handy. It takes under 60 seconds to enter values and view your structured assessment.
          </p>
          <div>
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-[#4F772D] hover:bg-[#3f6024] text-white font-bold text-base shadow-lg transition-all hover:scale-105"
            >
              <FlaskConical size={20} />
              <span>Start Analysis Now</span>
              <ArrowRight size={20} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
