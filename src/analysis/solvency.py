
import pandas as pd
import numpy as np

def calculate_solvency(data):
    solvency = pd.DataFrame(index=data['Report Date'])
    
    # Calculate Equity Base
    equity = data['Equity Share Capital'] + data['Reserves']
    
    # 1. Debt to Equity Ratio
    solvency['Debt to Equity'] = data['Borrowings'] / equity
    
    # 2. Interest Coverage Ratio
    # Formula: EBIT / Interest Expense
    ebit = data['Profit Before Tax'] + data['Interest']
    solvency['Interest Coverage'] = ebit / data['Interest'].replace(0, np.nan)
    
    # 3. Proprietary Ratio
    solvency['Proprietary Ratio'] = equity / data['Total Assets']
    
    return solvency
