def generate_shortcut_roadmap(
    ats_data, missing_skills, impact_score, current_prob, required_prob=85.0
):
    """
    Analyzes current resume deficiencies and generates an optimized, ordered roadmap
    to hit a target placement probability threshold by prioritizing Maximum Gain against Minimum Effort.
    """
    if current_prob >= required_prob:
        return {"status": "Complete", "roadmap": []}

    actions = []

    # 1. Structural Checks
    if not ats_data["sections"].get("projects"):
        actions.append(
            {
                "task": "Add a dedicated Projects section with at least 1 technical project.",
                "gain": 8.0,
                "time_str": "1 week",
                "minutes": 2400,
                "type": "High Effort",
            }
        )

    if not ats_data["sections"].get("experience"):
        actions.append(
            {
                "task": "Add an Experience or Internships section. Even relevant academic capstones count.",
                "gain": 12.0,
                "time_str": "1-2 weeks",
                "minutes": 4800,
                "type": "High Effort",
            }
        )

    if not ats_data["sections"].get("education"):
        actions.append(
            {
                "task": "Add your Education details (University, Degree, Grad Year).",
                "gain": 5.0,
                "time_str": "10 mins",
                "minutes": 10,
                "type": "Quick Win",
            }
        )

    if not ats_data["contact"].get("linkedin"):
        actions.append(
            {
                "task": "Add your LinkedIn profile URL securely to your header.",
                "gain": 3.0,
                "time_str": "5 mins",
                "minutes": 5,
                "type": "Quick Win",
            }
        )

    # 2. Skill Density Checks
    if missing_skills:
        top_skills = ", ".join(missing_skills[:3])
        actions.append(
            {
                "task": f"Inject critically missing hard keyword skills: {top_skills}.",
                "gain": 14.5,
                "time_str": "20 mins",
                "minutes": 20,
                "type": "Quick Win",
            }
        )

    # 3. Recruiter Impact Checks
    metrics_count = ats_data.get("metrics", 0)
    if metrics_count < 5:
        actions.append(
            {
                "task": f"Add quantified metrics (%, $) to your bullets. The system only found {metrics_count} numbers mapped to impact.",
                "gain": 6.0,
                "time_str": "45 mins",
                "minutes": 45,
                "type": "Medium Effort",
            }
        )

    if impact_score < 75:
        actions.append(
            {
                "task": "Upgrade generic phrasing into powerful achievements starting with strong action verbs.",
                "gain": 7.5,
                "time_str": "1 hour",
                "minutes": 60,
                "type": "Medium Effort",
            }
        )

    # 4. Parsing Constraints
    if ats_data.get("length_score", 100) < 100:
        actions.append(
            {
                "task": "Optimize resume length. Target approximately 400-800 words for ideal data extraction.",
                "gain": 4.0,
                "time_str": "30 mins",
                "minutes": 30,
                "type": "Medium Effort",
            }
        )

    # GREEDY OPTIMIZATION: Sort by Return On Investment (Score Gain per Minute of Effort)
    actions.sort(key=lambda x: x["gain"] / max(1, x["minutes"]), reverse=True)

    selected_actions = []
    accumulated_gain = 0.0

    for action in actions:
        if current_prob + accumulated_gain >= required_prob:
            break
        selected_actions.append(action)
        accumulated_gain += action["gain"]

    # Failsafe if the candidate is extremely far behind but we exhausted logical quick-actions
    if not selected_actions and actions:
        selected_actions = actions[:2]
        accumulated_gain = sum(a["gain"] for a in selected_actions)

    return {
        "status": "Roadmap",
        "target": required_prob,
        "total_gain": accumulated_gain,
        "actions": selected_actions,
    }
