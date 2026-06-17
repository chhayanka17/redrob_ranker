# rank.py
import json
import csv
import gzip
import argparse
from tqdm import tqdm

from filters import apply_hard_filters
from honeypot import is_honeypot
from scorer import compute_score
from signals import apply_signals
from reasoning import generate_reasoning

def load_candidates(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rt") as f:
            return [json.loads(line) for line in f if line.strip()]
    elif path.endswith(".jsonl"):
        with open(path, "r") as f:
            return [json.loads(line) for line in f if line.strip()]
    elif path.endswith(".json"):
        with open(path, "r") as f:
            return json.load(f)

def rank_candidates(candidates):
    # Step 1 — Hard filters
    kept, _ = apply_hard_filters(candidates)
    print(f"After filters: {len(kept)} / {len(candidates)}")

    # Step 2 — Remove honeypots
    clean = [c for c in kept if not is_honeypot(c)]
    print(f"After honeypot removal: {len(clean)}")

    # Step 3 — Score each candidate
    scored = []
    for c in tqdm(clean, desc="Scoring"):
        base_score, breakdown = compute_score(c)
        final_score = apply_signals(base_score, c["redrob_signals"])
        scored.append((c, final_score, breakdown))

    # Step 4 — Sort by final score descending
    scored.sort(key=lambda x: (-x[1], x[0]["candidate_id"]))

    # Step 5 — Take top 100
    top100 = scored[:100]
    return top100

def write_submission(top100, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        
        total = len(top100)
        for rank, (candidate, score, breakdown) in enumerate(top100, start=1):
            # Spread scores naturally: rank 1 = score, rank 100 = score * 0.60
            decay = 1.0 - (rank - 1) * (0.40 / (total - 1))
            final_score = round(score * decay, 4)
            
            reasoning = generate_reasoning(candidate, score, breakdown)
            writer.writerow([
                candidate["candidate_id"],
                rank,
                final_score,
                reasoning
            ])
    print(f"Saved {output_path}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default="sample_candidates.json")
    parser.add_argument("--out", default="submission.csv")
    args = parser.parse_args()

    candidates = load_candidates(args.candidates)
    print(f"Loaded {len(candidates)} candidates")

    top100 = rank_candidates(candidates)
    write_submission(top100, args.out)