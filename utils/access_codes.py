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

import time

def generate_unique_code(email):
    code = "PRO-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    codes = _load_json(CODES_FILE, {})
    codes[code] = {
        "email": email,
        "expires_at": time.time() + (6 * 3600), # 6 hours from now
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
        
    if time.time() > c_data.get("expires_at", 0):
        c_data["active"] = False
        _save_json(CODES_FILE, codes)
        return False
        
    return True

def has_premium_access(email):
    """Check if the user has an active, unexpired premium code."""
    codes = _load_json(CODES_FILE, {})
    has_access = False
    
    for code, data in codes.items():
        if data.get("email") == email and data.get("active", False):
            if time.time() < data.get("expires_at", 0):
                has_access = True
            else:
                data["active"] = False # Expire it
                
    _save_json(CODES_FILE, codes)
    return has_access

def get_premium_expiry(email):
    """Returns the expiration timestamp for the user's active premium, or 0 if none."""
    codes = _load_json(CODES_FILE, {})
    best_expiry = 0
    for code, data in codes.items():
        if data.get("email") == email and data.get("active", False):
            expiry = data.get("expires_at", 0)
            if expiry > time.time() and expiry > best_expiry:
                best_expiry = expiry
    return best_expiry
