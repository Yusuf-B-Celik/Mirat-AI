export interface Finding {
  id: string;
  category: string;
  category_id: string;
  title: string;
  method: string;
  metric: string;
  value: number | string | null;
  null_p: number | null;
  q_value: number | null;
  effect_size: number | null;
  evidence: string[];
  detail: string;
  llm_assisted: boolean;
  kind: string;
  is_significant: boolean;
  is_honest_null: boolean;
}

export interface CategorySummary {
  id: string;
  name: string;
  runtime_sec: number;
  total_findings: number;
  significant_count: number;
}

export interface Surah {
  number: number;
  name_tr: string;
  name_ar: string;
  meaning: string;
  place: "Mekke" | "Medine";
  revelation_order: number;
  verses: number;
  juz: string;
  summary: string;
  is_peak: boolean;
}

export interface WaveformStats {
  observed_peaks_count: number;
  mean_random_peaks: number;
  spearman_mushaf_order: number;
  roughness: number;
  mean_random_roughness: number;
  evaluation: string;
}

export interface Claim {
  id: string;
  title: string;
  category: string;
  counts: string;
  raw_p: number;
  q_value_fdr: number;
  tost_equivalent: boolean;
  tost_p: number;
  bayes_factor_bf01: number;
  bayes_interpretation: string;
  filter_notes: string;
  filter_dependent: boolean;
  audit_tier: string;
  base_rate_p: number;
}

export interface PreregRecord {
  timestamp: string;
  hypothesis: string;
  model_name: string;
  target_roots: string[];
  expected_relation: string;
  hash: string;
  prev_hash: string;
}

export interface StatsSummary {
  words_count: number;
  segments_count: number;
  surahs_count: number;
  verses_count: number;
  discovery_categories: number;
  total_findings: number;
  significant_findings: number;
  honest_null_findings: number;
  unit_tests_count: number;
  unit_tests_pass_rate: number;
  llm_consensus_kappa_antonyms: number;
  llm_consensus_kappa_fields: number;
  llm_consensus_models: string[];
}

