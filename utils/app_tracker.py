"""app_tracker.py — Local JSON-based application tracker with CRUD + stats."""
import json, os, uuid
from collections import defaultdict

STAGES = ["Applied", "Shortlisted", "Interview", "Offer", "Rejected"]
_DATA = os.path.join(os.path.dirname(__file__), "..", "data", "applications.json")


def load_applications() -> list:
    if not os.path.exists(_DATA):
        return []
    try:
        with open(_DATA, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _save(apps: list):
    os.makedirs(os.path.dirname(_DATA), exist_ok=True)
    with open(_DATA, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)


def add_application(company: str, role: str, resume_version: str,
                    date_applied: str, stage: str = "Applied") -> dict:
    apps = load_applications()
    entry = {"id": str(uuid.uuid4())[:8], "company": company, "role": role,
             "resume_version": resume_version, "date_applied": date_applied, "stage": stage}
    apps.append(entry)
    _save(apps)
    return entry


def update_stage(app_id: str, new_stage: str):
    apps = load_applications()
    for a in apps:
        if a["id"] == app_id:
            a["stage"] = new_stage
            break
    _save(apps)


def delete_application(app_id: str):
    apps = [a for a in load_applications() if a["id"] != app_id]
    _save(apps)


def get_stats(apps: list) -> dict:
    if not apps:
        return {"total": 0, "by_stage": {}, "best_resume": "N/A", "best_rate": 0, "offer_rate": 0}
    by_stage = defaultdict(int)
    by_ver   = defaultdict(lambda: {"total": 0, "positive": 0})
    for a in apps:
        by_stage[a["stage"]] += 1
        v = a.get("resume_version", "Unknown")
        by_ver[v]["total"] += 1
        if a["stage"] in ("Shortlisted", "Interview", "Offer"):
            by_ver[v]["positive"] += 1
    best_v, best_r = "N/A", -1
    for v, c in by_ver.items():
        r = c["positive"] / max(1, c["total"])
        if r > best_r:
            best_r, best_v = r, v
    offers = by_stage.get("Offer", 0)
    return {
        "total":        len(apps),
        "by_stage":     dict(by_stage),
        "best_resume":  best_v,
        "best_rate":    round(best_r * 100, 1),
        "offer_rate":   round(offers / len(apps) * 100, 1),
    }
