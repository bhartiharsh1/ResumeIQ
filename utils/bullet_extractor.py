import os
import json
import re
from openai import OpenAI
from utils.config import get_openrouter_key


def _get_client():
    """Return a fresh OpenAI client pointed at OpenRouter."""
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=get_openrouter_key())


def extract_bullets_from_resume(resume_text):
    prompt = """You are an expert resume reviewer.

Your task is to extract ONLY the exact lines from the resume that:
1. Represent meaningful content (e.g., bullet points, descriptions, summary, skills, achievements)
2. Can be improved, rewritten, or optimized
3. Are complete sentences or logical phrases

STRICT RULES:
- DO NOT extract dates, months, years, durations, or timelines
- DO NOT extract section headings (e.g., "Education", "Experience")
- DO NOT extract incomplete fragments or broken lines
- DO NOT extract contact details (email, phone, links)
- DO NOT paraphrase or modify the text — return EXACT lines as they appear
- Each extracted item must be a full, meaningful statement

FOCUS ON:
- Weak bullet points
- Generic statements (e.g., "Responsible for...")
- Poorly written achievements
- Lines lacking metrics or impact

OUTPUT FORMAT:
Return a clean list of exact lines:
[
  "line 1",
  "line 2",
  "line 3"
]

If no such lines exist, return:
[]"""

    # Fallback model list — tried in order on rate-limit (429) or missing model (404) errors
    _models = [
        "google/gemini-2.0-flash-001",
        "google/gemini-1.5-flash",
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
    ]
    messages = [
        {"role": "system", "content": "You are a JSON-generating assistant. "
                                      "Only return the JSON array of strings as requested. "
                                      "No markdown formatting or extra text."},
        {"role": "user", "content": prompt + "\n\nResume Text:\n" + resume_text},
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

            # Parse JSON array
            start_idx = text.find('[')
            end_idx   = text.rfind(']')
            if start_idx != -1 and end_idx != -1:
                extracted = json.loads(text[start_idx:end_idx + 1])
                if isinstance(extracted, list):
                    return extracted
            return []

        except Exception as e:
            err_str = str(e)
            safe    = err_str.encode("ascii", errors="replace").decode("ascii")
            if any(x in err_str for x in ("429", "404")) or "rate" in err_str.lower() or "quota" in err_str.lower():
                print(f"[bullet_extractor] Model {model} unavailable ({safe}), trying next...")
                last_error = e
                continue
            print(f"[bullet_extractor] Error with {model}: {safe}")
            return []

    safe_last = str(last_error).encode("ascii", errors="replace").decode("ascii")
    print(f"[bullet_extractor] All models rate-limited: {safe_last}")
    return []
