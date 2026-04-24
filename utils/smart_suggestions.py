import json
from openai import OpenAI
import os

from utils.bullet_extractor import API_KEY, client

def get_line_level_suggestions(resume_text):
    prompt = """You are an expert ATS resume reviewer.

Your task is to analyze the given resume and generate a MAXIMUM of 5 precise, context-aware, and highly actionable suggestions.

CRITICAL RULES:
1. Provide a MAXIMUM of 5 suggestions total. Focus ONLY on the absolute weakest lines that need the most critical improvement.
2. DO NOT REPEAT ADVICE. Every suggestion must highlight a DIFFERENT flaw (e.g. do not complain about missing action verbs more than once).
3. Do not give generic advice. Only pinpoint explicit flaws like "missing metrics", "passive voice", "cliché phrases", etc.
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
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are a JSON-generating assistant. Only return the JSON array of objects as requested in the output format. No markdown formatting or extra text."},
                {"role": "user", "content": prompt + "\n\nResume Text:\n" + resume_text}
            ],
            temperature=0.0
        )

        text = response.choices[0].message.content.strip()
        
        # Strip markdown json blocks if they exist
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)
        if text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text[:-3]
            
        text = text.strip()
        
        # Parse logic
        start_idx = text.find('[')
        end_idx = text.rfind(']')
        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx:end_idx+1]
            extracted = json.loads(json_str)
            if isinstance(extracted, list):
                return extracted
        return []
        
    except Exception as e:
        print(f"Error generating smart suggestions: {e}")
        return [{"error": str(e)}]
