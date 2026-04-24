
# ---------------- LENGTH CHECK ----------------
def check_length(resume_text):
    words = len(resume_text.split())

    if words < 300:
        return 40
    elif 300 <= words <= 800:
        return 100
    elif 800 < words <= 1200:
        return 70
    else:
        return 40


# ---------------- BULLET CHECK ----------------
def check_bullets(resume_text):
    bullets = resume_text.count("•") + resume_text.count("-")

    if bullets >= 15:
        return 100
    elif bullets >= 8:
        return 70
    else:
        return 40


# ---------------- FORMAT SCORE ----------------
def calculate_format_score(resume_text):

    length_score = check_length(resume_text)
    bullet_score = check_bullets(resume_text)

    format_score = (length_score + bullet_score) / 2

    return round(format_score, 2)


# ---------------- SECTION CHECK ----------------
def calculate_section_score(resume_text):

    text = resume_text.lower()

    sections = ["education", "experience", "projects", "skills", "certifications"]

    found = 0

    for sec in sections:
        if sec in text:
            found += 1

    score = (found / len(sections)) * 100

    return round(score, 2)
