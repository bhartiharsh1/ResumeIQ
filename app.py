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
try:
    import jwt as _pyjwt
except ImportError:
    _pyjwt = None
try:
    from streamlit_oauth import OAuth2Component as _OAuth2Component
except ImportError:
    _OAuth2Component = None
from utils.pdf_parser import extract_text_from_pdf
from utils.skills import extract_skills
from utils.info_extractor import extract_basic_info
from utils.jd_file import jd_match_final
from utils.ats_ai import real_ats_score
from utils.advanced_ats import impact_score
from data.skills_db import SKILLS_DB
# ---------------- CONFIG ----------------
st.set_page_config(page_title="ResumeIQ Platform", layout="wide", page_icon="🧠")

# ── GOOGLE OAUTH CONFIG ───────────────────────────────────────────────────────────────────────
try:
    _GOOGLE_CLIENT_ID     = st.secrets.get("GOOGLE_CLIENT_ID", "")
    _GOOGLE_CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET", "")
    _APP_URL              = st.secrets.get("APP_URL", "https://resumeiq-a3qrgwduuavjp79pqbsbvb.streamlit.app/")

except Exception:
    _GOOGLE_CLIENT_ID = _GOOGLE_CLIENT_SECRET = _APP_URL = ""

_OAUTH_READY = bool(_GOOGLE_CLIENT_ID and _GOOGLE_CLIENT_SECRET and _OAuth2Component)

# ── GLOBAL 3D THEME ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');


/* ── Base font ── */
body { font-family: 'Outfit', sans-serif; }

/* ── Deep-space gradient background ── */
.stApp {
    background-color: #050810 !important;
    background-image:
        radial-gradient(circle at 10% 20%, rgba(99,102,241,0.12) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(139,92,246,0.12) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(6,182,212,0.08) 0%, transparent 60%);
}

