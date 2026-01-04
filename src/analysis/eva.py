import pandas as pd

class EVAAnalyzer:
    """Calculates Economic Value Added and Market Value Added."""
    
    def __init__(self, df, wacc_default=0.10):
        self.df = df
        self.wacc = wacc_default

    def calculate_eva(self):
        """EVA = NOPAT - (Invested Capital * WACC)"""
        # 1. Calculate NOPAT (Assuming 25% tax)
        ebit = self.df['Profit before tax'] + self.df['Interest']
        nopat = ebit * (1 - 0.25)
        
        # 2. Invested Capital
        equity = self.df['Equity Share Capital'] + self.df['Reserves']
        invested_capital = equity + self.df['Borrowings']
        
        # 3. EVA Calculation
        capital_charge = invested_capital * self.wacc
        eva = nopat - capital_charge
        
        results = pd.DataFrame({
            'Year': self.df['Report Date'],
            'NOPAT': nopat,
            'Invested Capital': invested_capital,
            'Capital Charge': capital_charge,
            'EVA': eva,
            'Spread %': (nopat / invested_capital - self.wacc) * 100
        })
        return results
