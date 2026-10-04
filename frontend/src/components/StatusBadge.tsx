import React from 'react';
import type { ClassificationStatus } from '../types';
import {
  ArrowDownCircle,
  ArrowUpCircle,
  CheckCircle2,
  ShieldCheck,
  AlertTriangle,
  HelpCircle,
} from 'lucide-react';

interface StatusBadgeProps {
  status: ClassificationStatus;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5 gap-1',
    md: 'text-sm px-2.5 py-1 gap-1.5',
    lg: 'text-base px-3 py-1.5 gap-2 font-medium',
  }[size];

  const iconSizes = {
    sm: 12,
    md: 15,
    lg: 18,
  }[size];

  switch (status) {
    case 'Optimum':
      return (
        <span
          className={`inline-flex items-center rounded-full font-semibold bg-[#4F772D]/15 text-[#385620] border border-[#4F772D]/30 ${sizeClasses}`}
        >
          <CheckCircle2 size={iconSizes} className="text-[#4F772D]" />
          <span>Optimum</span>
        </span>
      );

    case 'Safe':
      return (
        <span
          className={`inline-flex items-center rounded-full font-semibold bg-[#4F772D]/15 text-[#385620] border border-[#4F772D]/30 ${sizeClasses}`}
        >
          <ShieldCheck size={iconSizes} className="text-[#4F772D]" />
          <span>Safe Limit</span>
        </span>
      );

    case 'Low':
      return (
        <span
          className={`inline-flex items-center rounded-full font-semibold bg-amber-100 text-amber-900 border border-amber-300 ${sizeClasses}`}
        >
          <ArrowDownCircle size={iconSizes} className="text-amber-600" />
          <span>Low</span>
        </span>
      );

    case 'High':
      return (
        <span
          className={`inline-flex items-center rounded-full font-semibold bg-orange-100 text-orange-900 border border-orange-300 ${sizeClasses}`}
        >
          <ArrowUpCircle size={iconSizes} className="text-orange-600" />
          <span>High</span>
        </span>
      );

    case 'Above Safe Limit':
      return (
        <span
          className={`inline-flex items-center rounded-full font-semibold bg-red-100 text-red-900 border border-red-300 ${sizeClasses}`}
        >
          <AlertTriangle size={iconSizes} className="text-red-600" />
          <span>Above Safe Limit</span>
        </span>
      );

    case 'Data Unavailable':
    default:
      return (
        <span
          className={`inline-flex items-center rounded-full font-medium bg-gray-100 text-gray-700 border border-gray-200 ${sizeClasses}`}
        >
          <HelpCircle size={iconSizes} className="text-gray-500" />
          <span>Data Unavailable</span>
        </span>
      );
  }
};
