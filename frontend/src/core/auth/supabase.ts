import { ENV } from "../config/env";

/**
 * Token manager for Supabase Auth in the browser.
 * Persists session and retrieves JWT token to attach to API requests.
 */
class AuthManager {
  private tokenKey = "memorizeme_auth_token";

  setToken(token: string | null) {
    if (token) {
      localStorage.setItem(this.tokenKey, token);
    } else {
      localStorage.removeItem(this.tokenKey);
    }
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isAuthenticated(): boolean {
    return Boolean(this.getToken());
  }

  logout() {
    this.setToken(null);
  }
}

export const authManager = new AuthManager();

