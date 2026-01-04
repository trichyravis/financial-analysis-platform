
"""
eva.py - Economic Value Added Engine
🏔️ THE MOUNTAIN PATH - World of Finance
"""

import pandas as pd
import numpy as np

class EVAAnalyzer:
    def __init__(self, df, wacc=0.12):
        # Handle tuple input from data_loader if necessary
        self.df = df[0] if isinstance(df, tuple) else df
        self.wacc = wacc

    def calculate_eva(self):
        """Calculates Economic Value Added over historical periods."""
        # Ensure we have a clean DataFrame to work with
        eva_df = pd.DataFrame(index=self.df.index)
        
        # Use .get() with a default of 0 to prevent KeyErrors
        # Title Case matches the UniversalScreenerLoader output
        pbt = self.df.get('Profit Before Tax', 0)
        interest = self.df.get('Interest', 0)
        depreciation = self.df.get('Depreciation', 0)
        
        # 1. Calculate NOPAT (Net Operating Profit After Tax)
        # Standard effective tax rate assumption (25% for Indian Corporates)
        tax_rate = 0.25 
        ebit = pbt + interest
        nopat = ebit * (1 - tax_rate)
        
        # 2. Calculate Invested Capital
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        debt = self.df.get('Borrowings', 0)
        invested_capital = equity + debt
        
        # 3. Calculate EVA
        capital_charge = invested_capital * self.wacc
        eva_value = nopat - capital_charge
        
        # 4. Compile Results
        eva_df['Report Date'] = self.df.get('Report Date', self.df.index)
        eva_df['NOPAT'] = nopat
        eva_df['Invested Capital'] = invested_capital
        eva_df['Capital Charge'] = capital_charge
        eva_df['EVA'] = eva_value
        
        # ROIC % = NOPAT / Invested Capital
        eva_df['ROIC %'] = (nopat / invested_capital.replace(0, np.nan)) * 100
        
        return eva_df
