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

    # 🔥 Strong pattern for prominent institutes (captures rest of the line)
    strong_patterns = [
        r"(Indian Institute of Technology[^\n\|]*)",
        r"(National Institute of Technology[^\n\|]*)",
        r"(Birla Institute of Technology[^\n\|]*)",
        r"(International Institute of Information Technology[^\n\|]*)"
    ]

    for pat in strong_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            found = match.group(1).strip()
            found = re.sub(r"[,;\-\(\)]+$", "", found).strip()
            return name, roll_number, found

    # 🔥 fallback: line-based extraction
    keywords = ["institute", "university", "college", "iit ", "nit ", "bits "]
    ignore_words = ["drdo", "project", "intern", "internship", "directorate", "summer", "experience", "school", "high school", "secondary", "pvt", "ltd", "private", "limited", "company"]

    for line in lines:
        line_lower = line.lower()

        if any(ignore in line_lower for ignore in ignore_words):
            continue

        if any(k in line_lower for k in keywords):
            # Split by pipes or common separators to isolate the college name
            parts = [p.strip() for p in re.split(r'[\|]', line)]
            best_part = line
            for part in parts:
                if any(k in part.lower() for k in keywords):
                    best_part = part
                    break

            # remove CGPA, numbers, year, grades
            clean_line = re.sub(r"\b\d+(\.\d+)?\b", "", best_part)
            clean_line = re.sub(r"cgpa|gpa|%|year|grade", "", clean_line, flags=re.IGNORECASE)

            # keep only meaningful words
            words = clean_line.split()
            words = [w for w in words if len(w) > 2 or w.lower() in ["of", "at"]]
            cleaned = " ".join(words).strip()
            
            # Clean up trailing punctuation
            cleaned = re.sub(r"[,;\-\(\)]+$", "", cleaned).strip()

            # filter garbage lines
            if 2 <= len(cleaned.split()) <= 12:
                college = cleaned
                break

    return name, roll_number, college
