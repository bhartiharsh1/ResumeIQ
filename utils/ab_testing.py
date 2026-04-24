import json
from openai import OpenAI

from utils.bullet_extractor import API_KEY, client


def compare_resumes_llm(resume_a, resume_b, jd):
    prompt = f"""You are an Expert Technical Recruiter evaluating two candidate resumes against a specific Job Description.

Job Description:
"{jd}"

Resume A Text:
"{resume_a}"

Resume B Text:
"{resume_b}"

Analyze both resumes and determine which one is objectively better suited for the Job Description. Judge based on:
1. Keyword match and skill alignment.
2. Strength of measurable outcomes (metrics, impact).
3. Clarity and professional tone.

Return your evaluation STRICTLY as a JSON object with EXACTLY these keys:
- "winner": A string, either "Resume A" or "Resume B" or "Tie".
- "key_differences": An array of strings, listing 2-3 main reasons why the winner is better (e.g. "Resume A uses stronger active verbs" or "Resume B has a missing Education section").
- "final_verdict": A short paragraph (2-3 sentences) summarizing your decision like a real human recruiter giving feedback.
"""

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are a Resume A/B Testing evaluator. Always return pure JSON."},
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
        return dict(data)
    except Exception as e:
        return {"error": str(e)}
