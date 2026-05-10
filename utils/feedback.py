import json
import os
import time

FEEDBACK_FILE = os.path.join("data", "feedback.json")

def save_feedback(feedback_type, text, email="Guest"):
    """
    Saves user feedback to a local JSON file.
    """
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
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "type": feedback_type,
        "text": text,
        "email": email
    })
    
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
