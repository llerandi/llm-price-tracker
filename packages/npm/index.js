"use strict";

/**
 * llm-price-tracker
 * Daily-updated LLM pricing data, served via jsDelivr CDN.
 * No dependencies - uses the global fetch (Node >= 18, all modern browsers).
 *
 * @example
 * const { fetchPrices, getModel, getProvider } = require("llm-price-tracker");
 *
 * const { models } = await fetchPrices();
 * const sonnet = await getModel("claude-sonnet-5");
 * const { models: anthropicModels } = await getProvider("anthropic");
 */

const BASE_URL =
  "https://cdn.jsdelivr.net/gh/llerandi/llm-price-tracker@main";

async function _get(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`llm-price-tracker: HTTP ${res.status} for ${url}`);
  return res.json();
}

/**
 * Fetch the full prices dataset (all providers and models).
 * @returns {Promise<{last_updated: string, models: object[]}>}
 */
async function fetchPrices() {
  return _get(`${BASE_URL}/data/prices.json`);
}

/**
 * Fetch a single model by its API identifier.
 * @param {string} modelId - e.g. "claude-sonnet-5", "gpt-4.1", "amazon.nova-pro-v1"
 * @returns {Promise<object|null>} The model object, or null if not found.
 */
async function getModel(modelId) {
  const data = await fetchPrices();
  return data.models.find((m) => m.model_id === modelId) ?? null;
}

/**
 * Fetch all models for a single provider.
 * @param {string} providerSlug - lowercase hyphenated slug, e.g. "anthropic",
 *   "openai", "google", "mistral", "amazon-bedrock", "xai", "perplexity"
 * @returns {Promise<{last_updated: string, models: object[]}>}
 */
async function getProvider(providerSlug) {
  return _get(`${BASE_URL}/data/providers/${providerSlug}.json`);
}

module.exports = { fetchPrices, getModel, getProvider, BASE_URL };
