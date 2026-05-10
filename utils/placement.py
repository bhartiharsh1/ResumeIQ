def calculate_placement_probability(format_score, skill_score, impact_score):
    """
    Transforms raw ATS scores into a realistic probabilistic prediction of getting shortlisted.
    Uses a Balanced Weighting model representing genuine algorithmic recruitment:
    30% Formatting | 45% Hard Skill Keywords | 25% Measurable Impact.
    """

    # Calculate holistic probability using real-world recruitment weights
    # 50% Formatting | 35% Hard Skill Keywords | 15% Measurable Impact.
    probability = (format_score * 0.50) + (skill_score * 0.35) + (impact_score * 0.15)

    # To ensure it accurately reflects real placement odds, we curve it slightly 
    # to elevate the floor if the core formatting is highly parsable.
    probability = (probability * 0.7) + (format_score * 0.3)

    # Prevent edge cases from showing perfect 100s or breaking
    # Strictly enforced user requirement: Probability can never exceed base formatting!
    probability = min(max(probability, 1.0), format_score)

    # Categorization tiers based on competitive applicant pool benchmarks
    if probability < 55:
        tier = "Below Average"
    elif probability < 70:
        tier = "Average Candidate"
    elif probability < 85:
        tier = "Above Average"
    else:
        tier = "Top-Tier Candidate"

    # Multi-Tiered Diagnostic Insight Engine
    insights = []

    if format_score < 70:
        insights.append(
            f"🔧 **Structure Issue**: Formatting is critically low ({format_score}/100). Ensure standard sections (Education, Experience, Skills) and clear contact info exist."
        )
    elif format_score < 85:
        insights.append(
            f"📏 **Formatting**: Structure is acceptable ({format_score}/100), but standardizing headers will raise your absolute probability ceiling."
        )

    if skill_score < 40:
        insights.append(
            "⚠️ **Keyword Gap**: Missing critical hard skills for this profile. "
            "Inject exact keywords from the target job description to pass ATS filters."
        )
    elif skill_score < 75:
        insights.append(
            f"🎯 **Skill Alignment**: Match is decent ({skill_score:.0f}/100), "
            "but weaving 2-3 more profile-specific tools into your bullets will spike your odds."
        )

    if impact_score < 50:
        insights.append(
            f"📉 **Low Human Impact**: Recruiter appeal is weak ({impact_score}/100). "
            "Add numbers, % improvements, and action verbs to prove your value."
        )
    elif impact_score < 80:
        insights.append(
            "📈 **Elevate Achievements**: Convert descriptive duties into "
            "quantified accomplishments to maximize your recruiter shortlist appeal."
        )

    # Failsafe if everything is somehow perfect
    if not insights:
        insights.append(
            "✨ **Flawless Execution**: Your structural, skill, and impact vectors are all elite. You are hyper-optimized for shortlisting."
        )

    final_insights = "\n\n".join(insights)

    return {
        "probability": round(probability, 1),
        "tier": tier,
        "insight": final_insights,
    }
