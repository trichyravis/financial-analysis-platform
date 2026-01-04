
import streamlit as st
import pandas as pd
from src.analysis.financial import FinancialAnalyzer

def render_dashboard(data, metadata):
    """
    Renders the institutional dashboard with core KPIs and profitability trends.
    """
    # 1. Initialize Analyzer
    analyzer = FinancialAnalyzer(data)
    
    # 2. Section Header
    st.markdown(f"### 🏔️ Performance Overview: {metadata.get('company_name', 'Company Profile')}")
    
    # 3. Safe Extraction Helper
    # This prevents the 'ValueError' by ensuring we only take 1 column even if duplicates exist
    def get_safe_series(col_name):
        series = data[col_name]
        if isinstance(series, pd.DataFrame):
            return series.iloc[:, 0]
        return series

    # 4. Top KPI Metrics Row
    cols = st.columns(4)
    
    try:
        # Get single series for each metric
        sales = get_safe_series('Sales')
        profit = get_safe_series('Net Profit')
        
        current_price = metadata.get('current_price', 0)
        mcap = metadata.get('market_cap', 0)
        
        # Calculate YoY Growth using the last two available years
        sales_growth = sales.pct_change().iloc[-1] * 100
        profit_growth = profit.pct_change().iloc[-1] * 100

        cols[0].metric("Current Price", f"₹{current_price:,.2f}")
        cols[1].metric("Market Cap", f"₹{mcap:,.0f} Cr")
        cols[2].metric("Sales Growth (YoY)", f"{sales_growth:+.1f}%")
        cols[3].metric("Profit Growth (YoY)", f"{profit_growth:+.1f}%")
    except Exception as e:
        st.error(f"Metric Error: Ensure 'Sales' and 'Net Profit' headers exist in Excel.")

    st.divider()

    # 5. Profitability Trends
    prof_df = analyzer.get_profitability_metrics()
    
    if not prof_df.empty:
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("**Return on Equity (ROE %)**")
            st.line_chart(prof_df.set_index('Year')['ROE %'])
            
        with c2:
            st.write("**Net Profit Margin (%)**")
            st.area_chart(prof_df.set_index('Year')['Net Margin %'])
            
        # Summary Table with High Contrast Formatting
        with st.expander("View Historical Ratios"):
            st.dataframe(
                prof_df.style.format("{:.2f}%", subset=['ROE %', 'Net Margin %']), 
                use_container_width=True
            )

    # 6. Debt Analysis
    st.write("### 🛡️ Solvency Position")
    solvency_df = analyzer.get_solvency_metrics()
    if not solvency_df.empty:
        st.bar_chart(solvency_df.set_index('Year')['Debt-to-Equity'])
        
        latest_de = solvency_df['Debt-to-Equity'].iloc[-1]
        if latest_de > 1.5:
            st.warning(f"High Leverage: D/E is {latest_de:.2f}. Institutional risk threshold exceeded.")
        else:
            st.success(f"Safe Leverage: D/E is {latest_de:.2f}.")
