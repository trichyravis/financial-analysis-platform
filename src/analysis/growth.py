
import pandas as pd
import numpy as np

class GrowthAnalyzer:
    def __init__(self, df):
        self.df = df[0] if isinstance(df, tuple) else df

    def calculate_cagr(self, series, periods):
        """Standard CAGR Formula: [(End/Start)^(1/n)] - 1"""
        if len(series) < periods + 1:
            return np.nan
        start_val = series.iloc[-(periods + 1)]
        end_val = series.iloc[-1]
        
        if start_val <= 0 or end_val <= 0:
            return np.nan
            
        return (pow((end_val / start_val), 1/periods) - 1) * 100

    def get_growth_summary(self):
        metrics = ['Sales', 'Net Profit']
        periods = [3, 5, 10]
        summary = {}

        for m in metrics:
            if m in self.df.columns:
                summary[m] = {f"{p}Y CAGR": self.calculate_cagr(self.df[m], p) for p in periods}
        
        return pd.DataFrame(summary).T
