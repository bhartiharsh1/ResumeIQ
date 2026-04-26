"""cold_outreach.py — Generate cold email + LinkedIn message for job outreach."""
import json, os
from openai import OpenAI

_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")

def _get_api_key() -> str:
    try:
        import streamlit as st
        key = st.secrets.get("OPENROUTER_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key
    try:
        from dotenv import load_dotenv as _ld
        _ld(dotenv_path=_ENV_PATH, override=True)
    except Exception:
        pass
    return os.environ.get("OPENROUTER_API_KEY", "")

def _get_client():
    return OpenAI(api_key=_get_api_key(), base_url="https://openrouter.ai/api/v1")

_MODEL = "openai/gpt-4o-mini"


_PERSON_CTX = {
    "Recruiter":       "a recruiter at the company. Professional tone, show enthusiasm and key skills briefly.",
    "Alumni":          "a college/university alumni at the company. Warm tone — leverage the shared college connection.",
    "Referral":        "someone who could refer you internally. Be direct about your ask; make it easy for them to say yes.",
    "Hiring Manager":  "the hiring manager. Lead with impact, show deep understanding of the role's challenges, be confident.",
}


def generate_outreach(resume_text: str, company: str, role: str,
                      person_type: str, person_name: str = "") -> dict:
    ctx = _PERSON_CTX.get(person_type, _PERSON_CTX["Recruiter"])
    name_clause = f"Their name is {person_name}." if person_name.strip() else "Use 'Hi [Name]' as placeholder."
    prompt = f"""You are an expert at cold outreach that actually gets replies.

Write messages for someone reaching out to {company} for a {role} role.
They are writing to {ctx}
{name_clause}

Use specific details from the resume. Reference {company} by name. No buzzwords. Clear CTA.

Resume highlights:
{resume_text[:2000]}

Output ONLY valid JSON:
{{
  "email_subject": "...",
  "email_body": "...(~150 words)...",
  "linkedin_message": "...(max 80 words)..."
}}"""
    try:
        resp = _get_client().chat.completions.create(
            model=_MODEL,
            messages=[{"role": "system", "content": "Return only valid JSON."}, {"role": "user", "content": prompt}],
            temperature=0.8
        )
        text = resp.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            return json.loads(text[s:e+1])
        return {"error": "Could not parse response"}
    except Exception as ex:
        return {"error": str(ex)}
