export interface Model {
  provider: string;
  model_id: string;
  model_name: string;
  input_per_1m_usd: number | null;
  output_per_1m_usd: number | null;
  context_window_k: number | null;
  supports_vision: boolean;
  supports_function_calling: boolean;
  is_reasoning: boolean;
  tier: "efficient" | "performance" | "flagship" | "specialized";
  notes: string;
  batch_input_per_1m_usd?: number | null;
  batch_output_per_1m_usd?: number | null;
  cache_read_per_1m_usd?: number | null;
  cache_write_per_1m_usd?: number | null;
}

export interface PricesData {
  last_updated: string;
  models: Model[];
}

export declare const BASE_URL: string;

/** Fetch the full prices dataset (all providers and models). */
export declare function fetchPrices(): Promise<PricesData>;

/** Fetch a single model by its API identifier, or null if not found. */
export declare function getModel(modelId: string): Promise<Model | null>;

/** Fetch all models for a single provider by its lowercase hyphenated slug. */
export declare function getProvider(providerSlug: string): Promise<PricesData>;
