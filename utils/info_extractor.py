import re


def extract_basic_info(resume_text):
    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]

    text = resume_text

    # ------------------ ROLL NUMBER ------------------
    roll_number = "Not Found"
    roll_match = re.search(r"\b[A-Z]{2}\d{2}[A-Z]\d{3}\b", text)
    if roll_match:
        roll_number = roll_match.group()

    # ------------------ NAME ------------------
    name = "Not Found"

    for line in lines[:5]:
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            name = parts[0]
            name = re.sub(r"\b[A-Z]{2}\d{2}[A-Z]\d{3}\b", "", name).strip()
            break

        if len(line.split()) <= 4 and not any(char.isdigit() for char in line):
            name = line
            break

    # ------------------ COLLEGE ------------------
    college = "Not Found"

    # 🔥 Strong pattern for IIT/NIT full names
    college_pattern = re.search(
        r"(Indian Institute of Technology\s*[A-Za-z, ]+)", text, re.IGNORECASE
    )

    if college_pattern:
        college = college_pattern.group().strip()
        return name, roll_number, college

    # 🔥 fallback: line-based extraction
    keywords = ["institute", "university", "college", "iit", "nit"]

    for line in lines:
        line_lower = line.lower()

        if any(k in line_lower for k in keywords):

            # remove CGPA, numbers, year
            clean_line = re.sub(r"\d+(\.\d+)?", "", line)
            clean_line = re.sub(r"cgpa|%|year", "", clean_line, flags=re.IGNORECASE)

            # keep only meaningful words
            words = clean_line.split()
            words = [w for w in words if len(w) > 2]

            cleaned = " ".join(words)

            # filter garbage lines
            if len(cleaned.split()) <= 10:
                college = cleaned.strip()
                break

    return name, roll_number, college
