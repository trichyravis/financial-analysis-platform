
import numpy as np

def calculate_dcf(fcf, growth_rate, wacc, terminal_growth):
    """
    Calculates 2-Stage DCF with safety guardrails.
    """
    # 1. DENOMINATOR SAFETY CHECK
    # Terminal growth must be strictly less than WACC
    if wacc <= terminal_growth:
        # Fallback: Cap terminal growth at WACC - 2% to prevent negative infinity
        terminal_growth = max(0, wacc - 0.02)
        
    # 2. STAGE 1: 5-YEAR PROJECTION
    projections = []
    current_fcf = fcf
    for i in range(1, 6):
        current_fcf *= (1 + growth_rate)
        discounted_fcf = current_fcf / ((1 + wacc) ** i)
        projections.append(discounted_fcf)
    
    pv_explicit_period = sum(projections)
    
    # 3. STAGE 2: TERMINAL VALUE
    fcf_year_5 = current_fcf
    # Gordon Growth Formula
    terminal_value = (fcf_year_5 * (1 + terminal_growth)) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + wacc) ** 5)
    
    # 4. TOTAL INTRINSIC VALUE
    intrinsic_value = pv_explicit_period + pv_terminal_value
    
    # Final Floor: Intrinsic value cannot be negative in a professional model
    return max(0, intrinsic_value)
