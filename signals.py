# signals.py
from datetime import datetime

def availability_multiplier(signals):
    """Returns a multiplier 0.3–1.1 based on behavioral signals."""
    multiplier = 1.0

    # 1. Recency — how recently active
    try:
        last_active = datetime.strptime(signals["last_active_date"], "%Y-%m-%d")
        days_inactive = (datetime.now() - last_active).days
        if days_inactive > 180:
            multiplier *= 0.4
        elif days_inactive > 90:
            multiplier *= 0.7
        elif days_inactive <= 30:
            multiplier *= 1.05
    except:
        pass

    # 2. Open to work
    if signals.get("open_to_work_flag"):
        multiplier *= 1.1
    else:
        multiplier *= 0.75

    # 3. Recruiter responsiveness
    response_rate = signals.get("recruiter_response_rate", 0.5)
    if response_rate < 0.2:
        multiplier *= 0.6
    elif response_rate > 0.7:
        multiplier *= 1.05

    # 4. Notice period
    notice = signals.get("notice_period_days", 60)
    if notice <= 15:
        multiplier *= 1.1
    elif notice <= 30:
        multiplier *= 1.05
    elif notice > 90:
        multiplier *= 0.8

    # 5. Interview reliability
    icr = signals.get("interview_completion_rate", 0.8)
    if icr < 0.5:
        multiplier *= 0.7
    elif icr > 0.9:
        multiplier *= 1.05

    # 6. Verification
    if signals.get("verified_email") and signals.get("verified_phone"):
        multiplier *= 1.05

    # 7. GitHub activity (engineering proof)
    github = signals.get("github_activity_score", -1)
    if github > 70:
        multiplier *= 1.1
    elif github == -1:
        multiplier *= 0.95  # no github linked

    return min(multiplier, 1.3)  # cap upside at 1.3


def apply_signals(base_score, signals):
    multiplier = availability_multiplier(signals)
    final = base_score * multiplier
    # Cap at 0.99 so scores spread naturally, never bunch at 1.0
    return round(min(final, 0.99), 4)