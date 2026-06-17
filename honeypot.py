# honeypot.py
from dateutil.parser import parse

# Companies known to be young (founded ~2019 or later)
# We'll use a heuristic instead — check if claimed experience > career dates

def get_career_span_years(career_history):
    """Calculate actual years from career history dates."""
    all_dates = []
    for role in career_history:
        try:
            all_dates.append(parse(role["start_date"]))
        except:
            pass
    if not all_dates:
        return None
    earliest = min(all_dates)
    from datetime import datetime
    span = (datetime.now() - earliest).days / 365
    return round(span, 1)

def has_impossible_experience(profile, career_history):
    """Flag if claimed YOE is much more than actual career span."""
    claimed = profile.get("years_of_experience", 0)
    actual = get_career_span_years(career_history)
    if actual is None:
        return False
    # Allow 2 year buffer (internships, gaps etc.)
    return claimed > actual + 2

def has_expert_skills_no_duration(skills):
    """Flag if many skills are 'expert' but duration_months is 0."""
    expert_no_duration = [
        s for s in skills
        if s.get("proficiency") == "expert" and s.get("duration_months", 1) == 0
    ]
    return len(expert_no_duration) >= 4

def is_honeypot(candidate):
    """Returns True if candidate looks like a honeypot."""
    profile = candidate["profile"]
    career = candidate["career_history"]
    skills = candidate.get("skills", [])

    if has_impossible_experience(profile, career):
        return True
    if has_expert_skills_no_duration(skills):
        return True
    return False