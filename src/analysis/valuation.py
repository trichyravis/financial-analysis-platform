
import numpy as np
import pandas as pd

def calculate_dcf(fcf, growth_rate, wacc, terminal_growth):
    """
    Calculates 2-Stage DCF with institutional safety guardrails.
    """
    # 1. Logic Guard: Denominator must be positive
    if wacc <= terminal_growth:
        return 0.0
    
    # 2. Stage 1: 5-Year Explicit Projection
    projections = []
    current_fcf = fcf
    for i in range(1, 6):
        current_fcf *= (1 + growth_rate)
        discounted_fcf = current_fcf / ((1 + wacc) ** i)
        projections.append(discounted_fcf)
    
    pv_explicit_period = sum(projections)
    
    # 3. Stage 2: Terminal Value (Gordon Growth Method)
    fcf_year_5 = current_fcf
    terminal_value = (fcf_year_5 * (1 + terminal_growth)) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + wacc) ** 5)
    
    # 4. Total Intrinsic Value
    intrinsic_value = pv_explicit_period + pv_terminal_value
    
    # Final Floor: Professional models do not show negative intrinsic value
    return max(0, intrinsic_value)

def get_sensitivity_matrix(fcf, growth_range, wacc_range, terminal_growth):
    """
    Generates a DataFrame of fair values based on varying WACC and Growth.
    """
    results = {}
    
    for g in growth_range:
        column_results = []
        for w in wacc_range:
            val = calculate_dcf(fcf, g, w, terminal_growth)
            column_results.append(val)
        results[g] = column_results
        
    return pd.DataFrame(results, index=wacc_range)
