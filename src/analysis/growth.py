
import pandas as pd
import numpy as np

class GrowthAnalyzer:
    def __init__(self, df):
        self.df = df

    def calculate_cagr(self, series, periods):
        """Calculates CAGR over a specific number of years."""
        if len(series) < periods + 1:
            return np.nan
        
        beginning_val = series.iloc[-(periods + 1)]
        ending_val = series.iloc[-1]
        
        if beginning_val <= 0 or ending_val <= 0:
            return np.nan
            
        cagr = (pow((ending_val / beginning_val), 1/periods) - 1) * 100
        return cagr

    def get_growth_summary(self):
        summary = {}
        metrics = ['Sales', 'Net Profit', 'Equity Share Capital']
        years = [3, 5, 10]
        
        for metric in metrics:
            if metric in self.df.columns:
                summary[metric] = {f"{y}Y CAGR": self.calculate_cagr(self.df[metric], y) for y in years}
        
        return pd.DataFrame(summary).T
