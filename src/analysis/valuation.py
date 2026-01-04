
import numpy as np
import pandas as pd

def calculate_dcf(fcf, growth_rate, wacc_decimal, terminal_growth):
    """
    Standard 2-Stage DCF Model
    fcf: Latest Free Cash Flow
    growth_rate: 5Y explicit growth (decimal, e.g., 0.15)
    wacc_decimal: Discount rate (decimal, e.g., 0.10)
    terminal_growth: Perpetuity growth (decimal, e.g., 0.04)
    """
    
    # 1. Guardrail: Prevent negative denominator in Gordon Growth
    if wacc_decimal <= terminal_growth:
        return 0.0
    
    # 2. Stage 1: Explicit 5-Year Projection
    # We project cash flows for 5 years and discount them back to Present Value (PV)
    pv_explicit_flows = 0
    current_fcf = fcf
    
    for year in range(1, 6):
        current_fcf *= (1 + growth_rate)
        discounted_fcf = current_fcf / ((1 + wacc_decimal) ** year)
        pv_explicit_flows += discounted_fcf
    
    # 3. Stage 2: Terminal Value (Gordon Growth Method)
    # This represents all cash flows from Year 6 to infinity
    fcf_year_6 = current_fcf * (1 + terminal_growth)
    terminal_value = fcf_year_6 / (wacc_decimal - terminal_growth)
    
    # Discount Terminal Value back to Year 0
    pv_terminal_value = terminal_value / ((1 + wacc_decimal) ** 5)
    
    # 4. Total Intrinsic Value
    intrinsic_value = pv_explicit_flows + pv_terminal_value
    
    # Final safety check: Valuation cannot be negative
    return max(0, intrinsic_value)

def get_sensitivity_matrix(fcf, growth_range, wacc_range, terminal_growth):
    """
    Generates data for the Heatmap in the UI.
    """
    results = {}
    for g in growth_range:
        column = []
        for w in wacc_range:
            # Calculate fair value for each combination
            val = calculate_dcf(fcf, g, w, terminal_growth)
            column.append(val)
        results[g] = column
        
    return pd.DataFrame(results, index=wacc_range)
