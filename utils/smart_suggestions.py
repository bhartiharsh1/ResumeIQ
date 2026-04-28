import json
from utils.bullet_extractor import _get_client

# Primary model first; fallbacks tried in order on 429 / 404 errors
_MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-1.5-flash",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
]

_PROMPT = """You are an expert ATS resume reviewer.

Your task is to analyze the given resume and generate a MAXIMUM of 5 precise, context-aware, and highly actionable suggestions.

CRITICAL RULES:
1. Provide a MAXIMUM of 5 suggestions total. Focus ONLY on the absolute weakest lines that need the most critical improvement.
2. DO NOT REPEAT ADVICE. Every suggestion must highlight a DIFFERENT flaw (e.g. do not complain about missing action verbs more than once).
3. Do not give generic advice. Only pinpoint explicit flaws like "missing metrics", "passive voice", "cliche phrases", etc.
4. Each suggestion MUST exactly quote a specific `original_line` from the resume text. Do not invent lines.
5. Provide a realistic `improved_suggestion` that uses strong action verbs and incorporates plausible metrics/results.
6. Include a numeric `confidence_score` between 0 and 100 (only include >= 80).

Output format must be a JSON array of objects exactly like this:
[
  {
    "original_line": "...",
    "issue": "...",
    "improved_suggestion": "...",
    "confidence_score": 85
  }
]
"""


def _parse_json(text: str):
    """Strip markdown fences and extract JSON array from model output."""
    for fence in ("```json", "```"):
        if text.startswith(fence):
            text = text[len(fence):]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    start = text.find('[')
    end   = text.rfind(']')
    if start != -1 and end != -1:
        parsed = json.loads(text[start:end + 1])
        if isinstance(parsed, list):
            return parsed
    return []


def get_line_level_suggestions(resume_text: str):
    """Call LLM with automatic model fallback on rate-limit (429) errors."""
    messages = [
        {"role": "system", "content": "You are a JSON-generating assistant. "
                                      "Only return the JSON array of objects as requested. "
                                      "No markdown formatting or extra text."},
        {"role": "user",   "content": _PROMPT + "\n\nResume Text:\n" + resume_text},
    ]

    last_error = None
    for model in _MODELS:
        try:
            response = _get_client().chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0,
            )
            text = response.choices[0].message.content.strip()
            result = _parse_json(text)
            return result  # success — return immediately

        except Exception as e:
            err_str = str(e)
            safe   = err_str.encode("ascii", errors="replace").decode("ascii")
            # Only fall through to next model on rate-limit / quota errors
            if any(x in err_str for x in ("429", "404")) or "rate" in err_str.lower() or "quota" in err_str.lower():
                print(f"[smart_suggestions] Model {model} unavailable ({safe}), trying next...")
                last_error = e
                continue
            # Any other error — return immediately with error payload
            print(f"[smart_suggestions] Error with {model}: {safe}")
            return [{"error": err_str}]

    # All models exhausted
    safe_last = str(last_error).encode("ascii", errors="replace").decode("ascii")
    print(f"[smart_suggestions] All models rate-limited: {safe_last}")
    return [{"error": str(last_error)}]
