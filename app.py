# app.py
import streamlit as st
import json
import pandas as pd
from filters import apply_hard_filters
from honeypot import is_honeypot
from scorer import compute_score
from signals import apply_signals
from reasoning import generate_reasoning

st.set_page_config(page_title="Redrob Ranker", page_icon="🎯", layout="wide")

st.title("🎯 Redrob Intelligent Candidate Ranker")
st.markdown("Upload a candidates JSON file to get a ranked shortlist — scored by career substance, skills depth, and behavioral signals.")

uploaded_file = st.file_uploader("Upload candidates.json or sample_candidates.json", type=["json"])

if uploaded_file:
    with st.spinner("Loading candidates..."):
        candidates = json.load(uploaded_file)
    st.success(f"Loaded {len(candidates)} candidates")

    if st.button("🚀 Run Ranker"):
        with st.spinner("Filtering..."):
            kept, rejected = apply_hard_filters(candidates)
            clean = [c for c in kept if not is_honeypot(c)]

        st.info(f"After filters: {len(kept)} kept, {len(rejected)} rejected | Honeypots removed: {len(kept) - len(clean)}")

        with st.spinner("Scoring..."):
            scored = []
            for c in clean:
                base_score, breakdown = compute_score(c)
                final_score = apply_signals(base_score, c["redrob_signals"])
                scored.append((c, final_score, breakdown))

            scored.sort(key=lambda x: (-x[1], x[0]["candidate_id"]))
            top = scored[:100]

        # Apply score decay
        total = len(top)
        results = []
        for rank, (c, score, breakdown) in enumerate(top, start=1):
            decay = 1.0 - (rank - 1) * (0.40 / max(total - 1, 1))
            final_score = round(score * decay, 4)
            reasoning = generate_reasoning(c, score, breakdown)
            p = c["profile"]
            results.append({
                "Rank": rank,
                "Score": final_score,
                "Title": p["current_title"],
                "Company": p["current_company"],
                "Experience (yrs)": p["years_of_experience"],
                "Location": p["location"],
                "Reasoning": reasoning
            })

        df = pd.DataFrame(results)

        st.success(f"✅ Top {len(df)} candidates ranked!")
        st.dataframe(df, use_container_width=True)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="ranked_candidates.csv",
            mime="text/csv"
        )

        # Score breakdown chart
        st.subheader("Score Distribution — Top 20")
        st.bar_chart(df.head(20).set_index("Rank")["Score"])