
import pandas as pd
import numpy as np

class RiskAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_risk_metrics(self):
        """Calculates volatility and safety margins."""
        risk = {}
        
        # 1. Earnings & Sales Volatility (Standard Deviation of Growth)
        sales_growth = self.df['Sales'].pct_change()
        profit_growth = self.df['Net Profit'].pct_change()
        
        risk['Sales Volatility (%)'] = sales_growth.std() * 100
        risk['Profit Volatility (%)'] = profit_growth.std() * 100
        
        # 2. Financial Leverage Risk
        total_debt = self.df['Borrowings'].iloc[-1]
        equity = (self.df['Equity Share Capital'] + self.df['Reserves']).iloc[-1]
        risk['Debt to Equity (Latest)'] = total_debt / equity if equity != 0 else 0
        
        # 3. Interest Coverage (Safety Margin)
        pbt = self.df['Profit Before Tax'].iloc[-1]
        interest = self.df['Interest'].iloc[-1]
        risk['Interest Coverage'] = (pbt + interest) / interest if interest > 0 else 999
        
        # 4. Cash Flow Coverage
        cfo = self.df.get('Cash From Operating Activity', pd.Series([0]*len(self.df))).iloc[-1]
        risk['CFO to Debt Ratio'] = cfo / total_debt if total_debt > 0 else 999
        
        return pd.Series(risk)
