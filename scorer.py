# scorer.py

MUST_HAVE_SKILLS = {
    "python", "machine learning", "deep learning", "nlp",
    "embeddings", "vector database", "faiss", "qdrant", "pinecone",
    "recommendation system", "search", "ranking", "retrieval",
    "pytorch", "tensorflow", "transformers", "bert", "llm"
}

GOOD_TO_HAVE_SKILLS = {
    "lora", "qlora", "fine-tuning", "rag", "langchain",
    "spark", "kafka", "redis", "elasticsearch", "aws", "gcp",
    "docker", "kubernetes", "airflow", "mlflow", "sql"
}

PRODUCT_COMPANY_HINTS = {
    "flipkart", "swiggy", "zomato", "ola", "cred", "razorpay",
    "paytm", "meesho", "dream11", "phonepe", "zepto", "blinkit",
    "myntra", "nykaa", "urban company", "lenskart", "groww",
    "startup", "product", "saas", "platform", "app"
}

CONSULTING_FIRMS = {
    "tcs", "infosys", "wipro", "accenture", "cognizant",
    "capgemini", "hcl", "tech mahindra", "mphasis", "hexaware"
}

RANKING_KEYWORDS = {
    "ranking", "recommendation", "retrieval", "search", "vector",
    "embedding", "similarity", "matching", "scoring", "ranker",
    "collaborative filtering", "content-based", "hybrid search"
}


def score_skills(skills):
    """Score 0-1 based on skill match, proficiency, and duration."""
    if not skills:
        return 0.0

    proficiency_weight = {"expert": 1.0, "advanced": 0.75,
                          "intermediate": 0.5, "beginner": 0.25}
    total, matched = 0.0, 0.0

    for skill in skills:
        name = skill.get("name", "").lower()
        prof = proficiency_weight.get(skill.get("proficiency", "beginner"), 0.25)
        duration = min(skill.get("duration_months", 0) / 24, 1.0)  # cap at 24 months
        endorsements = min(skill.get("endorsements", 0) / 20, 1.0)  # cap at 20

        trust = (0.5 * prof) + (0.3 * duration) + (0.2 * endorsements)

        if any(kw in name for kw in MUST_HAVE_SKILLS):
            matched += 1.5 * trust  # bonus for must-have
        elif any(kw in name for kw in GOOD_TO_HAVE_SKILLS):
            matched += 0.8 * trust
        total += 1.0

    return min(matched / max(total, 1), 1.0)


def score_career(career_history):
    """Score 0-1 based on career substance — product companies + ranking work."""
    if not career_history:
        return 0.0

    product_score = 0.0
    ranking_score = 0.0

    for role in career_history:
        company = role.get("company", "").lower()
        description = role.get("description", "").lower()
        duration = role.get("duration_months", 0)
        weight = min(duration / 12, 2.0)  # weight by tenure, cap at 2 years

        # Product company bonus
        if any(hint in company for hint in PRODUCT_COMPANY_HINTS):
            product_score += 0.3 * weight
        # Penalize pure consulting
        if any(firm in company for firm in CONSULTING_FIRMS):
            product_score -= 0.1 * weight

        # Ranking/search/recommendation work bonus
        if any(kw in description for kw in RANKING_KEYWORDS):
            ranking_score += 0.4 * weight

    return min((product_score + ranking_score) / 3, 1.0)


def score_experience(profile):
    """Score 0-1 based on years of experience. Sweet spot: 5-9 years."""
    years = profile.get("years_of_experience", 0)
    if 5 <= years <= 9:
        return 1.0
    elif 4 <= years < 5:
        return 0.8
    elif 9 < years <= 12:
        return 0.7
    elif 3 <= years < 4:
        return 0.5
    else:
        return 0.2


def score_education(education):
    """Score 0-1 based on education tier."""
    if not education:
        return 0.3  # neutral, not a dealbreaker

    tier_scores = {"tier_1": 1.0, "tier_2": 0.7,
                   "tier_3": 0.4, "tier_4": 0.2, "unknown": 0.3}
    best = max(
        tier_scores.get(edu.get("tier", "unknown"), 0.3)
        for edu in education
    )
    return best


def score_location(profile, signals):
    """Score 0-1 based on location fit for Pune/Noida."""
    country = profile.get("country", "").lower()
    location = profile.get("location", "").lower()
    willing = signals.get("willing_to_relocate", False)

    target_cities = {"pune", "noida", "delhi", "gurugram", "gurgaon",
                     "mumbai", "bangalore", "bengaluru", "hyderabad"}

    if any(city in location for city in target_cities):
        return 1.0
    elif country == "india" and willing:
        return 0.7
    elif country == "india":
        return 0.5
    elif willing:
        return 0.3
    return 0.1


def compute_score(candidate):
    """Combine all components into a final weighted score 0-1."""
    profile = candidate["profile"]
    career = candidate["career_history"]
    skills = candidate.get("skills", [])
    education = candidate.get("education", [])
    signals = candidate["redrob_signals"]

    s_skills   = score_skills(skills)
    s_career   = score_career(career)
    s_exp      = score_experience(profile)
    s_edu      = score_education(education)
    s_location = score_location(profile, signals)

    # Weighted combination
    final = (
        0.30 * s_career   +   # most important — substance
        0.25 * s_skills   +   # verified skill depth
        0.20 * s_exp      +   # experience fit
        0.15 * s_location +   # location
        0.10 * s_edu          # education (least important)
    )

    return round(final, 4), {
        "career": s_career,
        "skills": s_skills,
        "experience": s_exp,
        "education": s_edu,
        "location": s_location
    }