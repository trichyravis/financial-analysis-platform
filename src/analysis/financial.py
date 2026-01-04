
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Initializes the analyzer with the processed dataframe from the loader.
        Expects a dataframe where rows are years and columns are financial metrics.
        """
        self.df = df.copy()
        # Ensure all columns except 'Report Date' are numeric
        for col in self.df.columns:
            if col != 'Report Date':
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

    def get_profitability_metrics(self):
        """
        Calculates core profitability ratios with index alignment safety.
        Fixes the ValueError by ensuring the result matches the input length.
        """
        # 1. Initialize empty metrics dataframe with the same index as source
        metrics = pd.DataFrame(index=self.df.index)
        
        # 2. Extract components for readability
        pat = self.df['Net Profit']
        sales = self.df['Sales']
        
        # Equity = Share Capital + Reserves
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        
        # 3. Calculate Ratios (Pandas aligns these automatically via the index)
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        
        # 4. Add 'Year' column safely
        if 'Report Date' in self.df.columns:
            metrics['Year'] = self.df['Report Date']
        else:
            metrics['Year'] = self.df.index
            
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        """
        Calculates balance sheet strength metrics.
        """
        metrics = pd.DataFrame(index=self.df.index)
        
        borrowings = self.df.get('Borrowings', 0)
        equity = self.df.get('Equity Share Capital', 0) + self.df.get('Reserves', 0)
        total_assets = self.df.get('Total Assets', 0)
        
        metrics['Debt-to-Equity'] = borrowings / equity.replace(0, np.nan)
        metrics['Equity Multiplier'] = total_assets / equity.replace(0, np.nan)
        
        if 'Report Date' in self.df.columns:
            metrics['Year'] = self.df['Report Date']
        else:
            metrics['Year'] = self.df.index
            
        return metrics.fillna(0)

    def get_efficiency_metrics(self):
        """
        Calculates operational efficiency metrics.
        """
        metrics = pd.DataFrame(index=self.df.index)
        
        sales = self.df['Sales']
        inventory = self.df.get('Inventory', 0)
        debtors = self.df.get('Trade Receivables', 0)
        
        # Asset Turnover
        total_assets = self.df.get('Total Assets', 0)
        metrics['Asset Turnover'] = sales / total_assets.replace(0, np.nan)
        
        # Working Capital Ratios
        if 'Report Date' in self.df.columns:
            metrics['Year'] = self.df['Report Date']
        else:
            metrics['Year'] = self.df.index
            
        return metrics.fillna(0)
