# Redrob Ranker — Intelligent Candidate Discovery & Ranking

A rule-based AI ranking system that scores 100,000 candidates against a job description the way a great recruiter would — by understanding career substance, not just matching keywords.

## How it works
100K Candidates

↓

Hard Filters        → removes irrelevant titles, low experience, consulting-only, wrong location

↓

Honeypot Detection  → removes fake/impossible profiles

↓

Scoring Engine      → 5-component weighted score per candidate

↓

Behavioral Multiplier → reorders by availability, responsiveness, GitHub activity

↓

Top 100 with reasoning

## Scoring Components

| Component | Weight | What it measures |
|---|---|---|
| Career Substance | 30% | Product company experience, ranking/search/recommendation work |
| Skills Match | 25% | Skill depth, proficiency, duration, endorsements |
| Experience Fit | 20% | Sweet spot 5-9 years for Senior AI Engineer role |
| Location | 15% | Pune/Noida preference, relocation willingness |
| Education | 10% | Institution tier |

## Behavioral Signals (multiplier)

After scoring, each candidate's score is multiplied by an availability factor based on:
- Last active date (inactive 6+ months = 0.4x penalty)
- Open to work flag
- Recruiter response rate
- Notice period
- Interview completion rate
- GitHub activity score
- Email/phone verification

## How to run

```bash
pip install -r requirements.txt
python rank.py --candidates candidates.jsonl --out submission.csv
python validate_submission.py submission.csv
```

## Project Structure
redrob_ranker/

├── rank.py          # Main pipeline

├── filters.py       # Hard filters — title, experience, location, consulting

├── honeypot.py      # Honeypot detection — impossible profiles

├── scorer.py        # 5-component scoring engine

├── signals.py       # Behavioral multiplier

├── reasoning.py     # Reasoning string generator

├── validate_submission.py  # Format validator (provided by organizers)

└── requirements.txt

## Tech stack
- Python 3.11+
- pandas, tqdm, python-dateutil
- No LLM API calls during ranking (fully offline, CPU only)
- Runs in ~1 second on 100K candidates

## AI Tools Used
- Claude (architecture discussion, code review)
- No candidate data was fed to any LLM
