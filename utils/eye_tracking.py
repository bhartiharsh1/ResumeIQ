import re


def parse_resume_sections(resume_text):
    """
    Naively slices the resume text into dictionary mapping section names to their body text.
    """
    lines = resume_text.split("\n")

    sections = {
        "Summary": "",
        "Experience": "",
        "Projects": "",
        "Education": "",
        "Skills": "",
        "Certifications": "",
    }

    current_section = "Summary"

    header_patterns = {
        "Experience": ["experience", "work history", "employment", "career history", "positions"],
        "Projects": ["projects", "portfolio", "case studies", "personal projects"],
        "Education": ["education", "academics", "university", "college", "degrees", "academic background"],
        "Skills": ["skills", "technologies", "tools", "competencies", "expertise", "proficiencies", "software", "core competencies"],
        "Certifications": ["certifications", "licenses", "courses"],
    }

    for line in lines:
        line_clean = line.strip().lower()
        if not line_clean:
            continue

        if len(line_clean) < 60:  # Headers are usually short strings
            found_header = False
            # Remove punctuation to ensure clean string matching
            clean_for_match = re.sub(r'[^\w\s]', '', line_clean).strip()
            
            for sec, keywords in header_patterns.items():
                for kw in keywords:
                    if kw in clean_for_match:
                        # Ensure the line mostly consists of the header keyword
                        # e.g., "Professional Experience" -> 2 words, "experience" -> 1 word. 2 <= 1 + 2 (True)
                        # "I have great experience in python" -> 6 words. 6 <= 1 + 2 (False)
                        if len(clean_for_match.split()) <= len(kw.split()) + 2:
                            current_section = sec
                            found_header = True
                            break
                if found_header:
                    break
                    
            if found_header:
                continue

        sections[current_section] += line + "\n"

    return {k: v.strip() for k, v in sections.items() if v.strip()}


def score_section(name, content, target_skills):
    words = len(content.split())
    text_lower = content.lower()

    verbs = [
        "developed",
        "built",
        "designed",
        "implemented",
        "optimized",
        "led",
        "managed",
        "architected",
        "spearheaded",
    ]
    verb_hits = sum(1 for v in verbs if v in text_lower)

    metric_hits = sum(1 for char in content if char.isdigit() or char == "%")

    # Target skills check
    skill_hits = sum(1 for s in target_skills if s.lower() in text_lower)

    score = 0
    feedback = []

    if name == "Summary":
        score = 60 + (skill_hits * 10)
        if skill_hits > 0:
            feedback.append(f"Good keyword integration ({skill_hits} hits).")
        else:
            feedback.append("Generic summary. Lacks hard skills.")

    elif name == "Experience":
        score = 40 + (metric_hits * 2) + (verb_hits * 4) + (skill_hits * 15)
        if metric_hits < 5:
            feedback.append(f"Low metrics density ({metric_hits} nums/%).")
        else:
            feedback.append(f"Strong measurable impact ({metric_hits} metrics).")
        if verb_hits < 3:
            feedback.append("Weak action verbs.")

    elif name == "Projects":
        score = 45 + (metric_hits * 2) + (skill_hits * 15)
        if skill_hits > 2:
            feedback.append(f"Highly relevant project ({skill_hits} tools).")
        else:
            feedback.append("Lacks explicit tooling/keywords.")

    elif name == "Skills":
        score = 30 + (skill_hits * 20)
        if skill_hits == 0:
            feedback.append("Critically missing target profile keywords.")
        else:
            feedback.append(f"Found {skill_hits} exact target profile keywords.")

    elif name == "Education":
        score = 50  # Usually quickly glanced at
        feedback.append("Standard academic scanning.")

    elif name == "Certifications":
        score = 60
        feedback.append("Bonus validation points noticed.")

    else:
        score = 30
        feedback.append("Unstructured data block.")

    score = min(max(score, 10), 100)

    # Heatmap Colors
    if score >= 80:
        color = "#ff4b4b"  # Red
        bg_col = "rgba(255, 75, 75, 0.1)"
        label = "High Attention (Red)"
    elif score >= 55:
        color = "#ffcc00"  # Yellow
        bg_col = "rgba(255, 204, 0, 0.1)"
        label = "Medium Attention (Yellow)"
    else:
        color = "#808080"  # Grey
        bg_col = "rgba(128, 128, 128, 0.1)"
        label = "Ignored (Grey)"

    return {
        "score": round(score, 1),
        "color": color,
        "bg_col": bg_col,
        "label": label,
        "words": words,
        "feedback": " ".join(feedback),
    }


def generate_eye_tracking_data(resume_text, target_skills):
    sections = parse_resume_sections(resume_text)
    eye_tracking = {}

    for sec_name, content in sections.items():
        if not content:
            continue
            
        # Split into distinct lines to preserve formatting
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        
        # Fallback: If the block is one giant string without newlines, split by periods to ensure full sentences
        if len(lines) == 1 and len(lines[0]) > 250:
            lines = [s.strip() + "." for s in lines[0].split(". ") if s.strip()]
            
        # Capture full lines/sentences until we hit a reasonable preview length
        preview_lines = []
        char_count = 0
        for line in lines:
            preview_lines.append(line)
            char_count += len(line)
            if char_count >= 200:
                break
                
        preview = "<br/>".join(preview_lines)
        if len(preview_lines) < len(lines):
            preview += "<br/><span style='opacity: 0.6;'><em>... (section continues)</em></span>"
            
        tracker = score_section(sec_name, content, target_skills)
        tracker["preview"] = preview
        eye_tracking[sec_name] = tracker

    return eye_tracking
