/**
 * MemorizeMe Authentication Controller
 * Connects to Supabase Auth with fallback for local demo and testing.
 */

class AuthController {
  constructor() {
    this.mode = "login"; // "login" | "register" | "forgot"
    this.isLoading = false;

    this.initElements();
    this.initEvents();
  }

  initElements() {
    this.form = document.getElementById("authForm");
    this.tabLogin = document.getElementById("tabLogin");
    this.tabRegister = document.getElementById("tabRegister");
    this.authTitle = document.getElementById("authTitle");
    this.authSubtitle = document.getElementById("authSubtitle");

    this.nameGroup = document.getElementById("nameGroup");
    this.confirmPasswordGroup = document.getElementById("confirmPasswordGroup");
    this.formExtra = document.getElementById("formExtra");
    this.submitBtn = document.getElementById("submitBtn");
    this.submitBtnText = document.getElementById("submitBtnText");
    this.submitSpinner = document.getElementById("submitSpinner");

    this.alertBanner = document.getElementById("alertBanner");
    this.alertText = document.getElementById("alertText");

    this.togglePasswordBtn = document.getElementById("togglePassword");
    this.passwordInput = document.getElementById("password");

    this.forgotLink = document.getElementById("forgotLink");
  }

  initEvents() {
    // Mode switcher tabs
    this.tabLogin.addEventListener("click", () => this.setMode("login"));
    this.tabRegister.addEventListener("click", () => this.setMode("register"));

    if (this.forgotLink) {
      this.forgotLink.addEventListener("click", (e) => {
        e.preventDefault();
        this.setMode("forgot");
      });
    }

    // Toggle Password Visibility
    this.togglePasswordBtn.addEventListener("click", () => {
      const isPassword = this.passwordInput.type === "password";
      this.passwordInput.type = isPassword ? "text" : "password";
      this.togglePasswordBtn.innerHTML = isPassword
        ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`
        : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
    });

    // Social Login Buttons
    document.getElementById("btnGoogle")?.addEventListener("click", () => this.socialLogin("Google"));
    document.getElementById("btnGithub")?.addEventListener("click", () => this.socialLogin("GitHub"));

    // Form Submit
    this.form.addEventListener("submit", (e) => this.handleSubmit(e));
  }

  setMode(mode) {
    this.mode = mode;
    this.hideAlert();

    if (mode === "login") {
      this.tabLogin.classList.add("active");
      this.tabRegister.classList.remove("active");
      this.authTitle.textContent = "Welcome back! 👋";
      this.authSubtitle.textContent = "Access your decks and continue your daily study sessions.";
      this.nameGroup.style.display = "none";
      this.confirmPasswordGroup.style.display = "none";
      this.formExtra.style.display = "flex";
      this.submitBtnText.textContent = "Sign In";
    } else if (mode === "register") {
      this.tabRegister.classList.add("active");
      this.tabLogin.classList.remove("active");
      this.authTitle.textContent = "Create your free account 🚀";
      this.authSubtitle.textContent = "Start memorizing with spaced repetition today.";
      this.nameGroup.style.display = "block";
      this.confirmPasswordGroup.style.display = "block";
      this.formExtra.style.display = "none";
      this.submitBtnText.textContent = "Create MemorizeMe Account";
    } else if (mode === "forgot") {
      this.tabLogin.classList.remove("active");
      this.tabRegister.classList.remove("active");
      this.authTitle.textContent = "Reset Password 🔑";
      this.authSubtitle.textContent = "Enter your email to receive a password reset link.";
      this.nameGroup.style.display = "none";
      this.confirmPasswordGroup.style.display = "none";
      this.formExtra.style.display = "none";
      this.submitBtnText.textContent = "Send Reset Link";
    }
  }

  showAlert(message, type = "error") {
    this.alertText.textContent = message;
    this.alertBanner.className = `alert-banner ${type}`;
    this.alertBanner.style.display = "flex";
  }

  hideAlert() {
    this.alertBanner.style.display = "none";
  }

  setLoading(loading) {
    this.isLoading = loading;
    this.submitBtn.disabled = loading;
    this.submitSpinner.style.display = loading ? "inline-block" : "none";
    if (loading) {
      this.submitBtnText.dataset.orig = this.submitBtnText.textContent;
      this.submitBtnText.textContent = "Processing...";
    } else if (this.submitBtnText.dataset.orig) {
      this.submitBtnText.textContent = this.submitBtnText.dataset.orig;
    }
  }

  async handleSubmit(e) {
    e.preventDefault();
    this.hideAlert();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || (!password && this.mode !== "forgot")) {
      this.showAlert("Please fill in all required fields.");
      return;
    }

    if (this.mode === "register") {
      const confirmPassword = document.getElementById("confirmPassword").value;
      if (password !== confirmPassword) {
        this.showAlert("Passwords do not match.");
        return;
      }
      if (password.length < 6) {
        this.showAlert("Password must be at least 6 characters.");
        return;
      }
    }

    this.setLoading(true);

    try {
      // Check if Supabase client is configured in window/global
      if (window.supabase && typeof window.supabase.auth?.signInWithPassword === "function") {
        if (this.mode === "login") {
          const { data, error } = await window.supabase.auth.signInWithPassword({ email, password });
          if (error) throw error;
          localStorage.setItem("memorizeme_auth_token", data.session.access_token);
          this.showAlert("Signed in successfully! Redirecting...", "success");
          setTimeout(() => (window.location.href = "./index.html"), 900);
          return;
        } else if (this.mode === "register") {
          const { data, error } = await window.supabase.auth.signUp({ email, password });
          if (error) throw error;
          this.showAlert("Account created successfully! Check your email.", "success");
          setTimeout(() => this.setMode("login"), 1500);
          return;
        }
      }

      // Demo/Local Simulation Mode (when running standalone without configured Supabase keys)
      await new Promise((r) => setTimeout(r, 650));
      const demoToken = "demo-jwt-token-" + btoa(email);
      localStorage.setItem("memorizeme_auth_token", demoToken);

      if (this.mode === "login") {
        this.showAlert("Signed in successfully! Redirecting...", "success");
        setTimeout(() => (window.location.href = "./index.html"), 600);
      } else if (this.mode === "register") {
        this.showAlert("Account created successfully! Redirecting to study session...", "success");
        setTimeout(() => (window.location.href = "./index.html"), 800);
      } else {
        this.showAlert("Password reset email sent! Check your inbox.", "success");
        setTimeout(() => this.setMode("login"), 1500);
      }
    } catch (err) {
      this.showAlert(err.message || "Authentication failed. Please verify your credentials.");
    } finally {
      this.setLoading(false);
    }
  }

  async socialLogin(provider) {
    this.hideAlert();
    this.showAlert(`Starting authentication via ${provider}...`, "success");

    // Simulate or call Supabase OAuth
    setTimeout(() => {
      localStorage.setItem("memorizeme_auth_token", `oauth-${provider}-token-sample`);
      window.location.href = "./index.html";
    }, 600);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new AuthController();
});
