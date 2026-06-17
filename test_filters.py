import json
from filters import apply_hard_filters

with open("sample_candidates.json") as f:
    candidates = json.load(f)

kept, rejected = apply_hard_filters(candidates)

print(f"Total: {len(candidates)}")
print(f"Kept: {len(kept)}")
print(f"Rejected: {len(rejected)}")
print()

# See WHY candidates were rejected
print("=== Sample Rejected ===")
for c in rejected[:5]:
    p = c["profile"]
    print(f"  {p['current_title']} | {p['years_of_experience']}yr | {p['country']}")

print()
print("=== Sample Kept ===")
for c in kept[:5]:
    p = c["profile"]
    print(f"  {p['current_title']} | {p['years_of_experience']}yr | {p['country']}")
   
from honeypot import is_honeypot

honeypots = [c for c in candidates if is_honeypot(c)]
print(f"\nHoneypots found: {len(honeypots)}")
for c in honeypots:
    p = c["profile"]
    print(f"  {p['current_title']} | {p['years_of_experience']}yr claimed")

from scorer import compute_score

print("\n=== Scores for Kept Candidates ===")
for c in kept:
    score, breakdown = compute_score(c)
    print(f"  {c['profile']['current_title']:35} | score={score} | {breakdown}")

from signals import apply_signals

print("\n=== After Behavioral Multiplier ===")
for c in kept:
    base_score, breakdown = compute_score(c)
    final_score = apply_signals(base_score, c["redrob_signals"])
    signals = c["redrob_signals"]
    print(f"  {c['profile']['current_title']:35} | base={base_score} → final={final_score} | active={signals['last_active_date']} | open={signals['open_to_work_flag']}")