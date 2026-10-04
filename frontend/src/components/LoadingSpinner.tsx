import React from 'react';
import { Grape } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Analyzing leaf nutrient metrics...',
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 space-y-4">
      <div className="relative">
        <div className="w-16 h-16 rounded-full border-4 border-[#EAF3E2] border-t-[#54245F] animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <Grape className="w-6 h-6 text-[#7B3F98] animate-pulse" />
        </div>
      </div>
      <p className="text-sm font-medium text-[#54245F] tracking-wide animate-pulse">
        {message}
      </p>
    </div>
  );
};
