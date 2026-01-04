
import streamlit as st
from src.analysis.financial import FinancialAnalyzer

def render_profitability_tab(data):
    """Renders detailed margin and return analysis."""
    st.subheader("📉 Profitability & Efficiency Analysis")
    
    analyzer = FinancialAnalyzer(data)
    metrics_df = analyzer.get_profitability_metrics()
    
    # Margin Analysis
    st.write("#### Margin Trends (%)")
    margin_cols = ['Gross Margin %', 'EBITDA Margin %', 'Net Margin %']
    st.area_chart(metrics_df.set_index('Year')[margin_cols])
    
    # Return Ratios Table
    st.write("#### Historical Return Ratios")
    formatted_df = metrics_df[['Year', 'ROE %', 'ROCE %']].copy()
    formatted_df['ROE %'] = formatted_df['ROE %'].map('{:.2f}%'.format)
    formatted_df['ROCE %'] = formatted_df['ROCE %'].map('{:.2f}%'.format)
    
    st.table(formatted_df)
    
    # Key Insight
    latest_roe = metrics_df.iloc[-1]['ROE %']
    if latest_roe > 20:
        st.success(f"🌟 High Capital Efficiency: Current ROE is {latest_roe:.2f}%")
    elif latest_roe < 10:
        st.warning(f"⚠️ Capital Efficiency Concern: Current ROE is {latest_roe:.2f}%")
