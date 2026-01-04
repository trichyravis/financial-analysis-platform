
import pandas as pd
import numpy as np

def calculate_dcf(latest_fcf, growth_rate, wacc, terminal_growth, projection_years=5):
    """Calculates Intrinsic Value using 2-stage DCF model."""
    forecast_fcf = []
    current_fcf = latest_fcf
    
    # Stage 1: Growth Phase
    for i in range(projection_years):
        current_fcf *= (1 + growth_rate)
        forecast_fcf.append(current_fcf)
        
    # Stage 2: Terminal Value
    terminal_value = (forecast_fcf[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)
    
    # Discounting
    pv_fcf = sum([fcf / (1 + wacc)**(i+1) for i, fcf in enumerate(forecast_fcf)])
    pv_terminal = terminal_value / (1 + wacc)**projection_years
    
    return pv_fcf + pv_terminal

def get_sensitivity_matrix(fcf, growth_range, wacc_range, terminal_growth):
    """Generates data for a heat map of valuations."""
    matrix = np.zeros((len(wacc_range), len(growth_range)))
    for i, w in enumerate(wacc_range):
        for j, g in enumerate(growth_range):
            matrix[i, j] = calculate_dcf(fcf, g, w, terminal_growth)
    return pd.DataFrame(matrix, index=[f"{w*100:.1f}%" for w in wacc_range], 
                        columns=[f"{g*100:.1f}%" for g in growth_range])
