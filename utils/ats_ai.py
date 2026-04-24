import re

# ---------------- SECTION DETECTION ----------------
SECTION_PATTERNS = {
    "experience": r"\b(experience|work|employment)\b",
    "education": r"\b(education|university|college)\b",
    "skills": r"\b(skills|technologies)\b",
    "projects": r"\b(projects)\b",
    "summary": r"\b(summary|objective)\b",
}


def detect_sections(text):
    text = text.lower()
    return {k: bool(re.search(v, text)) for k, v in SECTION_PATTERNS.items()}


def check_contact(text):
    return {
         "email": bool(
            re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
        ),
        "phone": bool(re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)),
        "linkedin": "linkedin" in text.lower(),
    }


# ---------------- METRICS ----------------
def count_metrics(text):
    matches = re.findall(
        r"\d+%|\$\d+(?:[kKmMbB])?|\b(?!(?:19|20)\d{2}\b)\d{1,4}(?:[kKmM\+])?\b",
        text.lower(),
    )
    return len(matches)


# ---------------- VERBS ----------------
STRONG_VERBS = [
    "developed",
    "built",
    "designed",
    "led",
    "optimized",
    "created",
    "implemented",
    "improved",
    "managed",
    "architected",
    "spearheaded",
    "delivered",
    "engineered",
    "orchestrated",
    "launched",
    "analyzed",
    "reduced",
    "increased",
    "resolved",
    "coordinated",
    "collaborated",
    "facilitated",
    "mentored",
    "streamlined",
    "transformed",
]


def score_verbs(text):
    text = text.lower()
    return sum(1 for v in STRONG_VERBS if v in text)


# ---------------- LENGTH ----------------
def score_length(text):
    wc = len(text.split())
    if 300 <= wc <= 900:
        return 100
    elif 200 <= wc < 300 or wc > 900:
        return 70
    return 40


# ---------------- FINAL ATS ----------------
def real_ats_score(resume_text):

    text = resume_text

    sections = detect_sections(text)
    contact = check_contact(text)
    metrics = count_metrics(text)
    verbs = score_verbs(text)
    length_score = score_length(text)

    score = 0

    # 1. Parseability (20)
    score += 20

    # 2. Sections (20)
    section_score = (sum(sections.values()) / len(sections)) * 20
    score += section_score

    # 3. Contact (15)
    contact_score = sum(contact.values()) * 5
    score += contact_score

    # 4. Metrics (15)
    score += min(metrics * 3, 15)

    # 5. Verbs (20)
    score += min(verbs * 4, 20)

    # 6. Length (10)
    score += length_score * 0.1

    return round(min(score, 100), 2), {
        "sections": sections,
        "contact": contact,
        "metrics": metrics,
        "verbs": verbs,
        "length_score": length_score,
    }
