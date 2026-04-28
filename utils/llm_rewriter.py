import json
from utils.bullet_extractor import _get_client

# Fallback model chain — tried in order on 429 / 404 / 504 errors
_MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-1.5-flash",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
]

_RETRYABLE = ("429", "404", "504", "502", "503")


def rewrite_bullet(bullet_text, role, strength="Basic Polish"):
    if strength == "Aggressive Transformation":
        guidance = (
            "Dramatically rewrite the bullet to maximize impact. "
            "Inject strong professional industry jargon, structurally optimize "
            "the wording, and vividly highlight outcomes."
        )
    else:
        guidance = (
            "Polish the bullet. Fix grammar, ensure it starts with a strong "
            "action verb, and make it concise and ATS-friendly."
        )

    prompt = f"""You are an expert Executive Resume Writer and ATS Optimizer.
Your task is to intelligently rewrite the provided resume bullet point to make it exceptionally strong for a {role} position.

Guidelines:
1. Format strictly as: [Action Verb] + [Task/Contribution] + [Tools/Skills] + [Measurable Outcome].
2. {guidance}
3. Maintain factual accuracy but vastly elevate the professional tone. Do not invent completely fake metrics, but you can phrase existing numbers better.

Provide the response STRICTLY as a JSON object with two keys mapping to strings:
- "rewritten_bullet": The new, polished bullet point.
- "feedback_reason": A short 1-sentence critical phrasing of why the original bullet was weak and how you improved it.

Original Bullet: "{bullet_text}"
"""

    messages = [
        {"role": "system", "content": "You are a specialized JSON-generating ATS resume optimization assistant. Always return pure JSON."},
        {"role": "user",   "content": prompt},
    ]

    last_error = None
    for model in _MODELS:
        try:
            response = _get_client().chat.completions.create(
                model=model,
                messages=messages,
            )
            text = response.choices[0].message.content.strip()
            for fence in ("```json", "```"):
                if text.startswith(fence):
                    text = text[len(fence):]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            return json.loads(text)

        except Exception as e:
            err_str = str(e)
            safe = err_str.encode("ascii", errors="replace").decode("ascii")
            if any(code in err_str for code in _RETRYABLE) or \
               "rate" in err_str.lower() or "quota" in err_str.lower() or \
               "aborted" in err_str.lower() or "timeout" in err_str.lower():
                print(f"[llm_rewriter] Model {model} unavailable ({safe}), trying next...")
                last_error = e
                continue
            return {"error": err_str}

    return {"error": str(last_error)}
