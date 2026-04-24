"""interview_prep.py — Predict likely interview questions from resume + JD."""
import json, os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY", ""), base_url="https://openrouter.ai/api/v1")
_MODEL = "google/gemini-2.0-flash-001"


def predict_interview_questions(resume_text: str, jd_text: str = "") -> dict:
    jd_section = f"\n\nJob Description:\n{jd_text[:1500]}" if jd_text.strip() else ""
    prompt = f"""You are an expert interview coach. Analyze this resume{' and job description' if jd_text.strip() else ''} and generate 5 highly specific, realistic interview questions per category. Make them SPECIFIC to this person's actual skills and experience — not generic.

Resume:
{resume_text[:3000]}{jd_section}

Output ONLY a JSON object:
{{
  "behavioral": ["Q1","Q2","Q3","Q4","Q5"],
  "technical": ["Q1","Q2","Q3","Q4","Q5"],
  "role_specific": ["Q1","Q2","Q3","Q4","Q5"],
  "company_specific": ["Q1","Q2","Q3","Q4","Q5"]
}}"""
    try:
        resp = _client.chat.completions.create(
            model=_MODEL,
            messages=[{"role": "system", "content": "Return only valid JSON."}, {"role": "user", "content": prompt}],
            temperature=0.7
        )
        text = resp.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            return json.loads(text[s:e+1])
        return {"error": "Could not parse response"}
    except Exception as ex:
        return {"error": str(ex)}
