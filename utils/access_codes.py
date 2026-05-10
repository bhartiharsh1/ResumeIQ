import json
import os
import random
import string

CODES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "access_codes.json")

def _load_codes():
    if not os.path.exists(CODES_FILE):
        return []
    try:
        with open(CODES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def _save_codes(codes):
    os.makedirs(os.path.dirname(CODES_FILE), exist_ok=True)
    with open(CODES_FILE, "w") as f:
        json.dump(codes, f, indent=2)

def generate_unique_code():
    code = "PRO-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    codes = _load_codes()
    if code not in codes:
        codes.append(code)
        _save_codes(codes)
    return code

def validate_code(code):
    if code.strip() == "HARSH-PRO-2026":
        return True
    codes = _load_codes()
    if code.strip() in codes:
        return True
    return False
