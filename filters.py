# filters.py

CONSULTING_FIRMS = {
    "tcs", "tata consultancy", "infosys", "wipro", "accenture",
    "cognizant", "capgemini", "hcl", "tech mahindra", "mphasis",
    "hexaware", "ltimindtree", "persistent systems", "niit technologies",
    "syntel", "patni", "mastech", "kpit", "mindtree"
}

UNRELATED_TITLE_KEYWORDS = {
    "marketing", "sales", "hr", "human resource", "finance",
    "accountant", "recruiter", "lawyer", "content writer",
    "graphic designer", "business development", "operations manager",
    "supply chain", "procurement", "legal","business analyst", "civil engineer",                                                                  
    "frontend engineer","mobile engineer", "ios engineer", "android engineer",
    "qa engineer", "test engineer", "scrum master", "product manager"
}

AI_RELATED_KEYWORDS = {
    "machine learning", "ml", "ai", "data science", "deep learning",
    "nlp", "computer vision", "engineer", "developer", "architect",
    "analyst", "researcher", "scientist"
}

def is_consulting_only(career_history):
    """True only if EVERY role is at a consulting firm."""
    for role in career_history:
        company = role.get("company", "").lower()
        if not any(firm in company for firm in CONSULTING_FIRMS):
            return False  # at least one non-consulting role → keep
    return True

# Add this new set at the top
AI_ENGINEERING_KEYWORDS = {
    "machine learning", "ml engineer", "data scientist", "data science",
    "ai engineer", "deep learning", "nlp", "computer vision",
    "software engineer", "software developer", "backend engineer",
    "data engineer", "research scientist", "applied scientist",
    "recommendation", "search engineer", "platform engineer",
    "full stack", "fullstack", "python developer", "cloud engineer",
    "devops", "infrastructure engineer", "site reliability",
    "solutions architect", "tech lead", "engineering manager"
}

def has_relevant_title(profile):
    """Keep only titles that are clearly tech/AI/engineering relevant."""
    title = profile.get("current_title", "").lower()
    
    # First block obvious misfits
    if any(kw in title for kw in UNRELATED_TITLE_KEYWORDS):
        return False
    
    # Then require at least one AI/engineering keyword
    if any(kw in title for kw in AI_ENGINEERING_KEYWORDS):
        return True
    
    # Anything else (Project Manager, Mechanical Engineer etc.) → reject
    return False

def has_min_experience(profile, min_years=3):
    """False if under 3 years experience."""
    return profile.get("years_of_experience", 0) >= min_years

def is_india_eligible(profile, signals):
    """False if outside India and not willing to relocate."""
    country = profile.get("country", "").lower()
    willing = signals.get("willing_to_relocate", False)
    if country != "india" and not willing:
        return False
    return True

def apply_hard_filters(candidates):
    """Run all filters. Returns (kept, rejected) lists."""
    kept = []
    rejected = []

    for c in candidates:
        profile = c["profile"]
        career = c["career_history"]
        signals = c["redrob_signals"]

        if not has_min_experience(profile):
            rejected.append(c); continue
        if not has_relevant_title(profile):
            rejected.append(c); continue
        if is_consulting_only(career):
            rejected.append(c); continue
        if not is_india_eligible(profile, signals):
            rejected.append(c); continue

        kept.append(c)

    return kept, rejected