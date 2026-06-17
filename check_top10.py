import csv
with open("submission.csv") as f:
    rows = list(csv.DictReader(f))
print("Top 10 candidates:")
for r in rows[:10]:
    print(f"  Rank {r['rank']} | score={r['score']} | {r['reasoning'][:80]}")