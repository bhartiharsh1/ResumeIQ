import json
import os
import time
import requests
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDBACK_FILE = os.path.join(BASE_DIR, "data", "feedback.json")

def save_feedback(feedback_type, text, email="Guest"):
    """
    Saves user feedback. Tries to send to a Google Sheets Webhook if configured,
    otherwise falls back to a local JSON file.
    """
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Try sending to Google Sheets Webhook if configured in Streamlit secrets
    webhook_url = ""
    try:
        webhook_url = st.secrets.get("FEEDBACK_WEBHOOK_URL", "")
    except Exception:
        pass
        
    if webhook_url:
        try:
            payload = {
                "date": date_str,
                "type": feedback_type,
                "email": email,
                "text": text
            }
            # Send data to Apps Script Webhook
            requests.post(webhook_url, json=payload, timeout=5)
            return  # Successfully sent to cloud, no need to save locally
        except Exception as e:
            pass # Fall back to local file silently
            
    # Fallback to saving locally
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    
    data = []
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
            
    data.append({
        "timestamp": time.time(),
        "date": date_str,
        "type": feedback_type,
        "text": text,
        "email": email
    })
    
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
