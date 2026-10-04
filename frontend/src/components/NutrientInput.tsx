import React from 'react';
import type { NutrientStandard } from '../types';

interface NutrientInputProps {
  standard: NutrientStandard;
  value: string;
  onChange: (key: string, value: string) => void;
  error?: string;
}

export const NutrientInput: React.FC<NutrientInputProps> = ({
  standard,
  value,
  onChange,
  error,
}) => {
  const inputId = `nutrient-${standard.key}`;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    // Allow empty or numeric (including decimals)
    if (val === '' || /^[0-9]*\.?[0-9]*$/.test(val)) {
      onChange(standard.key, val);
    }
  };

  return (
    <div className="bg-white rounded-xl p-4 border border-gray-200 hover:border-[#7B3F98]/40 shadow-xs hover:shadow-sm transition-all flex flex-col justify-between">
      {/* Header */}
      <div>
        <div className="flex items-start justify-between gap-1 mb-1">
          <label htmlFor={inputId} className="font-semibold text-sm text-[#29232D]">
            {standard.displayName}
          </label>
          <span
            className={`text-xs px-2 py-0.5 rounded font-mono font-medium ${
              standard.unit === '%'
                ? 'bg-purple-50 text-[#54245F] border border-purple-200'
                : 'bg-emerald-50 text-[#4F772D] border border-emerald-200'
            }`}
          >
            {standard.unit}
          </span>
        </div>

        {/* Reference Range Indicator */}
        <div className="text-xs text-gray-500 mb-2.5 flex items-center justify-between">
          <span>
            {standard.isSafeLimit ? 'Safe threshold:' : 'Ref. Range:'}{' '}
            <strong className="text-[#54245F] font-semibold">{standard.referenceRange}</strong>
          </span>
        </div>
      </div>

      {/* Input row */}
      <div>
        <div className="relative">
          <input
            id={inputId}
            type="text"
            inputMode="decimal"
            placeholder="e.g. —"
            value={value}
            onChange={handleChange}
            className={`w-full px-3 py-2 text-base font-mono rounded-lg border focus:outline-none focus:ring-2 transition-all ${
              error
                ? 'border-red-400 focus:ring-red-300 bg-red-50/40'
                : 'border-gray-300 focus:border-[#7B3F98] focus:ring-[#7B3F98]/20 bg-gray-50/50 hover:bg-white'
            }`}
          />
          <div className="absolute right-3 top-2.5 text-xs text-gray-400 font-mono pointer-events-none">
            {standard.unit}
          </div>
        </div>

        {error && <p className="text-xs text-red-600 mt-1">{error}</p>}

        {/* Short description / hint */}
        <p className="text-[11px] text-gray-500 mt-2 line-clamp-2 leading-relaxed" title={standard.description}>
          {standard.description}
        </p>
      </div>
    </div>
  );
};
