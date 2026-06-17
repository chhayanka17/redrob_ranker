# reasoning.py

def generate_reasoning(candidate, score, breakdown):
    p = candidate["profile"]
    s = candidate["redrob_signals"]

    title = p.get("current_title", "Unknown")
    years = p.get("years_of_experience", 0)
    company = p.get("current_company", "Unknown")
    location = p.get("location", "Unknown")
    notice = s.get("notice_period_days", "?")
    active = s.get("last_active_date", "?")
    github = s.get("github_activity_score", -1)

    # Build reasoning from actual data points
    parts = []
    parts.append(f"{years}yr {title} at {company} ({location})")

    if breakdown["career"] > 0.5:
        parts.append("strong product/ranking background")
    if breakdown["skills"] > 0.5:
        parts.append("deep ML/search skills")
    if notice <= 30:
        parts.append(f"available in {notice} days")
    elif notice > 60:
        parts.append(f"long notice period ({notice} days)")
    if github > 70:
        parts.append("active GitHub contributor")
    if not s.get("open_to_work_flag"):
        parts.append("not actively looking")

    return "; ".join(parts) + "."