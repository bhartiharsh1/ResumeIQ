"""cover_letter.py — Generate real, personalized cover letters from resume + JD."""
from openai import OpenAI
from utils.config import get_openrouter_key


def _get_client():
    return OpenAI(api_key=get_openrouter_key(), base_url="https://openrouter.ai/api/v1")


_MODEL = "openai/gpt-4o-mini"


_TONE = {
    "Professional": "formal, confident, polished — business-appropriate language",
    "Enthusiastic": "energetic, genuine excitement, warm and human",
    "Concise":      "punchy and brief (~200 words total) — maximum impact, respects recruiter's time",
}


def generate_cover_letter(resume_text: str, jd_text: str, name: str,
                          company: str, role: str, tone: str = "Professional") -> dict:
    tone_desc = _TONE.get(tone, _TONE["Professional"])

    prompt = f"""You are an expert cover letter writer. Your job is to write a highly personalized, authentic cover letter.

APPLICANT DETAILS (use these EXACTLY — do not substitute from the JD):
- Full Name: {name}
- Applying for: {role}
- Target Company: {company}  ← use THIS company name everywhere, not any company mentioned in the JD

TONE: {tone_desc}

STRICT RULES:
1. Open with a powerful hook — reference ONE specific achievement from the resume in the first sentence
2. Body (2 paragraphs): pick 2–3 SPECIFIC accomplishments with metrics/numbers from the resume and connect them to what {company} needs for {role}
3. Never invent facts — only use what is in the resume text below
4. Never use: "I am writing to express my interest", "passionate about", "team player", "hard worker"
5. Close with a direct call-to-action and sign off as:
   Sincerely,
   {name}
6. Output format — write the COMPLETE letter including greeting and sign-off:
   Dear Hiring Manager at {company},
   
   [body]
   
   Sincerely,
   {name}

RESUME (extract real achievements, numbers, technologies, institutions from here):
{resume_text[:3000]}

JOB DESCRIPTION (understand the role requirements — but use ONLY "{company}" as the company name):
{jd_text[:1500]}

Write the complete cover letter now:"""

    try:
        resp = _get_client().chat.completions.create(
            model=_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You write real, personalized cover letters. "
                        f"The applicant is {name}. The company is ALWAYS '{company}'. "
                        f"The role is '{role}'. Never use a different company name. "
                        f"Always end with 'Sincerely,\\n{name}'."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        letter = resp.choices[0].message.content.strip()
        return {"cover_letter": letter, "word_count": len(letter.split())}
    except Exception as ex:
        return {"error": str(ex)}
