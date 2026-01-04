
import pandas as pd
import numpy as np

class EVAAnalyzer:
    def __init__(self, df, wacc=0.12):
        self.df = df
        self.wacc = wacc

    def calculate_eva(self):
        """Calculates Economic Value Added over historical periods."""
        eva_df = pd.DataFrame(index=self.df.index)
        eva_df['Report Date'] = self.df['Report Date']

        # Use standardized Title Case names
        pbt = self.df.get('Profit Before Tax', 0)
        interest = self.df.get('Interest', 0)
        tax_rate = 0.25  # Standard effective tax rate assumption
        
        # NOPAT = EBIT * (1 - Tax)
        ebit = pbt + interest
        nopat = ebit * (1 - tax_rate)
        
        # Invested Capital = Equity + Reserves + Borrowings
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        debt = self.df.get('Borrowings', 0)
        invested_capital = equity + debt
        
        # Capital Charge = Invested Capital * WACC
        capital_charge = invested_capital * self.wacc
        
        eva_df['NOPAT'] = nopat
        eva_df['Capital Charge'] = capital_charge
        eva_df['EVA'] = nopat - capital_charge
        
        # Return on Invested Capital (ROIC)
        eva_df['ROIC %'] = (nopat / invested_capital.replace(0, np.nan)) * 100
        
        return eva_df.set_index('Report Date')
