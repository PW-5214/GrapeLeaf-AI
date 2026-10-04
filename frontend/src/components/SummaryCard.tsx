import React from 'react';
import type { LucideIcon } from 'lucide-react';

interface SummaryCardProps {
  title: string;
  count: number;
  icon: LucideIcon;
  variant: 'default' | 'optimum' | 'low' | 'high' | 'safe' | 'alert' | 'attention';
  subtitle?: string;
}

export const SummaryCard: React.FC<SummaryCardProps> = ({
  title,
  count,
  icon: Icon,
  variant,
  subtitle,
}) => {
  const styles = {
    default: {
      bg: 'bg-white',
      border: 'border-gray-200',
      text: 'text-[#29232D]',
      iconBg: 'bg-gray-100 text-gray-700',
      badge: 'text-gray-600',
    },
    optimum: {
      bg: 'bg-emerald-50/70',
      border: 'border-[#4F772D]/30',
      text: 'text-[#385620]',
      iconBg: 'bg-[#4F772D]/20 text-[#4F772D]',
      badge: 'text-[#4F772D]',
    },
    safe: {
      bg: 'bg-emerald-50/70',
      border: 'border-[#4F772D]/30',
      text: 'text-[#385620]',
      iconBg: 'bg-[#4F772D]/20 text-[#4F772D]',
      badge: 'text-[#4F772D]',
    },
    low: {
      bg: 'bg-amber-50/70',
      border: 'border-amber-300',
      text: 'text-amber-900',
      iconBg: 'bg-amber-100 text-amber-700',
      badge: 'text-amber-700',
    },
    high: {
      bg: 'bg-orange-50/70',
      border: 'border-orange-300',
      text: 'text-orange-900',
      iconBg: 'bg-orange-100 text-orange-700',
      badge: 'text-orange-700',
    },
    alert: {
      bg: 'bg-red-50/70',
      border: 'border-red-300',
      text: 'text-red-900',
      iconBg: 'bg-red-100 text-red-700',
      badge: 'text-red-700',
    },
    attention: {
      bg: 'bg-[#F6F1F8]',
      border: 'border-[#7B3F98]/30',
      text: 'text-[#54245F]',
      iconBg: 'bg-[#7B3F98]/15 text-[#54245F]',
      badge: 'text-[#54245F]',
    },
  }[variant];

  return (
    <div
      className={`rounded-2xl p-5 border ${styles.bg} ${styles.border} shadow-xs transition-all hover:shadow-sm flex items-center justify-between`}
    >
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1">
          {title}
        </p>
        <div className="flex items-baseline gap-2">
          <span className={`text-3xl font-extrabold ${styles.text}`}>
            {count}
          </span>
          {subtitle && (
            <span className="text-xs text-gray-500 font-medium">
              {subtitle}
            </span>
          )}
        </div>
      </div>
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${styles.iconBg}`}>
        <Icon size={24} />
      </div>
    </div>
  );
};
