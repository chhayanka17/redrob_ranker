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


def score_skills(skills, assessment_scores=None):
    """Score 0-1 based on skill match, proficiency, duration AND trust."""
    if not skills:
        return 0.0

    if assessment_scores is None:
        assessment_scores = {}

    proficiency_weight = {"expert": 1.0, "advanced": 0.75,
                          "intermediate": 0.5, "beginner": 0.25}
    total, matched = 0.0, 0.0

    for skill in skills:
        name = skill.get("name", "").lower()
        prof = proficiency_weight.get(skill.get("proficiency", "beginner"), 0.25)
        duration = min(skill.get("duration_months", 0) / 24, 1.0)
        endorsements = skill.get("endorsements", 0)
        endorsed_score = min(endorsements / 20, 1.0)

        # --- SKILL TRUST LAYER ---
        trust = 1.0

        # Platform assessment score boosts trust
        for assess_name, assess_score in assessment_scores.items():
            if any(kw in assess_name.lower() for kw in name.split()):
                if assess_score > 80:
                    trust *= 1.3  # verified by platform test
                elif assess_score > 60:
                    trust *= 1.1
                break

        # Expert claim with no endorsements and no duration = suspicious
        if skill.get("proficiency") == "expert":
            if endorsements == 0 and skill.get("duration_months", 0) == 0:
                trust *= 0.3  # likely keyword stuffing
            elif endorsements == 0:
                trust *= 0.7  # unverified expert claim

        # Duration validates real usage
        if duration > 0.5:
            trust *= 1.1

        skill_score = (0.4 * prof + 0.3 * duration + 0.3 * endorsed_score) * trust

        if any(kw in name for kw in MUST_HAVE_SKILLS):
            matched += 1.5 * skill_score
        elif any(kw in name for kw in GOOD_TO_HAVE_SKILLS):
            matched += 0.8 * skill_score
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

from dateutil.parser import parse as parse_date

def score_trajectory(career_history):
    """Score 0-1 based on career growth momentum."""
    if not career_history or len(career_history) < 2:
        return 0.5  # neutral for short careers

    # Sort roles by start date (oldest first)
    try:
        sorted_career = sorted(
            career_history,
            key=lambda r: parse_date(r["start_date"])
        )
    except:
        return 0.5

    SENIORITY_LEVELS = {
        "intern": 0, "trainee": 0, "junior": 1, "associate": 1,
        "engineer": 2, "developer": 2, "analyst": 2, "scientist": 2,
        "senior": 3, "lead": 3, "staff": 3, "principal": 4,
        "manager": 4, "architect": 4, "head": 5, "director": 5,
        "vp": 6, "cto": 7
    }

    def get_level(title):
        title_lower = title.lower()
        best = 2  # default mid-level
        for keyword, level in SENIORITY_LEVELS.items():
            if keyword in title_lower:
                best = max(best, level)
        return best

    levels = [get_level(r["title"]) for r in sorted_career]

    # Count upward moves
    upward = sum(1 for i in range(1, len(levels)) if levels[i] > levels[i-1])
    downward = sum(1 for i in range(1, len(levels)) if levels[i] < levels[i-1])
    lateral = sum(1 for i in range(1, len(levels)) if levels[i] == levels[i-1])

    total_moves = len(levels) - 1
    if total_moves == 0:
        return 0.5

    # Trajectory score
    trajectory = (upward - downward * 0.5) / total_moves

    # Bonus if current role is most senior
    if levels[-1] == max(levels):
        trajectory += 0.2

    return round(min(max(trajectory, 0.0), 1.0), 4)


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
    profile = candidate["profile"]
    career = candidate["career_history"]
    skills = candidate.get("skills", [])
    education = candidate.get("education", [])
    signals = candidate["redrob_signals"]
    assessment_scores = signals.get("skill_assessment_scores", {})

    s_skills      = score_skills(skills, assessment_scores)
    s_career      = score_career(career)
    s_trajectory  = score_trajectory(career)
    s_exp         = score_experience(profile)
    s_edu         = score_education(education)
    s_location    = score_location(profile, signals)

    # Trajectory slightly adjusts career score
    s_career_final = (0.7 * s_career) + (0.3 * s_trajectory)

    final = (
        0.30 * s_career_final +
        0.25 * s_skills       +
        0.20 * s_exp          +
        0.15 * s_location     +
        0.10 * s_edu
    )

    return round(final, 4), {
        "career": s_career_final,
        "skills": s_skills,
        "experience": s_exp,
        "education": s_edu,
        "location": s_location,
        "trajectory": s_trajectory
    }