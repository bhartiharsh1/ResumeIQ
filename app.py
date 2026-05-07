import os
try:
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        override=True
    )
except Exception:
    pass

import streamlit as st
import re
from utils.pdf_parser import extract_text_from_pdf
from utils.skills import extract_skills
from utils.info_extractor import extract_basic_info
from utils.jd_file import jd_match_final
from utils.ats_ai import real_ats_score
from utils.advanced_ats import impact_score
from data.skills_db import SKILLS_DB
# ---------------- CONFIG ----------------
st.set_page_config(page_title="ResumeIQ Platform", layout="wide", page_icon="🧠")

# ── GLOBAL 3D THEME ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');


/* ── Base font — cascade only, never force-override icon fonts ── */
body { font-family: 'Outfit', sans-serif; }

/* ── Deep-space gradient background ── */
.stApp {
    background-color: #080c14 !important;
    background-image:
        radial-gradient(ellipse at 15% 40%, rgba(99,102,241,0.09) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 15%, rgba(139,92,246,0.09) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 90%, rgba(6,182,212,0.06) 0%, transparent 50%);
}

/* ── Sidebar — frosted-glass 3D panel ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0e1420 0%, #0a0f1a 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.25) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.6), inset -1px 0 0 rgba(99,102,241,0.12) !important;
}
section[data-testid="stSidebar"] * { color: #c4c9d8 !important; }
section[data-testid="stSidebar"] .stRadio label:hover { color: #a78bfa !important; }

/* ── Animated gradient headings ── */
h1 {
    background: linear-gradient(135deg, #667eea 0%, #a78bfa 45%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    filter: drop-shadow(0 0 24px rgba(102,126,234,0.35));
    animation: hue-rotate 6s linear infinite;
}
h2, h3 {
    background: linear-gradient(135deg, #e2eaf8 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700 !important;
}
@keyframes hue-rotate {
    0%   { filter: drop-shadow(0 0 24px rgba(102,126,234,0.35)) hue-rotate(0deg); }
    100% { filter: drop-shadow(0 0 24px rgba(102,126,234,0.35)) hue-rotate(360deg); }
}

/* ── 3D Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    letter-spacing: 0.4px !important;
    transform: perspective(600px) translateZ(0px);
    box-shadow:
        0 6px 20px rgba(102,126,234,0.45),
        0 1px 0 rgba(255,255,255,0.12) inset,
        0 -3px 0 rgba(0,0,0,0.25) inset !important;
    transition: all 0.15s cubic-bezier(0.4,0,0.2,1) !important;
}
.stButton > button:hover {
    transform: perspective(600px) translateZ(12px) translateY(-3px) !important;
    box-shadow:
        0 14px 36px rgba(102,126,234,0.65),
        0 1px 0 rgba(255,255,255,0.18) inset !important;
    background: linear-gradient(135deg, #7c8ef5 0%, #9d6cd4 100%) !important;
}
.stButton > button:active {
    transform: perspective(600px) translateZ(2px) translateY(1px) !important;
    box-shadow: 0 2px 8px rgba(102,126,234,0.35) !important;
}

/* ── 3D Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #131825 0%, #0f1520 100%) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 18px !important;
    padding: 20px !important;
    transform: perspective(900px) rotateX(3deg);
    box-shadow:
        0 12px 35px rgba(0,0,0,0.5),
        0 1px 0 rgba(255,255,255,0.04) inset,
        0 -5px 0 rgba(0,0,0,0.2) inset !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}
[data-testid="metric-container"]:hover {
    transform: perspective(900px) rotateX(0deg) translateY(-6px) !important;
    box-shadow: 0 24px 50px rgba(99,102,241,0.25) !important;
    border-color: rgba(99,102,241,0.55) !important;
}
[data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #667eea, #a78bfa) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
}

/* ── 3D Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(8,12,20,0.8) !important;
    border-bottom: 1px solid rgba(99,102,241,0.2) !important;
    padding: 0 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-radius: 10px 10px 0 0 !important;
    font-weight: 600 !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    padding: 10px 22px !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(99,102,241,0.1) !important;
    color: #e2eaf8 !important;
    transform: translateY(-2px) !important;
    border-color: rgba(99,102,241,0.25) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(102,126,234,0.22), rgba(167,139,250,0.12)) !important;
    color: #a78bfa !important;
    border-color: rgba(167,139,250,0.45) !important;
    border-bottom-color: transparent !important;
    box-shadow: 0 -4px 16px rgba(102,126,234,0.25) !important;
}

/* ── Glassmorphism Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: rgba(19,24,37,0.95) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 11px !important;
    color: #e2eaf8 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.35) inset !important;
    transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(99,102,241,0.65) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.35) inset, 0 0 0 3px rgba(99,102,241,0.18) !important;
}

/* ── 3D Expanders ── */
.stExpander {
    background: linear-gradient(135deg, #131825 0%, #0f1520 100%) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35), 0 1px 0 rgba(255,255,255,0.03) inset !important;
    transition: all 0.25s ease !important;
    overflow: hidden !important;
}
.stExpander:hover {
    border-color: rgba(99,102,241,0.45) !important;
    box-shadow: 0 12px 36px rgba(99,102,241,0.18) !important;
    transform: translateY(-2px) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    background: rgba(19,24,37,0.9) !important;
    border: 2px dashed rgba(99,102,241,0.4) !important;
    border-radius: 14px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(99,102,241,0.85) !important;
    background: rgba(99,102,241,0.05) !important;
    box-shadow: 0 0 28px rgba(99,102,241,0.22) !important;
}

/* ── Progress bar — glowing ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #667eea, #a78bfa) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 12px rgba(102,126,234,0.55) !important;
}

/* ── Alerts — colour-coded 3D cards ── */
div[data-testid="stSuccessMessage"], .stSuccess, [class*="stSuccess"] {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-left: 4px solid #10b981 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.12) !important;
}
div[data-testid="stErrorMessage"], .stError, [class*="stError"] {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-left: 4px solid #ef4444 !important;
    border-radius: 12px !important;
}
div[data-testid="stWarningMessage"], .stWarning, [class*="stWarning"] {
    background: rgba(245,158,11,0.08) !important;
    border: 1px solid rgba(245,158,11,0.3) !important;
    border-left: 4px solid #f59e0b !important;
    border-radius: 12px !important;
}
div[data-testid="stInfoMessage"], .stInfo, [class*="stInfo"] {
    background: rgba(99,102,241,0.08) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-left: 4px solid #6366f1 !important;
    border-radius: 12px !important;
}

/* ── Dividers ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent) !important;
    margin: 28px 0 !important;
}

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #667eea, #764ba2);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: #a78bfa; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #667eea !important; }

/* ── Caption ── */
.stCaption, small { color: #4b5563 !important; font-size: 0.78rem !important; }

/* ── DataFrame table ── */
.stDataFrame {
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Selectbox dropdown ── */
div[data-baseweb="select"] > div {
    background: rgba(19,24,37,0.95) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 11px !important;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["📊 Single Analyzer", "⚖️ A/B Testing Engine", "🎯 Career Tools", "🙋 Resume Help"])

# ── PRO SESSION STATE ──────────────────────────────────────────────────────────
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

# ── ADMIN / HARDCODED CODES (fallback + owner access) ─────────────────────────
try:
    _raw = st.secrets.get("pro_codes", "")
    VALID_PRO_CODES = set(c.strip() for c in _raw.split(",") if c.strip())
except Exception:
    VALID_PRO_CODES = set()
VALID_PRO_CODES.update({"RESUMEIQ-PRO", "RIQA-2024", "UNLOCK-PRO-IQ"})

# ── WEBHOOK SERVER URL (set in secrets.toml as webhook_url) ───────────────────
try:
    WEBHOOK_SERVER_URL = st.secrets.get("webhook_url", "").rstrip("/")
except Exception:
    WEBHOOK_SERVER_URL = ""

def _validate_pro_code(code: str) -> bool:
    """Check code against hardcoded list OR the webhook server (customer codes)."""
    code_up = code.strip().upper()
    # 1. Hardcoded admin codes
    if code_up in {c.upper() for c in VALID_PRO_CODES}:
        return True
    # 2. Dynamically generated codes stored in Supabase via webhook server
    if WEBHOOK_SERVER_URL:
        try:
            import requests as _req
            resp = _req.get(
                f"{WEBHOOK_SERVER_URL}/validate",
                params={"code": code_up},
                timeout=5
            )
            if resp.status_code == 200:
                return resp.json().get("valid", False)
        except Exception:
            pass
    return False

# ── SIDEBAR PRO STATUS ─────────────────────────────────────────────────────────
st.sidebar.divider()
if not st.session_state.is_pro:
    st.sidebar.markdown(
        """
        <div style='background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);
                    border-radius:10px;padding:12px 14px;text-align:center;'>
            <div style='font-size:1rem;font-weight:800;color:#f59e0b;margin-bottom:4px;'>⚡ Upgrade to Pro</div>
            <div style='font-size:0.73rem;color:#9ca3af;margin-bottom:10px;'>Unlock all AI features — ₹79 one-time</div>
            <div style='font-size:0.75rem;color:#9ca3af;margin-top:4px;'>
                Enter your email on the feature page to get a personalized payment link →
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.success("✅ Pro Active — All features unlocked!")
    if st.sidebar.button("🔒 Sign Out of Pro", key="_signout_btn", use_container_width=True):
        st.session_state.is_pro = False
        st.rerun()


# ── PAYWALL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.paywall-card {
    background: linear-gradient(135deg, #0f1520 0%, #160e2a 100%);
    border: 1px solid rgba(245,158,11,0.4);
    border-radius: 18px;
    padding: 36px 40px;
    text-align: center;
    margin: 28px 0;
    box-shadow: 0 8px 40px rgba(245,158,11,0.13), 0 2px 0 rgba(255,255,255,0.03) inset;
}
.paywall-lock { font-size: 3rem; margin-bottom: 10px; }
.paywall-title {
    font-size: 1.25rem; font-weight: 800;
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 16px;
}
.paywall-bullets {
    list-style: none; padding: 0; margin: 0 0 24px 0;
    color: #9ca3af; font-size: 0.9rem; line-height: 2.2;
}
.paywall-bullets li::before { content: "✦  "; color: #f59e0b; }
.paywall-btn {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #000 !important; font-weight: 800; font-size: 1rem;
    padding: 14px 40px; border-radius: 30px; text-decoration: none !important;
    box-shadow: 0 6px 28px rgba(245,158,11,0.45); letter-spacing: 0.3px;
}
.paywall-note { margin-top: 14px; color: #6b7280; font-size: 0.78rem; }
/* ── Inline unlock strip ── */
.unlock-strip {
    margin-top: 28px;
    padding-top: 22px;
    border-top: 1px solid rgba(245,158,11,0.18);
}
.unlock-strip-label {
    font-size: 0.82rem; font-weight: 700; letter-spacing: 0.8px;
    color: #a78bfa; text-transform: uppercase; margin-bottom: 10px;
}
.badge-free {
    display: inline-block; background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.4); color: #10b981;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px;
    padding: 2px 9px; border-radius: 20px; text-transform: uppercase; vertical-align: middle;
}
.badge-pro {
    display: inline-block; background: rgba(245,158,11,0.15);
    border: 1px solid rgba(245,158,11,0.4); color: #f59e0b;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px;
    padding: 2px 9px; border-radius: 20px; text-transform: uppercase; vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

def pro_wall(feature_name, bullets):
    """Render a locked paywall card for a Pro feature, with inline code-unlock."""
    bullets_html = "".join(f"<li>{b}</li>" for b in bullets)
    # Sanitise feature name for use as a unique widget key
    _key = re.sub(r"[^a-z0-9]", "_", feature_name.lower())
    _link_key  = f"_wall_link_{_key}"
    _email_key = f"_wall_email_{_key}"

    st.markdown(f"""
    <div class="paywall-card">
        <div class="paywall-lock">🔒</div>
        <div class="paywall-title">{feature_name} — Pro Feature</div>
        <ul class="paywall-bullets">{bullets_html}</ul>
        <div class="paywall-note">⚡ One-time payment · ₹79 · No subscription · Instant email delivery</div>
        <div class="unlock-strip">
            <div class="unlock-strip-label">Step 1 · Enter your email to get a unique payment link →</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _col_l, _col_mid, _col_r = st.columns([1, 3, 1])
    with _col_mid:

        # ── STEP 1: Generate a unique payment link ──────────────────────────
        if _link_key not in st.session_state:
            _em_col, _nm_col = st.columns(2)
            with _em_col:
                _email = st.text_input(
                    "📧 Your Email",
                    placeholder="you@gmail.com",
                    key=f"_wall_email_{_key}",
                    help="Your access code is emailed to you after payment."
                )
            with _nm_col:
                _name = st.text_input(
                    "👤 Your Name (optional)",
                    placeholder="Rahul Sharma",
                    key=f"_wall_name_{_key}",
                )

            if st.button("⚡ Get My Payment Link →", key=f"_wall_gen_{_key}", use_container_width=True):
                _email_val   = (_email or "").strip()
                _name_val    = (_name  or "").strip()
                _static_link = "https://rzp.io/rzp/xxU96u4d"
                if not _email_val:
                    st.error("Please enter your email address to continue.")
                else:
                    _got_link = _static_link   # default fallback
                    if WEBHOOK_SERVER_URL:
                        with st.spinner("⏳ Generating your personal payment link..."):
                            try:
                                import requests as _req
                                _resp = _req.post(
                                    f"{WEBHOOK_SERVER_URL}/create-payment-link",
                                    json={"email": _email_val, "name": _name_val},
                                    timeout=30,
                                )
                                if _resp.status_code == 200:
                                    _got_link = _resp.json().get("url", _static_link)
                            except Exception:
                                pass  # silently use static link
                    st.session_state[_link_key]  = _got_link
                    st.session_state[_email_key] = _email_val
                    st.rerun()

        # ── STEP 2: Payment link + "I've Paid" polling ──────────────────────
        else:
            _pay_url     = st.session_state[_link_key]
            _saved_email = st.session_state.get(_email_key, "")
            _code_key    = f"_found_code_{_key}"

            # ── Code already found → show popup ─────────────────────────
            if st.session_state.get(_code_key):
                _found_code = st.session_state[_code_key]
                st.markdown(f"""
<style>
@keyframes rzqSlide {{
    from {{ transform: translateX(110%); opacity:0; }}
    to   {{ transform: translateX(0);   opacity:1; }}
}}
#rzq-popup {{
    position:fixed; top:20px; right:20px; z-index:9999999;
    background:linear-gradient(135deg,#0d1117,#1a0800);
    border:2px solid #f59e0b; border-radius:18px;
    padding:22px 26px; width:300px;
    box-shadow:0 8px 40px rgba(245,158,11,0.5);
    animation:rzqSlide 0.45s cubic-bezier(.22,1,.36,1);
    font-family:'Segoe UI',system-ui,sans-serif;
}}
#rzq-lbl  {{ color:#f59e0b; font-weight:800; font-size:1rem; margin-bottom:4px; }}
#rzq-sub  {{ color:#9ca3af; font-size:0.72rem; margin-bottom:12px; }}
#rzq-code {{
    font-size:1.3rem; font-weight:900; color:#fff; letter-spacing:3px;
    background:#0a0a0a; border:2px solid #f59e0b; border-radius:10px;
    padding:11px; text-align:center; font-family:monospace;
    margin-bottom:10px; cursor:pointer; user-select:all;
}}
#rzq-btn  {{
    width:100%; padding:9px; border:none; border-radius:10px;
    background:linear-gradient(135deg,#f59e0b,#d97706);
    color:#000; font-weight:800; cursor:pointer; font-size:0.88rem;
    margin-bottom:8px;
}}
#rzq-foot {{ color:#6b7280; font-size:0.7rem; text-align:center; }}
</style>
<div id="rzq-popup">
  <div id="rzq-lbl">🎉 Payment Confirmed!</div>
  <div id="rzq-sub">Your unique Pro access code:</div>
  <div id="rzq-code" title="Click to copy">{_found_code}</div>
  <button id="rzq-btn" onclick="navigator.clipboard.writeText('{_found_code}');this.textContent='✅ Copied to clipboard!'">📋 Copy Code</button>
  <div id="rzq-foot">Closes in <span id="rzq-t">30</span>s &nbsp;·&nbsp; code also shown below</div>
</div>
<script>
(function(){{
  var s=30,el=document.getElementById('rzq-t'),p=document.getElementById('rzq-popup');
  var iv=setInterval(function(){{
    s--;if(el)el.textContent=s;
    if(s<=0){{clearInterval(iv);if(p)p.style.display='none';}}
  }},1000);
}})();
</script>
<div style="background:linear-gradient(135deg,#1a0800,#0d0d0d);border:2px solid #f59e0b;
border-radius:14px;padding:18px 22px;text-align:center;margin:14px 0 4px;">
  <div style="color:#9ca3af;font-size:0.75rem;margin-bottom:6px;letter-spacing:1px;">YOUR PRO ACCESS CODE</div>
  <div style="font-size:1.7rem;font-weight:900;color:#f59e0b;letter-spacing:4px;font-family:monospace;">{_found_code}</div>
  <div style="color:#6b7280;font-size:0.72rem;margin-top:6px;">↓ Paste in the field below and click Unlock Pro</div>
</div>
""", unsafe_allow_html=True)

            # ── Show payment link + "I've Paid" button ───────────────────
            else:
                st.success("✅ Your personal payment link is ready!")
                st.markdown(
                    f'<a href="{_pay_url}" target="_blank" '
                    f'style="display:block;text-align:center;'
                    f'background:linear-gradient(135deg,#f59e0b,#d97706);'
                    f'color:#000;font-weight:800;font-size:1rem;padding:14px 24px;'
                    f'border-radius:30px;text-decoration:none;'
                    f'box-shadow:0 6px 24px rgba(245,158,11,0.4);margin:12px 0;">'
                    f'💳 Pay ₹79 — Open Payment Page →</a>',
                    unsafe_allow_html=True,
                )
                st.info(f"⚠️ **Important:** When Razorpay asks for your email, enter **{_saved_email}** (same as above) so we can match your payment and show your code.")
                st.caption("After paying, click the button below — your unique code appears on screen instantly!")

                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("✅ I've Paid — Show My Code!", key=f"_wall_paid_{_key}", use_container_width=True):
                        _found = False
                        if WEBHOOK_SERVER_URL:
                            try:
                                import requests as _req
                                _r = _req.get(
                                    f"{WEBHOOK_SERVER_URL}/get-code",
                                    params={"email": _saved_email},
                                    timeout=10,
                                )
                                if _r.status_code == 200 and _r.json().get("found"):
                                    st.session_state[_code_key] = _r.json()["code"]
                                    _found = True
                            except Exception:
                                pass
                        if _found:
                            st.rerun()
                        else:
                            st.warning("⏳ Payment still processing — wait ~10 seconds and try again.")
                with col2:
                    if st.button("🔄 Reset", key=f"_wall_regen_{_key}"):
                        del st.session_state[_link_key]
                        st.rerun()

        # ── STEP 3: Enter access code ────────────────────────────────────────
        st.divider()
        st.markdown('<div class="unlock-strip-label">Step 2 (after paying) · Enter your access code</div>',
                    unsafe_allow_html=True)
        _prefill = st.session_state.get(f"_found_code_{_key}", "")
        _code = st.text_input(
            "🔑 Access Code",
            value=_prefill,
            placeholder="e.g. RIQ-A1B2-C3D4-E5F6",
            key=f"_wall_code_{_key}",
            help="Code appears on screen after payment — or check your email."
        )
        if st.button("🔓 Unlock Pro", key=f"_wall_btn_{_key}", use_container_width=True):
            if _validate_pro_code(_code):
                st.session_state.is_pro = True
                st.rerun()
            else:
                st.error("❌ Invalid code. Double-check or contact support.")


# ═══════════════════════════════════════════════════════════════════════════════
# 🙋  RESUME HELP REQUEST PAGE
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🙋 Resume Help":

    st.markdown("""
    <style>
    .help-hero {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 50%, #1a1a2e 100%);
        border: 1px solid rgba(100,180,255,0.2);
        border-radius: 18px;
        padding: 32px 36px;
        margin-bottom: 24px;
        text-align: center;
    }
    .help-hero h2 { color: #e2eaf8; font-size: 1.7rem; margin-bottom: 8px; }
    .help-hero p  { color: #8eb8f0; font-size: 1rem; line-height: 1.6; margin: 0; }
    .help-step {
        background: #161b22;
        border: 1px solid rgba(100,180,255,0.12);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
    }
    .help-step .icon { font-size: 2rem; margin-bottom: 8px; }
    .help-step .title { color: #e2eaf8; font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; }
    .help-step .desc  { color: #8eb8f0; font-size: 0.82rem; line-height: 1.4; }
    .open-btn {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        font-weight: 700;
        font-size: 1rem;
        padding: 12px 32px;
        border-radius: 30px;
        text-decoration: none !important;
        box-shadow: 0 4px 20px rgba(102,126,234,0.4);
        transition: box-shadow 0.2s;
    }
    .open-btn:hover { box-shadow: 0 6px 28px rgba(102,126,234,0.65); }
    </style>
    """, unsafe_allow_html=True)

    # Hero banner
    st.markdown("""
    <div class="help-hero">
      <h2>🙋 Free Resume Review Service</h2>
      <p>
        Not sure how to build your resume? Fill out the form below — share your current resume
        and any suggestions, and I'll personally review it, improve it, and send it back to you.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # How it works — 3 steps
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("""
        <div class="help-step">
          <div class="icon">📝</div>
          <div class="title">Step 1 — Fill the Form</div>
          <div class="desc">Enter your name, roll number, WhatsApp number, upload your resume PDF and add any suggestions.</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="help-step">
          <div class="icon">🔍</div>
          <div class="title">Step 2 — We Review It</div>
          <div class="desc">Your resume will be carefully reviewed, improved for ATS and recruiter standards.</div>
        </div>""", unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="help-step">
          <div class="icon">📲</div>
          <div class="title">Step 3 — Get It Back</div>
          <div class="desc">Your upgraded resume is sent back to you on WhatsApp — ready to apply!</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # Open in new tab button (centered)
    st.markdown("""
    <div style="text-align:center; margin: 16px 0 28px;">
      <a class="open-btn" href="https://docs.google.com/forms/d/e/1FAIpQLSemc5ETP_xfPMbBK6genuziHDDJZRvjrsRzJz2vHZGlxw2Fhg/viewform?usp=header"
         target="_blank">🔗 Open Form in New Tab</a>
    </div>
    """, unsafe_allow_html=True)



    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯  CAREER TOOLS PAGE
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🎯 Career Tools":

    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .ct-qcard {
        background: #1a1a2e;
        border-left: 3px solid #3498db;
        padding: 10px 16px;
        margin: 6px 0;
        border-radius: 0 10px 10px 0;
        color: #e2eaf8;
        font-size: 0.93rem;
        line-height: 1.5;
    }
    .ct-outbox {
        background: #0d1117;
        border: 1px solid rgba(100,180,255,0.2);
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 10px;
    }
    .ct-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #64b5f6;
        margin-bottom: 6px;
    }
    .ct-subject {
        font-size: 0.85rem;
        color: #8eb8f0;
        margin-bottom: 10px;
    }
    .tracker-row {
        background: #161b22;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    .stage-pill {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎯 Career Tools")
    st.markdown('<p style="color:#8eb8f0;font-size:0.95rem;margin-bottom:1.5rem;">Cover letters &amp; tracking are free. Pro tools unlock interview prep and outreach.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["✉️ Cover Letter  🆓", "📋 Application Tracker  🆓", "🎤 Interview Predictor  🔒", "📨 Cold Outreach  🔒"])

    # ── TAB 1: Cover Letter Generator (FREE) ─────────────────────────────────
    with tab1:
        st.markdown('<span class="badge-free">Free</span>', unsafe_allow_html=True)
        st.subheader("✉️ Cover Letter Generator")
        st.write("Auto-draft a personalized, ATS-friendly cover letter from your resume + job description.")
        cl_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="cl_resume")
        c1, c2, c3 = st.columns(3)
        with c1: cl_name    = st.text_input("Your Full Name", key="cl_name")
        with c2: cl_company = st.text_input("Target Company", key="cl_company")
        with c3: cl_role    = st.text_input("Target Role",    key="cl_role")
        cl_jd   = st.text_area("Job Description", height=150, key="cl_jd")
        cl_tone = st.radio("Tone", ["Professional", "Enthusiastic", "Concise"], horizontal=True, key="cl_tone")

        if st.button("Generate Cover Letter ✉️", key="cl_btn"):
            if not all([cl_resume, cl_jd.strip(), cl_name.strip(), cl_company.strip(), cl_role.strip()]):
                st.error("Please fill in all fields and upload your resume.")
            else:
                with st.spinner("Crafting your personalized cover letter..."):
                    cl_text = extract_text_from_pdf(cl_resume)
                    from utils.cover_letter import generate_cover_letter
                    st.session_state["cl_result"] = generate_cover_letter(cl_text, cl_jd, cl_name, cl_company, cl_role, cl_tone)

        if "cl_result" in st.session_state:
            res = st.session_state["cl_result"]
            if "error" in res:
                st.error(f"❌ {res['error']}")
            else:
                st.divider()
                st.success(f"✅ Cover letter ready! ({res['word_count']} words) — Select all inside the box and copy.")
                st.text_area("📄 Your Cover Letter", value=res["cover_letter"], height=380, key="cl_display")

    # ── TAB 2: Application Tracker (FREE basic) ───────────────────────────────
    with tab2:
        from utils.app_tracker import (load_applications, add_application,
                                       update_stage, delete_application, get_stats, STAGES)
        st.markdown('<span class="badge-free">Free</span>', unsafe_allow_html=True)
        st.subheader("📋 Application Tracker")
        st.write("Track every application — stage-by-stage. Saved to disk, persists across sessions.")

        apps = load_applications()
        stats = get_stats(apps)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📨 Total Applied",   stats["total"])
        m2.metric("✅ Shortlisted",      stats["by_stage"].get("Shortlisted", 0) + stats["by_stage"].get("Interview", 0))
        m3.metric("🏆 Offer Rate",       f"{stats['offer_rate']}%")
        m4.metric("🌟 Best Resume Ver.", f"{stats['best_resume']} ({stats['best_rate']}%)" if stats['best_resume'] != 'N/A' else "N/A")

        st.divider()

        with st.expander("➕ Add New Application", expanded=(len(apps) == 0)):
            with st.form("add_app_form"):
                fa1, fa2 = st.columns(2)
                with fa1:
                    new_company = st.text_input("Company *")
                    new_role    = st.text_input("Role / Position *")
                with fa2:
                    new_version = st.text_input("Resume Version (e.g. v1, v2, 'FAANG')")
                    new_date    = st.date_input("Date Applied")
                new_stage = st.selectbox("Current Stage", STAGES)
                submitted = st.form_submit_button("Add Application ➕")
                if submitted:
                    if not new_company.strip() or not new_role.strip():
                        st.error("Company and Role are required.")
                    else:
                        add_application(new_company.strip(), new_role.strip(),
                                        new_version.strip() or "v1",
                                        str(new_date), new_stage)
                        st.success(f"✅ Added {new_company} — {new_role}")
                        st.rerun()

        st.divider()
        if not apps:
            st.info("No applications tracked yet. Add your first one above!")
        else:
            st.markdown(f"**Your Applications ({len(apps)})**")
            stage_colors = {
                "Applied":     "#3498db",
                "Shortlisted": "#f39c12",
                "Interview":   "#9b59b6",
                "Offer":       "#1db954",
                "Rejected":    "#e74c3c",
            }
            for app in reversed(apps):
                sc = stage_colors.get(app["stage"], "#888")
                with st.container():
                    r1, r2, r3, r4 = st.columns([3, 2, 2, 1])
                    with r1:
                        st.markdown(f"**{app['company']}** · {app['role']}")
                        st.caption(f"Resume: `{app['resume_version']}` · Applied: {app['date_applied']}")
                    with r2:
                        new_s = st.selectbox("Stage", STAGES,
                                             index=STAGES.index(app["stage"]),
                                             key=f"st_{app['id']}",
                                             label_visibility="collapsed")
                        if new_s != app["stage"]:
                            update_stage(app["id"], new_s)
                            st.rerun()
                    with r3:
                        st.markdown(
                            f'<span class="stage-pill" style="background:{sc}20;color:{sc};border:1px solid {sc}40;">'
                            f'● {app["stage"]}</span>',
                            unsafe_allow_html=True
                        )
                    with r4:
                        if st.button("🗑️", key=f"del_{app['id']}", help="Delete"):
                            delete_application(app["id"])
                            st.rerun()
                    st.write("")

    # ── TAB 3: Interview Predictor (🔒 PRO) ──────────────────────────────────
    with tab3:
        st.markdown('<span class="badge-pro">Pro</span>', unsafe_allow_html=True)
        st.subheader("🎤 Interview Question Predictor")
        if not st.session_state.is_pro:
            pro_wall("Interview Predictor", [
                "AI-generated behavioral, technical & role-specific questions",
                "Personalized to your resume background",
                "Company-specific questions when JD is provided",
                "Practice-ready format with Q-by-Q breakdown",
            ])
        else:
            st.write("Upload your resume to generate likely interview questions specific to your background and target role.")
            iq_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="iq_resume")
            iq_jd = st.text_area("Job Description (optional — unlocks company & role-specific questions)", height=120, key="iq_jd")
            if st.button("Generate Questions 🎤", key="iq_btn"):
                if not iq_resume:
                    st.error("Please upload your resume.")
                else:
                    with st.spinner("Analyzing your profile and predicting questions..."):
                        iq_text = extract_text_from_pdf(iq_resume)
                        from utils.interview_prep import predict_interview_questions
                        st.session_state["iq_result"] = predict_interview_questions(iq_text, iq_jd)
            if "iq_result" in st.session_state:
                res = st.session_state["iq_result"]
                if "error" in res:
                    st.error(f"❌ {res['error']}")
                else:
                    st.divider()
                    st.success("✅ Questions ready — use these to practice before your interview.")
                    cats = [
                        ("behavioral",       "🧠 Behavioral",       "#e74c3c"),
                        ("technical",        "⚙️ Technical",        "#3498db"),
                        ("role_specific",    "🎯 Role-Specific",    "#2ecc71"),
                        ("company_specific", "🏢 Company-Specific", "#f39c12"),
                    ]
                    for key, label, color in cats:
                        qs = res.get(key, [])
                        if qs:
                            st.markdown(f"**{label}**")
                            for i, q in enumerate(qs, 1):
                                st.markdown(
                                    f'<div class="ct-qcard" style="border-left-color:{color};">'
                                    f'<span style="color:#888;font-size:0.75rem;">Q{i}</span><br>{q}</div>',
                                    unsafe_allow_html=True
                                )
                            st.write("")

    # ── TAB 4: Cold Outreach Writer (🔒 PRO) ─────────────────────────────────
    with tab4:
        st.markdown('<span class="badge-pro">Pro</span>', unsafe_allow_html=True)
        st.subheader("📨 Cold Outreach Writer")
        if not st.session_state.is_pro:
            pro_wall("Cold Email & LinkedIn Outreach Generator", [
                "Personalized cold emails drafted from your resume",
                "LinkedIn connection messages (≤80 words, high-reply rate)",
                "Tailored for Recruiter, Alumni, Referral or Hiring Manager",
                "Written to actually get responses — not generic templates",
            ])
        else:
            st.write("Generate cold emails and LinkedIn messages personalized from your resume — written to actually get replies.")
            co_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="co_resume")
            c1, c2, c3 = st.columns(3)
            with c1: co_company = st.text_input("Target Company", key="co_company")
            with c2: co_role    = st.text_input("Target Role",    key="co_role")
            with c3: co_ptype   = st.selectbox("Writing to...", ["Recruiter", "Alumni", "Referral", "Hiring Manager"], key="co_ptype")
            co_pname = st.text_input("Their Name (optional — makes it more personal)", key="co_pname")
            if st.button("Generate Outreach 📨", key="co_btn"):
                if not all([co_resume, co_company.strip(), co_role.strip()]):
                    st.error("Please upload resume and fill in company + role.")
                else:
                    with st.spinner("Writing your outreach messages..."):
                        co_text = extract_text_from_pdf(co_resume)
                        from utils.cold_outreach import generate_outreach
                        st.session_state["co_result"] = generate_outreach(co_text, co_company, co_role, co_ptype, co_pname)
            if "co_result" in st.session_state:
                res = st.session_state["co_result"]
                if "error" in res:
                    st.error(f"❌ {res['error']}")
                else:
                    st.divider()
                    st.success("✅ Outreach messages ready!")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown('<div class="ct-label">📧 Cold Email</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="ct-subject">Subject: <b>{res.get("email_subject","")}</b></div>', unsafe_allow_html=True)
                        st.text_area("Email body — select all to copy", value=res.get("email_body",""), height=220, key="co_email_display")
                    with col_b:
                        st.markdown('<div class="ct-label">🔗 LinkedIn Message</div>', unsafe_allow_html=True)
                        st.markdown('<div class="ct-subject">Connection request note (≤80 words)</div>', unsafe_allow_html=True)
                        st.text_area("LinkedIn message — select all to copy", value=res.get("linkedin_message",""), height=220, key="co_li_display")

    st.stop()



if page == "⚖️ A/B Testing Engine":

    st.title("⚖️ Resume A/B Testing Engine")
    st.markdown('<span class="badge-pro">Pro</span>', unsafe_allow_html=True)
    st.write("Mathematically compare two resume versions against a job description — data-driven winner selection.")

    if not st.session_state.is_pro:
        pro_wall("A/B Testing Engine", [
            "Upload Resume A vs Resume B — AI picks the winner",
            "Full ATS format score + semantic JD alignment comparison",
            "Expert LLM verdict with key difference breakdown",
            "Recruiter-perspective summary on which resume to submit",
        ])
    else:
        col1, col2 = st.columns(2)
        with col1:
            res_a_file = st.file_uploader("Upload Resume A (PDF)", type=["pdf"], key="res_a")
        with col2:
            res_b_file = st.file_uploader("Upload Resume B (PDF)", type=["pdf"], key="res_b")

        jd_ab = st.text_area("Paste Target Job Description", key="jd_ab", height=150)

        if st.button("Compare Resumes ⚖️"):
            if not res_a_file or not res_b_file or not jd_ab:
                st.error("Please upload both resumes and provide a job description.")
            else:
                with st.spinner("Analyzing structures and querying LLM for Recruiter Feedback..."):
                    text_a = extract_text_from_pdf(res_a_file)
                    text_b = extract_text_from_pdf(res_b_file)
                    score_a, ats_data_a = real_ats_score(text_a)
                    score_b, ats_data_b = real_ats_score(text_b)
                    from utils.jd_file import model, split_text, cosine_similarity
                    import numpy as np

                    def get_jd_score(res_txt, jd_txt):
                        r_chunks = split_text(res_txt)
                        j_chunks = split_text(jd_txt)
                        if not r_chunks or not j_chunks:
                            return 0
                        r_emb = model.encode(r_chunks)
                        j_emb = model.encode(j_chunks)
                        sim = cosine_similarity(np.mean(r_emb, axis=0), np.mean(j_emb, axis=0))
                        return min(max(0, float(sim) * 100), 100)

                    jd_a = get_jd_score(text_a, jd_ab)
                    jd_b = get_jd_score(text_b, jd_ab)
                    overall_a = (score_a * 0.4) + (jd_a * 0.6)
                    overall_b = (score_b * 0.4) + (jd_b * 0.6)

                    st.divider()
                    st.subheader("🔢 Quantitative Comparison")
                    colA, colB = st.columns(2)
                    with colA:
                        st.write("### Resume A")
                        st.metric("Overall ATS Match", f"{overall_a:.1f}/100")
                        st.caption(f"Format Score: {score_a}/100 | Semantic Alignment: {jd_a:.1f}%")
                    with colB:
                        st.write("### Resume B")
                        st.metric("Overall ATS Match", f"{overall_b:.1f}/100")
                        st.caption(f"Format Score: {score_b}/100 | Semantic Alignment: {jd_b:.1f}%")

                    st.divider()
                    st.subheader("🤖 Expert LLM Verdict")
                    from utils.ab_testing import compare_resumes_llm
                    feedback = compare_resumes_llm(text_a, text_b, jd_ab)
                    if "error" in feedback:
                        st.error(f"Error calling AI Evaluator: {feedback['error']}")
                    else:
                        winner = feedback.get("winner", "Unknown")
                        if winner in ("Resume A", "Resume B"):
                            st.success(f"🏆 Ultimate Winner: **{winner}**")
                        else:
                            st.warning(f"🤝 Result: **{winner}**")
                        st.write("### Key Comparative Advantages:")
                        for diff in feedback.get("key_differences", []):
                            st.write(f"- {diff}")
                        st.write("### Recruiter Summary View:")
                        st.info(feedback.get("final_verdict", ""))

    st.stop()

st.title("Single Resume Analyzer")
st.write("Real ATS Scoring + Smart Resume Feedback")

# ---------------- PROFILE ----------------
profiles = list(SKILLS_DB.keys())
selected_profile = st.selectbox("Select Target Role", profiles)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

# ---------------- MAIN ----------------
if uploaded_file:

    resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text.strip():
        st.error("❌ Could not extract text")
        st.stop()

    # -------- BASIC INFO --------
    name, roll_number, college = extract_basic_info(resume_text)

    st.subheader("Candidate Details")

    col1, col2, col3 = st.columns(3)
    col1.write(f"**Name:** {name}")
    col2.write(f"**Roll No:** {roll_number}")
    col3.write(f"**College:** {college}")

    st.divider()

    # -------- SKILLS — FREE --------
    present, missing, exact = extract_skills(resume_text, selected_profile, SKILLS_DB)

    st.markdown('<span class="badge-free">Free</span>', unsafe_allow_html=True)
    st.subheader("🧩 Skills Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("✅ Skills Found")
        st.write(", ".join(exact) if exact else "None")

    with col2:
        st.write("❌ Missing Skills")
        st.write(", ".join(missing) if missing else "None")

    st.divider()

    # -------- REAL ATS — FREE --------
    st.markdown('<span class="badge-free">Free</span>', unsafe_allow_html=True)
    st.subheader("🤖 ATS Score")

    score, ats_data = real_ats_score(resume_text)

    st.metric("Overall ATS Parseability", f"{score}/100")

    if score > 80:
        st.success("🔥 Excellent Formatting")
    elif score > 60:
        st.warning("⚡ Good Formatting")
    else:
        st.error("🚨 Needs Formatting Improvement")

    st.divider()

    # -------- PLACEMENT PROBABILITY — 🔒 PRO --------
    st.markdown('<span class="badge-pro">Pro</span>', unsafe_allow_html=True)
    st.subheader("🎯 Placement Probability Engine")
    if not st.session_state.is_pro:
        pro_wall("Placement Probability Predictor", [
            "Predicts your % chance of getting shortlisted",
            "Recruiter-grade benchmark modeling (vs 1000s of applicants)",
            "Applicant Tier rating (Top 10%, Average, Below Average)",
            "Market Benchmark progress bar with insight",
        ])
    else:
        from utils.placement import calculate_placement_probability
        skill_match_percentage = (len(exact) / max(1, len(exact) + len(missing))) * 100
        impact_res = impact_score(resume_text)
        prob_data = calculate_placement_probability(score, skill_match_percentage, impact_res)
        p_val = prob_data["probability"]
        c1, c2, c3 = st.columns([1, 1.2, 1.2])
        with c1:
            st.metric("Shortlist Probability", f"{p_val}%", delta=f"{p_val - 45.0:.1f}% vs Average")
        with c2:
            st.metric("Applicant Tier", prob_data["tier"])
        with c3:
            st.info(f"💡 {prob_data['insight']}")
        st.write("### Market Benchmark Comparison")
        st.progress(int(p_val))
        st.caption(f"**Your Score:** {p_val}% | **Average Applicant:** ~45% | **Top 10% Cutoff:** ~85%")

    st.divider()

    # -------- SMART SUGGESTIONS — 🔒 PRO --------
    st.markdown('<span class="badge-pro">Pro</span>', unsafe_allow_html=True)
    st.subheader("💡 Smart Suggestions (Resume Worded AI)")
    if not st.session_state.is_pro:
        pro_wall("AI-Powered Resume Suggestions", [
            "Line-by-line feedback on every bullet point",
            "Confidence-scored issue detection",
            "Side-by-side original vs improved suggestions",
            "Personalized to your target role",
        ])
    else:
        with st.spinner("Analyzing resume for targeted improvements..."):
            from utils.smart_suggestions import get_line_level_suggestions
            suggestions_list = get_line_level_suggestions(resume_text)
        if suggestions_list:
            if "error" in suggestions_list[0]:
                st.error(f"❌ Smart Suggestions Error: {suggestions_list[0]['error']}")
            else:
                for idx, sug in enumerate(suggestions_list):
                    with st.expander(f"⚠️ Issue: {sug.get('issue', 'Needs Improvement')} (Confidence: {sug.get('confidence_score', 0)})"):
                        st.write("**Original Line:**")
                        st.error(sug.get('original_line'))
                        st.write("**Suggested Improvement:**")
                        st.success(sug.get('improved_suggestion'))
        else:
            st.info("No major line-level issues found! Your resume bullets look strong.")

    st.divider()

    # -------- AI RESUME REWRITER — 🔒 PRO --------
    st.markdown('<span class="badge-pro">Pro</span>', unsafe_allow_html=True)
    st.subheader("✨ AI Resume Rewriter")
    if not st.session_state.is_pro:
        pro_wall("AI Resume Rewriter", [
            "Select any bullet from your resume to instantly upgrade",
            "Basic Polish or Aggressive Transformation modes",
            "Before vs After comparison with ATS-optimized output",
            "AI feedback explaining every rewrite decision",
        ])
    else:
        with st.spinner("Intelligently scanning resume for lines to improve..."):
            from utils.bullet_extractor import extract_bullets_from_resume
            valid_bullets_raw = extract_bullets_from_resume(resume_text)
        valid_bullets = list(dict.fromkeys(valid_bullets_raw))
        options = ["📝 Type or paste a custom bullet point..."] + valid_bullets
        selected_option = st.selectbox("Select a bullet from your resume to enhance:", options)
        if selected_option == "📝 Type or paste a custom bullet point...":
            bullet_to_rewrite = st.text_area("Paste original bullet point:")
        else:
            bullet_to_rewrite = selected_option
        if bullet_to_rewrite:
            strength = st.radio("Rewrite Strength", ["Basic Polish", "Aggressive Transformation"], horizontal=True)
            if st.button("Rewrite Bullet 🚀"):
                with st.spinner("Analyzing and rewriting..."):
                    from utils.llm_rewriter import rewrite_bullet
                    result = rewrite_bullet(bullet_to_rewrite, selected_profile, strength)
                    if "error" in result:
                        st.error(f"Failed to generate rewrite: {result['error']}")
                    else:
                        st.success("Bullet Transformed Successfully!")
                        colA, colB = st.columns(2)
                        with colA:
                            st.subheader("🔴 Before")
                            st.error(bullet_to_rewrite)
                        with colB:
                            st.subheader("🟢 After (Optimized)")
                            st.success(result.get("rewritten_bullet", "Error: Missing response data"))
                        st.write("💡 **AI Feedback:**")
                        st.info(result.get("feedback_reason", "No feedback provided by model."))

    st.divider()

    # -------- JOB MATCH — FREE --------
    st.markdown('<span class="badge-free">Free</span>', unsafe_allow_html=True)
    st.subheader("📄 Job Match")

    jd = st.text_area("Paste Job Description")

    if jd:
        final_score, semantic_score, skill_score = jd_match_final(
            resume_text, jd, present, missing
        )

        st.metric("🎯 Match Score", f"{final_score:.2f}/100")

        st.write(f"🤖 Semantic Match: {semantic_score:.2f}%")
        st.write(f"🧠 Skill Match: {skill_score:.2f}%")

