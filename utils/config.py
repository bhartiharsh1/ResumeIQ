"""
config.py — Centralized API key loader for ResumeIQ.

Priority order:
  1. Streamlit secrets (st.secrets) — used on Streamlit Cloud
  2. OS environment variable — works if set via shell or a parent process
  3. .env file — used for local development (not committed to Git)

NEVER hardcode secrets here. Use .env locally and st.secrets on the cloud.
"""
import os

_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")

# Load .env once at import time (no-op if file doesn't exist)
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=_ENV_PATH, override=False)
except Exception:
    pass


def _st_secret(key: str) -> str:
    """Safely read a key from st.secrets — works on both Cloud and local."""
    try:
        import streamlit as st
        val = st.secrets.get(key)          # returns None if missing, never raises
        return (val or "").strip()
    except Exception:
        return ""


def get_openrouter_key() -> str:
    """Return the OpenRouter API key. Raises RuntimeError if not configured."""
    key = _st_secret("OPENROUTER_API_KEY")
    if key:
        return key

    key = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
    if key:
        return key

    raise RuntimeError(
        "OPENROUTER_API_KEY is not set.\n"
        "  * Local dev: add it to your .env file\n"
        "  * Streamlit Cloud: add it to App Settings -> Secrets"
    )


def get_apollo_key() -> str:
    """Return the Apollo API key. Returns empty string if not configured."""
    key = _st_secret("APOLLO_API_KEY")
    if key:
        return key
    return (os.environ.get("APOLLO_API_KEY") or "").strip()
