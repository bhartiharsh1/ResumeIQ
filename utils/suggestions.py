import re


def generate_suggestions(resume_text, present_skills, missing_skills):

    text = resume_text.lower()
    suggestions = []

    # Experience check
    if "experience" not in text:
        suggestions.append(
            "💼 Add an Experience section to showcase internships or work."
        )

    # Projects check
    if "project" in text:
        if "developed" not in text and "built" not in text:
            suggestions.append(
                "🚀 Improve project descriptions using action verbs like 'developed', 'built'."
            )
    else:
        suggestions.append("🧪 Add 2–3 strong projects relevant to your role.")

    # Numbers / impact
    if not re.search(r"\d+", text):
        suggestions.append("📊 Add measurable impact (e.g., improved accuracy by 20%).")

    # Missing skills
    if missing_skills:
        suggestions.append(f"🧠 Add these skills: {', '.join(missing_skills[:5])}")

    # Tools
    tools = ["python", "sql", "excel", "aws", "docker"]
    if not any(t in text for t in tools):
        suggestions.append("🛠️ Mention tools/technologies used in your projects.")

    if not suggestions:
        suggestions.append(
            "🔥 Your resume looks strong! Try tailoring it for specific jobs."
        )

    return suggestions
