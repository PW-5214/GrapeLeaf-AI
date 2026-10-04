import React from 'react';
import { Link } from 'react-router-dom';
import { Grape, ShieldAlert, Sparkles } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#29232D] text-white/80 border-t border-white/10 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-[#54245F] flex items-center justify-center border border-white/20">
                <Grape className="w-5 h-5 text-[#98D65F]" />
              </div>
              <span className="font-bold text-lg text-white">GrapeLeaf AI</span>
            </div>
            <p className="text-sm text-white/70 max-w-md leading-relaxed">
              Smart petiole and leaf nutrient analysis platform engineered specifically for viticulturists.
              Translating lab findings into clear educational guidance based on Petiole Reference Standards.
            </p>
            <div className="inline-flex items-center gap-2 text-xs bg-[#54245F]/50 border border-white/10 px-3 py-1.5 rounded-full text-white/90">
              <Sparkles size={13} className="text-[#98D65F]" />
              <span>Transparent Rule-Based Classification Engine</span>
            </div>
          </div>

          {/* Navigation */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white mb-3">
              Application
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="hover:text-white transition-colors">
                  Home & Overview
                </Link>
              </li>
              <li>
                <Link to="/analyze" className="hover:text-white transition-colors">
                  Analyze Sample
                </Link>
              </li>
              <li>
                <Link to="/report" className="hover:text-white transition-colors">
                  My Report
                </Link>
              </li>
              <li>
                <Link to="/standards" className="hover:text-white transition-colors">
                  Reference Standards
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-white transition-colors">
                  About the System
                </Link>
              </li>
            </ul>
          </div>

          {/* Reference & Quality */}
          <div>
            <h4 className="text-sm font-semibold uppercase tracking-wider text-white mb-3">
              Standards
            </h4>
            <p className="text-xs text-white/70 leading-relaxed mb-3">
              Configured for standard petiole tissue analysis. Reference limits should be reviewed and validated periodically by local agronomic specialists.
            </p>
            <div className="text-xs text-[#98D65F] font-medium">
              Viticulture Decision Support v1.0
            </div>
          </div>
        </div>

        {/* Educational Disclaimer Banner */}
        <div className="rounded-xl bg-[#1e1921] border border-amber-500/20 p-4 mb-6 flex flex-col sm:flex-row gap-3 items-start sm:items-center">
          <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5 sm:mt-0" />
          <p className="text-xs text-white/75 leading-relaxed">
            <strong className="text-amber-300">Educational Disclaimer:</strong> This application provides educational decision support based on entered values and configured reference standards. It is not a substitute for professional agricultural advice. Verify recommendations with a qualified agricultural expert before taking corrective action. No guaranteed yield improvement, disease detection, or crop recovery is promised or implied.
          </p>
        </div>

        {/* Bottom Bar */}
        <div className="pt-4 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-xs text-white/50 gap-2">
          <p>© {new Date().getFullYear()} GrapeLeaf AI. All rights reserved.</p>
          <p className="tracking-wide">
            GrapeLeaf AI | Petiole Reference Standards | Educational Decision Support
          </p>
        </div>
      </div>
    </footer>
  );
};
