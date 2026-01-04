
import pandas as pd
import numpy as np

class GrowthAnalyzer:
    def __init__(self, df):
        self.df = df

    def calculate_cagr(self, series, periods):
        if len(series) < periods + 1:
            return np.nan
        start_val = series.iloc[-(periods + 1)]
        end_val = series.iloc[-1]
        if start_val <= 0 or end_val <= 0:
            return np.nan
        return (pow((end_val / start_val), 1/periods) - 1) * 100

    def get_growth_summary(self):
        summary = {}
        for metric in ['Sales', 'Net Profit']:
            summary[metric] = {
                '3Y CAGR': self.calculate_cagr(self.df[metric], 3),
                '5Y CAGR': self.calculate_cagr(self.df[metric], 5),
                '10Y CAGR': self.calculate_cagr(self.df[metric], 10)
            }
        return pd.DataFrame(summary).T
