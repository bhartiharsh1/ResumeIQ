import re


def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9+ ]", " ", text.lower())


def extract_skills(resume_text, selected_profile, skills_db):

    text = clean_text(resume_text)

    profile_skills = skills_db.get(selected_profile, {})

    present_skills = []
    missing_skills = []
    exact_matches = []

    for skill, keywords in profile_skills.items():
        found = False

        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"

            if re.search(pattern, text):
                found = True
                exact_matches.append(keyword)  # exact keyword
                break

        if found:
            present_skills.append(skill)
        else:
            missing_skills.append(skill)

    return present_skills, missing_skills, list(set(exact_matches))
