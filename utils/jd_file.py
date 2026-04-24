from sentence_transformers import SentenceTransformer
import numpy as np
import re

model = SentenceTransformer("all-mpnet-base-v2")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def split_text(text):
    return [line.strip() for line in text.split("\n") if len(line.strip()) > 20]


def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9+ ]", " ", text.lower())


def extract_keywords(text):
    words = clean_text(text).split()
    return set([w for w in words if len(w) > 3])


def jd_match_final(resume_text, job_description, present_skills, missing_skills):

    # -------- SEMANTIC MATCH --------
    resume_chunks = split_text(resume_text)
    jd_chunks = split_text(job_description)

    if not resume_chunks or not jd_chunks:
        semantic_score = 0
    else:
        resume_emb = model.encode(resume_chunks)
        jd_emb = model.encode(jd_chunks)

        mean_resume_emb = np.mean(resume_emb, axis=0)
        mean_jd_emb = np.mean(jd_emb, axis=0)

        sim = cosine_similarity(mean_resume_emb, mean_jd_emb)
        semantic_score = max(0, float(sim) * 100)

    semantic_score = min(semantic_score, 100)

    # -------- SKILL MATCH --------
    total = len(present_skills) + len(missing_skills)

    if total == 0:
        skill_score = 0
    else:
        skill_score = (len(present_skills) / total) * 100

    # -------- FINAL SCORE --------
    final_score = (0.7 * semantic_score) + (0.3 * skill_score)

    return round(final_score, 2), round(semantic_score, 2), round(skill_score, 2)
