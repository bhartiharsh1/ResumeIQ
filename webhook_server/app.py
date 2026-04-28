import os
import hmac
import hashlib
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
GMAIL_USER              = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD      = os.getenv("GMAIL_APP_PASSWORD", "")
SUPABASE_URL            = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY            = os.getenv("SUPABASE_KEY", "")
APP_URL                 = os.getenv("APP_URL", "https://resumeiq.streamlit.app")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def generate_code() -> str:
    """Generate a unique Pro access code like RIQ-A1B2-C3D4-E5F6."""
    chars = string.ascii_uppercase + string.digits
    parts = [''.join(random.choices(chars, k=4)) for _ in range(3)]
    return f"RIQ-{'-'.join(parts)}"


def send_email(to_email: str, code: str, customer_name: str) -> None:
    """Send the access code to the customer via Gmail SMTP."""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "🎉 Your ResumeIQ Pro Access Code is Here!"
    msg['From']    = f"ResumeIQ <{GMAIL_USER}>"
    msg['To']      = to_email

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#080c14;font-family:'Segoe UI',Arial,sans-serif;">
      <div style="max-width:580px;margin:40px auto;background:linear-gradient(135deg,#0f1520,#1a1030);
                  border:1px solid rgba(167,139,250,0.3);border-radius:20px;overflow:hidden;">

        <!-- Header -->
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:32px;text-align:center;">
          <h1 style="margin:0;color:#fff;font-size:1.8rem;letter-spacing:-0.5px;">🧠 ResumeIQ Pro</h1>
          <p style="margin:8px 0 0;color:rgba(255,255,255,0.85);font-size:0.95rem;">
            Your upgrade is confirmed ✅
          </p>
        </div>

        <!-- Body -->
        <div style="padding:36px 40px;">
          <p style="color:#c4c9d8;font-size:1rem;line-height:1.7;">
            Hi <strong style="color:#e2eaf8;">{customer_name}</strong>,<br><br>
            Thank you for upgrading to <strong style="color:#a78bfa;">ResumeIQ Pro</strong>!
            Your unique access code is below — enter it in the app to unlock
            <strong>all Pro features instantly</strong>.
          </p>

          <!-- Code Box -->
          <div style="background:#0d1117;border:2px solid #f59e0b;border-radius:14px;
                      padding:24px;text-align:center;margin:28px 0;">
            <p style="margin:0 0 8px;color:#9ca3af;font-size:0.78rem;letter-spacing:2px;text-transform:uppercase;">
              Your Access Code
            </p>
            <span style="font-size:1.6rem;font-weight:800;color:#f59e0b;letter-spacing:5px;
                         font-family:'Courier New',monospace;">{code}</span>
          </div>

          <!-- Steps -->
          <p style="color:#c4c9d8;font-size:0.95rem;font-weight:700;margin-bottom:12px;">
            How to activate:
          </p>
          <ol style="color:#9ca3af;font-size:0.88rem;line-height:2.2;padding-left:20px;">
            <li>Open <a href="{APP_URL}" style="color:#a78bfa;text-decoration:none;">{APP_URL}</a></li>
            <li>Go to any Pro feature (e.g. <strong style="color:#e2eaf8;">Interview Predictor</strong> or <strong style="color:#e2eaf8;">A/B Testing</strong>)</li>
            <li>You'll see a <strong style="color:#f59e0b;">"Already paid? Enter your access code"</strong> field</li>
            <li>Paste your code and click <strong style="color:#e2eaf8;">🔓 Unlock Pro</strong> — done! ✅</li>
          </ol>

          <div style="background:rgba(245,158,11,0.08);border-left:4px solid #f59e0b;
                      border-radius:0 8px 8px 0;padding:12px 16px;margin-top:24px;">
            <p style="margin:0;color:#9ca3af;font-size:0.82rem;">
              ⚠️ This code is personal. Do not share it — each code works for one person.
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div style="padding:20px 40px;border-top:1px solid rgba(99,102,241,0.15);text-align:center;">
          <p style="margin:0;color:#4b5563;font-size:0.78rem;">
            ResumeIQ · Made for students who mean business
          </p>
        </div>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())


# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


@app.route('/webhook/razorpay', methods=['POST'])
def razorpay_webhook():
    """Receive Razorpay payment_link.paid event and send code to customer."""

    # 1. Verify webhook signature
    raw_body  = request.get_data()
    signature = request.headers.get('X-Razorpay-Signature', '')

    expected = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        app.logger.warning("Invalid webhook signature")
        return jsonify({"error": "Invalid signature"}), 400

    data  = request.get_json(force=True)
    event = data.get('event', '')

    # 2. Only handle payment_link.paid
    if event != 'payment_link.paid':
        return jsonify({"status": f"event '{event}' ignored"}), 200

    try:
        pl_entity  = data['payload']['payment_link']['entity']
        pay_entity = data['payload']['payment']['entity']

        customer      = pl_entity.get('customer', {})
        customer_name = customer.get('name', 'Customer')
        customer_email = customer.get('email', '').strip()
        payment_id    = pay_entity.get('id', '')

        if not customer_email:
            app.logger.error("No email in payload")
            return jsonify({"error": "No customer email found in payload"}), 400

        # 3. Generate unique code
        code = generate_code()

        # 4. Store in Supabase
        supabase.table('pro_codes').insert({
            'code':          code,
            'email':         customer_email,
            'payment_id':    payment_id,
            'customer_name': customer_name,
        }).execute()

        # 5. Send email
        send_email(customer_email, code, customer_name)

        app.logger.info(f"Code {code} sent to {customer_email}")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        app.logger.exception("Webhook processing failed")
        return jsonify({"error": str(e)}), 500


@app.route('/validate', methods=['GET'])
def validate_code():
    """Streamlit app calls this endpoint to check if a code is valid."""
    code = request.args.get('code', '').strip().upper()
    if not code:
        return jsonify({"valid": False}), 200

    result = supabase.table('pro_codes') \
        .select('code') \
        .eq('code', code) \
        .execute()

    is_valid = bool(result.data)
    return jsonify({"valid": is_valid}), 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
