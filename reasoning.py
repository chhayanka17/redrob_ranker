# reasoning.py

def generate_reasoning(candidate, score, breakdown):
    p = candidate["profile"]
    s = candidate["redrob_signals"]
    skills = candidate.get("skills", [])

    title = p.get("current_title", "Unknown")
    years = p.get("years_of_experience", 0)
    company = p.get("current_company", "Unknown")
    location = p.get("location", "Unknown")
    notice = s.get("notice_period_days", 99)
    active = s.get("last_active_date", "")
    github = s.get("github_activity_score", -1)
    open_to_work = s.get("open_to_work_flag", False)
    response_rate = s.get("recruiter_response_rate", 0)
    interview_rate = s.get("interview_completion_rate", 0)
    verified = s.get("verified_email") and s.get("verified_phone")

    # Get top 3 relevant skills
    relevant_keywords = {
        "python", "machine learning", "deep learning", "nlp",
        "embeddings", "vector", "recommendation", "search",
        "ranking", "pytorch", "tensorflow", "faiss", "qdrant"
    }
    top_skills = [
        s_item["name"] for s_item in skills
        if any(kw in s_item["name"].lower() for kw in relevant_keywords)
        and s_item.get("proficiency") in ["advanced", "expert"]
    ][:3]

    # Build strengths
    strengths = []
    if breakdown["career"] > 0.5:
        strengths.append(f"proven product-company background in ranking/search")
    if breakdown["skills"] > 0.4 and top_skills:
        strengths.append(f"strong in {', '.join(top_skills)}")
    if breakdown["experience"] >= 1.0:
        strengths.append(f"{years}yr experience in sweet spot for this role")
    if open_to_work:
        strengths.append("actively looking")
    if notice <= 15:
        strengths.append(f"immediately available ({notice}-day notice)")
    elif notice <= 30:
        strengths.append(f"available in {notice} days")
    if github > 70:
        strengths.append(f"active GitHub contributor (score {github})")
    if response_rate > 0.7:
        strengths.append("highly responsive to recruiters")

    # Build concerns
    concerns = []
    if not open_to_work:
        concerns.append("not actively looking")
    if notice > 60:
        concerns.append(f"long notice period ({notice} days)")
    if github == -1:
        concerns.append("no GitHub linked")
    if response_rate < 0.3:
        concerns.append("low recruiter response rate")
    if interview_rate < 0.5:
        concerns.append("poor interview completion history")

    # Compose final reasoning
    base = f"{years}yr {title} at {company} ({location})"

    if strengths:
        strength_str = "; ".join(strengths)
        result = f"{base}. Strengths: {strength_str}."
    else:
        result = f"{base}."

    if concerns:
        concern_str = ", ".join(concerns)
        result += f" Watch out: {concern_str}."

    return result