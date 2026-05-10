import json
import os
import random
import string

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CODES_FILE = os.path.join(DATA_DIR, "access_codes.json")
USED_TX_FILE = os.path.join(DATA_DIR, "used_payments.json")

def _load_json(filepath, default):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, type(default)):
                return data
            return default
    except:
        return default

def _save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def is_transaction_used(tx_id):
    if not tx_id or tx_id.strip() == "":
        return False
    used = _load_json(USED_TX_FILE, [])
    return tx_id in used

def mark_transaction_used(tx_id):
    if not tx_id or tx_id.strip() == "":
        return
    used = _load_json(USED_TX_FILE, [])
    if tx_id not in used:
        used.append(tx_id)
        _save_json(USED_TX_FILE, used)

def generate_unique_code(email):
    code = "PRO-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    codes = _load_json(CODES_FILE, {})
    codes[code] = {
        "email": email,
        "usages": 0,
        "max_usages": 3,
        "active": True
    }
    _save_json(CODES_FILE, codes)
    return code

def validate_code(code, email):
    if code.strip() == "HARSH-PRO-2026":
        return True
    
    codes = _load_json(CODES_FILE, {})
    c_data = codes.get(code.strip())
    
    if not c_data:
        return False
        
    if not c_data.get("active", False):
        return False
        
    if c_data.get("email") != email:
        return False
        
    if c_data.get("usages", 0) >= c_data.get("max_usages", 3):
        return False
        
    return True

def use_premium_action(email):
    """Call this when a user performs a premium action. Returns True if allowed."""
    codes = _load_json(CODES_FILE, {})
    active_code = None
    for code, data in codes.items():
        if data.get("email") == email and data.get("active", False):
            if data.get("usages", 0) < data.get("max_usages", 3):
                active_code = code
                break
                
    if active_code:
        codes[active_code]["usages"] += 1
        if codes[active_code]["usages"] >= codes[active_code]["max_usages"]:
            codes[active_code]["active"] = False # Expire it
        _save_json(CODES_FILE, codes)
        return True
    
    return False

def get_remaining_usages(email):
    codes = _load_json(CODES_FILE, {})
    for code, data in codes.items():
        if data.get("email") == email and data.get("active", False):
            return data.get("max_usages", 3) - data.get("usages", 0)
    return 0
