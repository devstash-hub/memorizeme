/**
 * Environment configuration for MemorizeMe Frontend.
 * Supports Vite (`import.meta.env`) and fallback to window/process.
 */
export const ENV = {
  API_BASE_URL: (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  SUPABASE_URL: (import.meta as any).env?.VITE_SUPABASE_URL || "",
  SUPABASE_ANON_KEY: (import.meta as any).env?.VITE_SUPABASE_ANON_KEY || "",
};

