import streamlit as st
from src.analysis.thesis import ThesisEngine

def render_thesis_tab(data, settings):
    st.subheader("📝 Automated Investment Thesis")
    
    # Simple placeholder values for DCF/EVA for the engine
    engine = ThesisEngine(data, 0, data['Net Profit'].iloc[-1])
    score, checks = engine.generate_scorecard()
    
    # Visual Score
    st.write(f"### Final Mountain Score: **{score} / 3**")
    st.progress(score / 3)
    
    # Detailed Verdicts
    for title, msg in checks:
        with st.expander(title):
            st.write(msg)
            
    if score >= 2:
        st.success("🏔️ **Verdict: INVESTABLE GRADE.** The company meets the majority of 'The Mountain Path' quality criteria.")
    else:
        st.error("🚨 **Verdict: AVOID / MONITOR.** Significant fundamental red flags detected in current financials.")
