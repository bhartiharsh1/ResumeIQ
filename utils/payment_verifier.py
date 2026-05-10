import json
from utils.bullet_extractor import _get_client

def verify_payment_screenshot(base64_image: str) -> dict:
    prompt = """You are a payment verification assistant.
Look at the attached image. Determine if it is a successful UPI payment screenshot.
Specifically, check for:
1. The payment is marked as successful or completed.
2. The amount is ₹79 (79 INR).
3. The recipient is "bhartiharsh64-1@oksbi" or "Harsh Bharti".

Return your answer strictly as a JSON object with two keys:
- "is_valid": boolean (true if all conditions are met, false otherwise)
- "reason": A short string explaining your decision.

ONLY output valid JSON without any markdown formatting like ```json.
"""
    _models = [
        "google/gemini-2.0-flash-001",
        "google/gemini-1.5-flash",
    ]
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]}
    ]

    last_error = None
    for model in _models:
        try:
            response = _get_client().chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0,
            )
            text = response.choices[0].message.content.strip()

            # Strip markdown fences
            for fence in ("```json", "```"):
                if text.startswith(fence):
                    text = text[len(fence):]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            result = json.loads(text)
            if "is_valid" not in result:
                result["is_valid"] = False
            if "reason" not in result:
                result["reason"] = "Unexpected response format."
            return result
            
        except Exception as e:
            err_str = str(e)
            if any(x in err_str for x in ("429", "404", "504", "502", "503")) or \
               "rate" in err_str.lower() or "quota" in err_str.lower() or \
               "aborted" in err_str.lower() or "timeout" in err_str.lower():
                print(f"[payment_verifier] Model {model} unavailable, trying next...")
                last_error = e
                continue
            return {"is_valid": False, "reason": f"Verification failed: {err_str}"}
    
    return {"is_valid": False, "reason": f"All models rate-limited or unavailable: {last_error}"}
