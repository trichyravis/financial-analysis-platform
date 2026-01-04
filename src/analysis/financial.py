
import pandas as pd
import numpy as np

class FinancialAnalyzer:
    def __init__(self, df):
        """
        Institutional Financial Analyzer with multi-column protection.
        """
        # 1. Standardize the Index
        if 'Report Date' in df.columns:
            df = df.set_index('Report Date')
        
        # 2. De-duplicate columns (Screener.in often repeats 'Sales' or 'Net Profit')
        # We keep the first instance and discard the rest to prevent multi-column errors
        df = df.loc[:, ~df.columns.duplicated()]
        
        # 3. Target Length Guardrail
        target_length = len(df.index)
        cleaned_data = {}

        for col in df.columns:
            # Flatten to 1D and ensure length matches the number of years
            raw_array = np.array(df[col]).ravel()[:target_length]
            cleaned_data[col] = pd.to_numeric(pd.Series(raw_array), errors='coerce').fillna(0).values
        
        # Final cleaned dataframe
        self.df = pd.DataFrame(cleaned_data, index=df.index)

    def _get_safe_series(self, col_name):
        """Internal helper to ensure we always handle a single Series, never a DataFrame."""
        val = self.df.get(col_name, 0)
        if isinstance(val, pd.DataFrame):
            return val.iloc[:, 0]
        return val

    def get_profitability_metrics(self):
        """Calculates core profitability ratios with alignment and multi-column safety."""
        metrics = pd.DataFrame(index=self.df.index)
        
        pat = self._get_safe_series('Net Profit')
        sales = self._get_safe_series('Sales')
        equity = self._get_safe_series('Equity Share Capital') + self._get_safe_series('Reserves')
        
        # Logic: Replace 0 with NaN to avoid division errors
        metrics['ROE %'] = (pat / equity.replace(0, np.nan)) * 100
        metrics['Net Margin %'] = (pat / sales.replace(0, np.nan)) * 100
        
        # Add 'Year' for UI
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        """Calculates Debt-to-Equity and leverage ratios."""
        metrics = pd.DataFrame(index=self.df.index)
        
        borrowings = self._get_safe_series('Borrowings')
        equity = self._get_safe_series('Equity Share Capital') + self._get_safe_series('Reserves')
        
        metrics['Debt-to-Equity'] = borrowings / equity.replace(0, np.nan)
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)

    def get_efficiency_metrics(self):
        """Calculates operational efficiency metrics."""
        metrics = pd.DataFrame(index=self.df.index)
        
        sales = self._get_safe_series('Sales')
        total_assets = self._get_safe_series('Total Assets')
        
        metrics['Asset Turnover'] = sales / total_assets.replace(0, np.nan)
        metrics['Year'] = self.df.index.astype(str)
        
        return metrics.fillna(0)