/* ── Sidebar — frosted-glass 3D panel ── */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 26, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    box-shadow: 10px 0 30px rgba(0,0,0,0.5) !important;
}
section[data-testid="stSidebar"] * { color: #d1d5db !important; }
section[data-testid="stSidebar"] .stRadio label:hover { color: #a78bfa !important; text-shadow: 0 0 8px rgba(167,139,250,0.4); }

/* ── Animated gradient headings ── */
h1 {
    background: linear-gradient(to right, #667eea, #a78bfa, #06b6d4, #667eea);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900 !important;
    letter-spacing: -1px !important;
    filter: drop-shadow(0 4px 12px rgba(102,126,234,0.4));
    animation: shine 4s linear infinite;
}
@keyframes shine {
    to { background-position: 200% center; }
}

h2, h3 {
    background: linear-gradient(135deg, #f3f4f6 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}

/* ── 3D Buttons with Glow ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 12px 28px !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4), inset 0 2px 0 rgba(255,255,255,0.2) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    text-transform: uppercase;
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 15px 35px rgba(139,92,246,0.6), inset 0 2px 0 rgba(255,255,255,0.3) !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
}

/* ── Glass Metric cards ── */
[data-testid="metric-container"] {
    background: rgba(20, 25, 40, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    transition: all 0.3s ease !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 15px 40px rgba(99,102,241,0.2) !important;
}
[data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #06b6d4, #3b82f6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important;
    font-size: 2.4rem !important;
    letter-spacing: -1px !important;
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
    background: rgba(15, 20, 30, 0.6) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #f3f4f6 !important;
    font-size: 1rem !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    background: rgba(20, 25, 40, 0.8) !important;
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.2), inset 0 2px 4px rgba(0,0,0,0.2) !important;
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
    background: linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6) !important;
    background-size: 200% auto !important;
    animation: shine 2s linear infinite !important;
    border-radius: 8px !important;
    box-shadow: 0 0 15px rgba(59,130,246,0.5) !important;
}

/* ── Alerts — Glass Panels ── */
div[data-testid="stSuccessMessage"], .stSuccess {
    background: rgba(16,185,129,0.1) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(16,185,129,0.2) !important;
    border-left: 5px solid #10b981 !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
    color: #d1fae5 !important;
}
div[data-testid="stErrorMessage"], .stError {
    background: rgba(239,68,68,0.1) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    border-left: 5px solid #ef4444 !important;
    border-radius: 12px !important;
    color: #fee2e2 !important;
}
div[data-testid="stWarningMessage"], .stWarning {
    background: rgba(245,158,11,0.1) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(245,158,11,0.2) !important;
    border-left: 5px solid #f59e0b !important;
    border-radius: 12px !important;
    color: #fef3c7 !important;
}
div[data-testid="stInfoMessage"], .stInfo {
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

# ── GOOGLE LOGIN GATE ───────────────────────────────────────────────────────────────────────
if _OAUTH_READY and "user_email" not in st.session_state:
    st.markdown("""
<div style="max-width:460px;margin:80px auto;text-align:center;">
  <div style="font-size:3.5rem;margin-bottom:16px">🧠</div>
  <h1 style="background:linear-gradient(135deg,#667eea,#a78bfa);-webkit-background-clip:text;
             -webkit-text-fill-color:transparent;font-size:2rem;margin-bottom:8px;">ResumeIQ</h1>
  <p style="color:#9ca3af;font-size:0.95rem;margin-bottom:32px;">Sign in to access AI-powered resume tools.</p>
</div>
""", unsafe_allow_html=True)
    _login_col = st.columns([1, 2, 1])[1]
    with _login_col:
        _oauth2 = _OAuth2Component(
            _GOOGLE_CLIENT_ID, _GOOGLE_CLIENT_SECRET,
            "https://accounts.google.com/o/oauth2/auth",
            "https://oauth2.googleapis.com/token",
            "https://oauth2.googleapis.com/token",
            # Google's revoke endpoint doesn't support the httpx_oauth auth method
            # — omit it to avoid MissingRevokeTokenAuthMethodError
        )
        _result = _oauth2.authorize_button(
            name="🔑  Sign in with Google",
            redirect_uri=_APP_URL,
            scope="openid email profile",
            key="google_login",
            extras_params={"prompt": "select_account"},
            use_container_width=True,
        )
        if _result and "token" in _result:
            _tok = _result["token"]
            try:
                _claims = _pyjwt.decode(
                    _tok.get("id_token", ""),
                    options={"verify_signature": False}
                )
                st.session_state.user_email = _claims.get("email", "")
                st.session_state.user_name  = _claims.get("name",  "")
                st.session_state.user_pic   = _claims.get("picture", "")
            except Exception:
                st.session_state.user_email = ""
            st.rerun()
    st.stop()

# ── User info (populated after login, or empty if OAuth not configured) ──────────────────
_USER_EMAIL = st.session_state.get("user_email", "")
_USER_NAME  = st.session_state.get("user_name",  "Guest")

def check_premium_access(action_name):
    """
    Checks if the user has an active, unexpired premium access code.
    If not, removes pro status, shows error, and returns False.
    """
    from utils.access_codes import has_premium_access
    
    if has_premium_access(_USER_EMAIL):
        return True
        
    st.session_state.is_pro = False
    st.error(f"❌ Your 6-hour premium access has expired. Please purchase a new access code to continue using {action_name}.")
    return False

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["📊 Single Analyzer", "⚖️ A/B Testing Engine", "🎯 Career Tools", "🙋 Resume Help"])



# ── SIDEBAR: user avatar + pro status + sign out ──────────────────────────────────
st.sidebar.divider()
if _USER_EMAIL:
    _pic = st.session_state.get("user_pic", "")
    _avatar = (f'<img src="{_pic}" style="width:100%;height:100%;object-fit:cover;"/>'
               if _pic else
               f'<div style="width:100%;height:100%;background:linear-gradient(135deg,#667eea,#a78bfa);'
               f'display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;'
               f'font-size:1rem;">{_USER_NAME[:1].upper()}</div>')
    st.sidebar.markdown(
        f"""<div style='display:flex;align-items:center;gap:10px;padding:8px 4px;'>
          <div style='width:34px;height:34px;border-radius:50%;overflow:hidden;
                      border:2px solid rgba(99,102,241,0.5);flex-shrink:0;'>{_avatar}</div>
          <div style='overflow:hidden;'>
            <div style='color:#e2eaf8;font-weight:700;font-size:0.84rem;white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis;'>{_USER_NAME}</div>
            <div style='color:#6b7280;font-size:0.72rem;white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis;'>{_USER_EMAIL}</div>
          </div></div>""",
        unsafe_allow_html=True,
    )
if _USER_EMAIL:
    if st.sidebar.button("🚪 Sign Out", key="_signout_btn", use_container_width=True):
        for _k in ["user_email", "user_name", "user_pic", "is_pro"]:
            st.session_state.pop(_k, None)
        st.rerun()

    if st.session_state.get("is_pro", False):
        from utils.access_codes import get_premium_expiry
        expiry_ts = get_premium_expiry(_USER_EMAIL)
        import time
        if expiry_ts > time.time():
            import streamlit.components.v1 as components
            with st.sidebar:
                components.html(f'''
                <style>
                    body {{ margin: 0; padding: 0; font-family: 'Outfit', sans-serif; overflow: hidden; }}
                    @keyframes pulseGlow {{
                        0% {{ box-shadow: 0 0 15px rgba(16,185,129,0.2); }}
                        50% {{ box-shadow: 0 0 30px rgba(16,185,129,0.6); }}
                        100% {{ box-shadow: 0 0 15px rgba(16,185,129,0.2); }}
                    }}
                </style>
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 16px; padding: 20px; margin-top: 10px; text-align: center; backdrop-filter: blur(10px); animation: pulseGlow 3s infinite;">
                    <div style="color: #10b981; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; text-shadow: 0 0 10px rgba(16,185,129,0.5);">Premium Session</div>
                    <div id="countdown-timer" style="color: white; font-size: 2.2rem; font-weight: 900; font-family: monospace; text-shadow: 0 0 15px rgba(255,255,255,0.4); letter-spacing: 1px;">--:--:--</div>
                    <div style="color: rgba(255,255,255,0.6); font-size: 0.75rem; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">Unlimited Access Pass</div>
                </div>
                <script>
                    var countDownDate = {expiry_ts} * 1000;
                    var x = setInterval(function() {{
                        var now = new Date().getTime();
                        var distance = countDownDate - now;
                        if (distance < 0) {{
                            clearInterval(x);
                            document.getElementById("countdown-timer").innerHTML = "EXPIRED";
                        }} else {{
                            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
                            
                            var h = hours < 10 ? "0" + hours : hours;
                            var m = minutes < 10 ? "0" + minutes : minutes;
                            var s = seconds < 10 ? "0" + seconds : seconds;
                            
                            document.getElementById("countdown-timer").innerHTML = h + ":" + m + ":" + s;
                        }}
                    }}, 1000);
                </script>
                ''', height=130)
        else:
            st.session_state.is_pro = False
            st.rerun()



# ── FREEMIUM STATE ────────────────────────────────────────────────────────────
if _USER_EMAIL:
    from utils.access_codes import has_premium_access
    st.session_state.is_pro = has_premium_access(_USER_EMAIL)
elif "is_pro" not in st.session_state:
    st.session_state.is_pro = False

if "cover_letters_used" not in st.session_state:
    st.session_state.cover_letters_used = 0
if "job_matches_used" not in st.session_state:
    st.session_state.job_matches_used = 0

def pro_wall(feature_name, bullets):
    if st.session_state.get("is_pro", False):
        return False
    bullets_html = "".join([f"<li>{b}</li>" for b in bullets])
    _key = feature_name.lower().replace(" ", "_").replace("/", "")
    st.markdown(f'''
<style>
@keyframes rotateGradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
</style>
<div style="position:relative; padding: 3px; border-radius: 24px; background: linear-gradient(60deg, #f59e0b, #ef4444, #8b5cf6, #3b82f6, #10b981, #f59e0b); background-size: 300% 300%; animation: rotateGradient 6s ease infinite; margin-bottom:30px; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
<div style="background: rgba(10, 15, 26, 0.95); border-radius: 21px; padding: 35px; text-align: center; backdrop-filter: blur(20px);">
<div style="display:inline-block; padding:8px 16px; background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); border-radius:20px; color:#f59e0b; font-size:0.8rem; font-weight:800; letter-spacing:1px; text-transform:uppercase; margin-bottom:20px;">Premium Locked</div>
<h2 style="color:white; margin-bottom:12px; font-weight: 900; font-size: 2.2rem; letter-spacing:-0.5px;">{feature_name}</h2>
<ul style="text-align:left; color:#d1d5db; margin: 0 auto 30px auto; max-width: 80%; font-size: 1.05rem; line-height: 1.8;">
{bullets_html}
</ul>
<hr style="border:none; height:1px; background:linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); margin:30px 0;"/>
<h3 style="color:#10b981; margin-bottom:12px; font-weight:800; font-size: 1.8rem; text-shadow: 0 0 15px rgba(16,185,129,0.4);">🚀 Unlock The 6-Hour Pass (₹79)</h3>
<p style="color:#e2eaf8; font-size:1.1rem; margin-bottom:8px; font-weight:600;">Get unrestricted access to ALL premium tools instantly.</p>
<p style="color:#9ca3af; font-size:0.95rem; margin-bottom:25px; line-height:1.5;">After payment, you can use all premium features without limits during your session.<br/>A live countdown HUD will track your remaining time.<br/>Expires automatically when the timer ends.</p>
<div style="display:inline-block; padding: 6px; background: linear-gradient(135deg, #f59e0b, #ec4899); border-radius: 20px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(245,158,11,0.3);">
<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi%3A%2F%2Fpay%3Fpa%3Dbhartiharsh64-1%40oksbi%26pn%3DHarsh%2520Bharti%26am%3D79.00%26cu%3DINR" style="border-radius:14px; display:block;" alt="UPI QR"/>
</div>
<p style="color:#e2eaf8; margin:5px 0; font-size:1.1rem;">UPI ID: <b style="color:white; letter-spacing:1px;">bhartiharsh64-1@oksbi</b></p>
<p style="color:#9ca3af; font-size:0.9rem; margin-bottom:0; margin-top:15px; opacity:0.8;">🔒 Powered by AI Verification. Instant Activation.</p>
</div>
</div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### 📸 Verify Payment")
    payment_screenshot = st.file_uploader("Upload Payment Screenshot (JPG/PNG)", type=["png", "jpg", "jpeg"], key=f"img_{_key}")
    if payment_screenshot:
        if st.button("Verify Screenshot & Get Code 🔍", key=f"verify_{_key}", use_container_width=True):
            with st.spinner("AI is verifying your payment screenshot..."):
                import base64
                from utils.payment_verifier import verify_payment_screenshot
                
                base64_image = base64.b64encode(payment_screenshot.read()).decode("utf-8")
                res = verify_payment_screenshot(base64_image)
                
                if res.get("is_valid"):
                    from utils.access_codes import is_transaction_used, mark_transaction_used, generate_unique_code
                    tx_id = res.get("transaction_id", "").strip()
                    
                    if not tx_id:
                        st.warning("⚠️ Payment appears valid, but no unique transaction ID could be read. Please upload a clearer screenshot showing the UTR or Reference ID.")
                    elif is_transaction_used(tx_id):
                        st.error(f"❌ Verification Failed: This transaction ID ({tx_id}) has already been used.")
                    else:
                        st.success("✅ Payment Verified!")
                        mark_transaction_used(tx_id)
                        
                        # Generate a unique code bound to this email and persist it
                        new_code = generate_unique_code(_USER_EMAIL)
                        
                        st.markdown(f'''
                        <div style="background:linear-gradient(135deg, #10b981, #059669); border-radius:12px; padding:20px; text-align:center; margin: 20px 0; box-shadow: 0 4px 15px rgba(16,185,129,0.3);">
                            <h3 style="color:white; margin:0; font-size:1.2rem;">Your Unique Access Code:</h3>
                            <div style="font-size:2rem; font-weight:800; color:#fff; letter-spacing:2px; margin-top:10px; user-select:all;">{new_code}</div>
                            <p style="color:rgba(255,255,255,0.8); margin:10px 0 0 0; font-size:0.9rem;">Copy this code and paste it below to unlock your 6-hour unlimited pass.</p>
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Verification Failed: {res.get('reason', 'Invalid payment screenshot.')}")
    
    st.divider()

    c1, c2 = st.columns([3, 1])
    with c1:
        access_code = st.text_input("🔑 Enter Access Code:", type="password", key=f"code_{_key}")
    with c2:
        st.write("")
        st.write("")
        if st.button("Unlock 🔓", key=f"btn_{_key}", use_container_width=True):
            from utils.access_codes import validate_code
            if validate_code(access_code, _USER_EMAIL):
                st.session_state.is_pro = True
                st.rerun()
            else:
                st.error("❌ Invalid Code! It may belong to another account or has expired.")
    return True


# ── BADGE CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.badge-free {
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

    tab1, tab2, tab3, tab4 = st.tabs(["✉️ Cover Letter", "📋 Application Tracker", "🎤 Interview Predictor", "📨 Cold Outreach"])

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
                proceed = True
                if st.session_state.cover_letters_used >= 2:
                    if not st.session_state.is_pro:
                        if pro_wall("Unlimited Cover Letters", ["You have used your 2 free cover letters for this session.", "Upgrade to Pro to generate unlimited personalized cover letters."]):
                            proceed = False
                    else:
                        proceed = check_premium_access("Unlimited Cover Letters")
                        
                if proceed:
                    with st.spinner("Crafting your personalized cover letter..."):
                        cl_text = extract_text_from_pdf(cl_resume)
                        from utils.cover_letter import generate_cover_letter
                        st.session_state["cl_result"] = generate_cover_letter(cl_text, cl_jd, cl_name, cl_company, cl_role, cl_tone)
                        if not st.session_state.is_pro:
                            st.session_state.cover_letters_used += 1

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

    # ── TAB 3: Interview Predictor ───────────────────────────────────────────
    with tab3:
        st.subheader("🎤 Interview Question Predictor")
        if not st.session_state.is_pro:
            if pro_wall("Interview Predictor", ["AI-generated behavioral, technical & role-specific questions", "Personalized to your resume background", "Company-specific questions when JD is provided", "Practice-ready format with Q-by-Q breakdown"]):
                pass
        else:
            st.write("Upload your resume to generate likely interview questions specific to your background and target role.")
        iq_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="iq_resume")
        iq_jd = st.text_area("Job Description (optional — unlocks company & role-specific questions)", height=120, key="iq_jd")
        if st.button("Generate Questions 🎤", key="iq_btn"):
            if not iq_resume:
                st.error("Please upload your resume.")
            else:
                if check_premium_access("Interview Predictor"):
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

    # ── TAB 4: Cold Outreach Writer ───────────────────────────────────────────
    with tab4:
        st.subheader("📨 Cold Outreach Writer")
        if not st.session_state.is_pro:
            if pro_wall("Cold Email & LinkedIn Outreach Generator", ["Personalized cold emails drafted from your resume", "LinkedIn connection messages (≤80 words, high-reply rate)", "Tailored for Recruiter, Alumni, Referral or Hiring Manager", "Written to actually get responses — not generic templates"]):
                pass
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
                    if check_premium_access("Cold Outreach Writer"):
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
    st.write("Mathematically compare two resume versions against a job description — data-driven winner selection.")

    if not st.session_state.is_pro:
        if pro_wall("A/B Testing Engine", ["Upload Resume A vs Resume B — AI picks the winner", "Full ATS format score + semantic JD alignment comparison", "Expert LLM verdict with key difference breakdown", "Recruiter-perspective summary on which resume to submit"]):
            st.stop()

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
            if check_premium_access("A/B Testing Engine"):
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

if page == "📊 Single Analyzer":
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
        st.subheader("🎯 Placement Probability Engine")
        from utils.placement import calculate_placement_probability
        skill_match_percentage = (len(exact) / max(1, len(exact) + len(missing))) * 100
        impact_res = impact_score(resume_text)
        prob_data = calculate_placement_probability(score, skill_match_percentage, impact_res)
        p_val = prob_data["probability"]
        c1, c2, c3 = st.columns([1, 1.2, 1.2])
        with c1:
            st.metric("Shortlist Probability", f"{p_val}%", delta=f"{p_val - 45.0:.1f}% vs Average")
        
        if not st.session_state.is_pro:
            with c2:
                st.metric("Applicant Tier", "🔒 Pro")
            with c3:
                st.info("💡 Unlock Pro to see your specific applicant tier and actionable insight roadmap.")
        else:
            with c2:
                st.metric("Applicant Tier", prob_data["tier"])
            with c3:
                st.info(f"💡 {prob_data['insight']}")
        st.write("### Market Benchmark Comparison")
        st.progress(int(p_val))
        st.caption(f"**Your Score:** {p_val}% | **Average Applicant:** ~45% | **Top 10% Cutoff:** ~85%")

        st.divider()

        # -------- SMART SUGGESTIONS — 🔒 PRO --------
        st.subheader("💡 Smart Suggestions (Resume Worded AI)")
        with st.spinner("Analyzing resume for targeted improvements..."):
            from utils.smart_suggestions import get_line_level_suggestions
            suggestions_list = get_line_level_suggestions(resume_text)
        if suggestions_list:
            if "error" in suggestions_list[0]:
                st.error(f"❌ Smart Suggestions Error: {suggestions_list[0]['error']}")
            else:
                # Show only first 2 for free
                limit = len(suggestions_list) if st.session_state.is_pro else 2
                
                for idx, sug in enumerate(suggestions_list[:limit]):
                    with st.expander(f"⚠️ Issue: {sug.get('issue', 'Needs Improvement')} (Confidence: {sug.get('confidence_score', 0)})"):
                        st.write("**Original Line:**")
                        st.error(sug.get('original_line'))
                        st.write("**Suggested Improvement:**")
                        st.success(sug.get('improved_suggestion'))
                
                if not st.session_state.is_pro and len(suggestions_list) > 2:
                    st.warning(f"🔒 {len(suggestions_list) - 2} more advanced line-level suggestions are hidden.")
                    pro_wall("Advanced Smart Suggestions", ["Line-by-line feedback on every single bullet point", "Confidence-scored issue detection", "Side-by-side original vs improved suggestions", "Personalized to your target role"])
        else:
            st.info("No major line-level issues found! Your resume bullets look strong.")

        st.divider()

        # -------- AI RESUME REWRITER — 🔒 PRO --------
        st.subheader("✨ AI Resume Rewriter")
        if not st.session_state.is_pro:
            if pro_wall("AI Resume Rewriter", ["Select any bullet from your resume to instantly upgrade", "Basic Polish or Aggressive Transformation modes", "Before vs After comparison with ATS-optimized output", "AI feedback explaining every rewrite decision"]):
                pass
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
                    if check_premium_access("AI Resume Rewriter"):
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
        st.markdown('<span class="badge-free">Free (Limited)</span>', unsafe_allow_html=True)
        st.subheader("📄 Job Match")

        jd = st.text_area("Paste Job Description")

        if st.button("Calculate Job Match 🎯"):
            if jd:
                proceed = True
                if st.session_state.job_matches_used >= 1:
                    if not st.session_state.is_pro:
                        if pro_wall("Unlimited Job Matches", ["You have used your 1 free job match for this session.", "Upgrade to Pro to test your resume against unlimited job descriptions."]):
                            proceed = False
                    else:
                        proceed = check_premium_access("Unlimited Job Matches")
                        
                if proceed:
                    if not st.session_state.is_pro:
                        st.session_state.job_matches_used += 1
                    final_score, semantic_score, skill_score = jd_match_final(
                        resume_text, jd, present, missing
                    )

                    st.metric("🎯 Match Score", f"{final_score:.2f}/100")
                    
                    st.write(f"🤖 Semantic Match: {semantic_score:.2f}%")
                    st.write(f"🧠 Skill Match: {skill_score:.2f}%")
            else:
                st.error("Please paste a job description first.")

