import { ENV } from "../config/env";
import { authManager } from "../auth/supabase";

export interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean | undefined>;
}

export class ApiError extends Error {
  constructor(public status: number, message: string, public data?: any) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Universal Fetch API client for MemorizeMe backend.
 * Automatically injects Supabase JWT Bearer token into headers.
 */
export async function apiClient<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { params, headers = {}, ...rest } = options;

  let url = `${ENV.API_BASE_URL}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined) searchParams.append(key, String(val));
    });
    const qs = searchParams.toString();
    if (qs) url += `?${qs}`;
  }

  const reqHeaders: Record<string, string> = {
    "Content-Type": "application/json; charset=utf-8",
    Accept: "application/json",
    ...(headers as Record<string, string>),
  };

  const token = authManager.getToken();
  if (token) {
    reqHeaders["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...rest,
    headers: reqHeaders,
  });

  if (response.status === 204) {
    return null as T;
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(response.status, data?.detail || "An unexpected API error occurred", data);
  }

  return data as T;
}

