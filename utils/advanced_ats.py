from utils.sematic_match import semantic_similarity


# -------- SKILL MATCH --------
def advanced_skill_match(resume_text, skills):

    matched = []

    for skill in skills:
        score = semantic_similarity(resume_text, skill)

        if score > 35:  # lower threshold → more realistic
            matched.append(skill)

    return matched


# -------- IMPACT SCORE --------
def impact_score(resume_text):

    text = resume_text.lower()

    verbs = [
        "developed",
        "built",
        "designed",
        "implemented",
        "optimized",
        "led",
        "improved",
        "created",
        "managed",
        "architected",
        "spearheaded",
        "delivered",
        "engineered",
        "orchestrated",
        "launched",
    ]

    score = 30  # 🔥 lower base (important)

    if any(v in text for v in verbs):
        score += 25

    if any(char.isdigit() for char in text):
        score += 25

    if "%" in text:
        score += 20

    return min(score, 100)


# -------- SECTION QUALITY --------
def section_quality(resume_text):

    text = resume_text.lower()

    score = 0

    if "education" in text:
        score += 15
    if "experience" in text:
        score += 30
    if "project" in text:
        score += 30
    if "skills" in text:
        score += 25

    return score


# -------- FINAL ATS --------
def final_ats_score(resume_text, matched_skills):

    # 🔥 BETTER SKILL SCORING
    skill_score = min(len(matched_skills) * 15, 100)

    impact = impact_score(resume_text)
    section = section_quality(resume_text)

    # 🔥 NEW WEIGHTS (VERY IMPORTANT)
    final = 0.45 * skill_score + 0.30 * impact + 0.25 * section

    return round(final, 2)
