import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- HELPER FUNCTIONS ---------------- #

def get_section_text(resume_text, section_name):
    pattern = rf"{section_name}.*?(?=\n[A-Z][^\n]+\n|\Z)"
    match = re.search(pattern, resume_text, re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else ""


def count_action_verbs(text):
    verbs = [
        "developed", "built", "designed", "implemented", "optimized",
        "led", "created", "engineered", "analyzed", "improved"
    ]
    return sum(text.lower().count(v) for v in verbs)


def count_metrics(text):
    return len(re.findall(r"\b\d+%|\b\d+\b|\$\d+", text))


def keyword_match(text, target_skills):
    text = text.lower()
    matched = [skill for skill in target_skills if skill.lower() in text]
    return len(matched), len(target_skills)


def compute_similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([text1, text2])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100


def structure_score(text):
    lines = text.split("\n")
    bullet_count = sum(1 for l in lines if l.strip().startswith(("-", "•", "*")))
    word_count = len(text.split())

    score = 100

    if bullet_count < 3:
        score -= 30
    if word_count < 50:
        score -= 20
    if word_count > 400:
        score -= 10

    return max(score, 0)


# ---------------- SECTION SCORERS ---------------- #

def score_experience(text, jd_text, target_skills):
    verbs = count_action_verbs(text)
    metrics = count_metrics(text)
    matched, total = keyword_match(text, target_skills)

    verbs_score = min(verbs * 10, 100)
    metrics_score = min(metrics * 12, 100)
    keyword_score = (matched / max(1, total)) * 100
    jd_score = compute_similarity(text, jd_text)
    struct = structure_score(text)

    final = (
        0.25 * verbs_score +
        0.30 * metrics_score +
        0.20 * keyword_score +
        0.15 * jd_score +
        0.10 * struct
    )

    feedback = []
    if verbs < 3:
        feedback.append("Use more strong action verbs (developed, built, optimized)")
    if metrics < 2:
        feedback.append("Add measurable impact (%, numbers, results)")
    if keyword_score < 50:
        feedback.append("Improve alignment with target role skills")
    if jd_score < 50:
        feedback.append("Low relevance to job description")

    return int(final), feedback


def score_projects(text, jd_text, target_skills):
    metrics = count_metrics(text)
    matched, total = keyword_match(text, target_skills)
    jd_score = compute_similarity(text, jd_text)

    tech_score = (matched / max(1, total)) * 100
    complexity_score = min(len(text.split()) / 5, 100)
    impact = min(metrics * 15, 100)

    final = (
        0.30 * tech_score +
        0.30 * complexity_score +
        0.20 * jd_score +
        0.20 * impact
    )

    feedback = []
    if impact < 30:
        feedback.append("Projects lack measurable outcomes")
    if tech_score < 50:
        feedback.append("Use more relevant technologies")
    if jd_score < 50:
        feedback.append("Projects not aligned with job role")

    return int(final), feedback


def score_skills(text, target_skills):
    matched, total = keyword_match(text, target_skills)

    score = (matched / max(1, total)) * 100

    feedback = []
    if score < 50:
        feedback.append("Missing key skills for target role")
    if matched < 5:
        feedback.append("Increase skill density")

    return int(score), feedback


def score_education(text):
    score = 70

    if re.search(r"b\.?tech|bachelor", text.lower()):
        score += 10
    if re.search(r"cgpa|gpa|percentage", text.lower()):
        score += 10
    if len(text.split()) < 30:
        score -= 20

    feedback = []
    if score < 70:
        feedback.append("Add degree details or academic performance")

    return int(min(score, 100)), feedback


# ---------------- MAIN FUNCTION ---------------- #

def final_section_score(resume_text, target_skills, jd_text=""):
    sections = {
        "Education": get_section_text(resume_text, "education"),
        "Experience": get_section_text(resume_text, "experience"),
        "Projects": get_section_text(resume_text, "project"),
        "Skills": get_section_text(resume_text, "skill"),
    }

    results = {}

    edu_score, edu_fb = score_education(sections["Education"])
    exp_score, exp_fb = score_experience(sections["Experience"], jd_text, target_skills)
    proj_score, proj_fb = score_projects(sections["Projects"], jd_text, target_skills)
    skill_score, skill_fb = score_skills(sections["Skills"], target_skills)

    results["Education"] = {"score": edu_score, "feedback": edu_fb}
    results["Experience"] = {"score": exp_score, "feedback": exp_fb}
    results["Projects"] = {"score": proj_score, "feedback": proj_fb}
    results["Skills"] = {"score": skill_score, "feedback": skill_fb}

    return results