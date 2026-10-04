export type NutrientKey =
  | 'N'
  | 'NO3'
  | 'NH4_N'
  | 'P'
  | 'K'
  | 'Ca'
  | 'Mg'
  | 'S'
  | 'Fe'
  | 'Mn'
  | 'Zn'
  | 'Cu'
  | 'Boron'
  | 'Mo'
  | 'Na'
  | 'Cl';

export type ClassificationStatus =
  | 'Low'
  | 'Optimum'
  | 'High'
  | 'Safe'
  | 'Above Safe Limit'
  | 'Data Unavailable';

export interface NutrientStandard {
  key: NutrientKey;
  displayName: string;
  unit: '%' | 'ppm';
  referenceRange: string;
  isSafeLimit: boolean;
  safeLimit?: number;
  refMin?: number;
  refMax?: number;
  description: string;
}

export interface NutrientResult {
  nutrient_key: string;
  display_name: string;
  entered_value: number | null;
  unit: string;
  reference_range: string;
  status: ClassificationStatus;
  explanation: string;
  recommendation: string;
}

export interface AnalysisSummary {
  total_analyzed: number;
  low: number;
  optimum: number;
  high: number;
  safe: number;
  above_safe_limit: number;
  data_unavailable: number;
  attention_required: number;
}

export interface AnalysisResponse {
  sample_id: string | null;
  crop: string;
  location: string | null;
  season: 'October' | 'April' | 'Other';
  season_warning: boolean;
  analyzed_at: string;
  results: NutrientResult[];
  summary: AnalysisSummary;
}

export interface SampleFormData {
  sample_id: string;
  crop: string;
  location: string;
  season: 'October' | 'April' | 'Other';
  nutrients: Record<string, string>; // raw string values for form inputs
}
