import json
from openai import OpenAI

from utils.bullet_extractor import API_KEY, client

def rewrite_bullet(bullet_text, role, strength="Basic Polish"):
    if strength == "Aggressive Transformation":
        guidance = "Dramatically rewrite the bullet to maximize impact. Inject strong professional industry jargon, structurally optimize the wording, and vividly highlight outcomes."
    else:
        guidance = "Polish the bullet. Fix grammar, ensure it starts with a strong action verb, and make it concise and ATS-friendly."

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

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are a specialized JSON-generating ATS resume optimization assistant. Always return pure JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)
        if text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        data = json.loads(text)
        return data

    except Exception as e:
        return {"error": str(e)}
