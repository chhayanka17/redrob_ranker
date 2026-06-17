# 🎯 Redrob Intelligent Candidate Ranker

> Ranking candidates the way a great recruiter would — by career substance, not keyword density.

![Python](https://img.shields.io/badge/Python-3.14-blue) ![Status](https://img.shields.io/badge/Status-Submission%20Ready-brightgreen) ![Hackathon](https://img.shields.io/badge/India%20Runs-Track%2001-purple)

---

## 🧠 How It Works
100K Candidates

↓

🔍 Hard Filters         → removes wrong titles, low experience, consulting-only, wrong location

↓

🚨 Honeypot Detection   → removes fake/impossible profiles

↓

📊 Scoring Engine       → 5-component weighted score per candidate

↓

📡 Behavioral Signals   → reorders by availability, responsiveness, GitHub activity

↓

🏆 Top 100 with Reasoning

---

## 📊 Scoring Components

| Component | Weight | What It Measures |
|---|---|---|
| 🏢 Career Substance | 30% | Product company experience, ranking/search/recommendation work |
| 🛠️ Skills Match | 25% | Skill depth, proficiency, duration, trust score |
| 📅 Experience Fit | 20% | Sweet spot 5–9 years for Senior AI Engineer role |
| 📍 Location | 15% | Pune/Noida preference, relocation willingness |
| 🎓 Education | 10% | Institution tier |

---

## 📡 Behavioral Multiplier

After scoring, each candidate's score is adjusted by an availability factor based on:

- 🕐 **Last active date** — inactive 6+ months = 0.4× penalty
- ✅ **Open to work flag** — direct availability boost
- 📬 **Recruiter response rate** — ghosting risk detection
- ⏱️ **Notice period** — sub-30 days gets priority
- 🎯 **Interview completion rate** — reliability signal
- 💻 **GitHub activity score** — validates real engineering work
- 📧 **Email/phone verification** — basic credibility check

---

## 🚀 Unique Differentiators

Things most rankers won't do:

- **📈 Career Trajectory Scoring** — rewards Engineer → Senior → Lead growth, not just current title
- **🔒 Skill Trust Layer** — platform assessment scores validate expert claims; unendorsed expert skills flagged as suspicious
- **💬 Recruiter-Quality Reasoning** — specific strengths and concerns per candidate, not generic summaries
- **🚨 Honeypot Detection** — flags impossible experience timelines before scoring

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python rank.py --candidates candidates.jsonl --out submission.csv
python validate_submission.py submission.csv
```

---

## 📁 Project Structure
redrob_ranker/

├── 🚀 rank.py                  # Main pipeline

├── 🔍 filters.py               # Hard filters — title, experience, location, consulting

├── 🚨 honeypot.py              # Honeypot detection — impossible profiles

├── 📊 scorer.py                # 5-component scoring engine + trajectory + trust

├── 📡 signals.py               # Behavioral multiplier

├── 💬 reasoning.py             # Recruiter-quality reasoning generator

├── ✅ validate_submission.py   # Format validator (provided by organizers)

└── 📦 requirements.txt

---

## ⚡ Performance

- ✅ 100,000 candidates processed in **~2 seconds**
- ✅ 9,403 candidates pass filters
- ✅ 0 API calls during ranking — **fully offline, CPU only**
- ✅ Runs well within 5-minute and 16GB RAM constraints

---

## 🛠️ Tech Stack

- Python 3.14
- `pandas`, `tqdm`, `python-dateutil`, `streamlit`
- No LLM during ranking — fully rule-based and reproducible

---

## 🌐 Live Demo

**[▶️ Try the Streamlit Sandbox](https://redrobranker-v2ljj6dvmzaxpcqmxlpmr5.streamlit.app/)**

Upload any candidates JSON file and see the ranking live.

---

## 🤖 AI Tools Used

Claude was used for architecture discussion and code review. No candidate data was fed to any LLM. All ranking logic is original code running fully offline.
