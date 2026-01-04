
"""
financial.py - Institutional Financial Analysis Engine
🏔️ THE MOUNTAIN PATH - World of Finance
CORRECTED: Works with Screener.in data loader structure
"""

import pandas as pd
import numpy as np


class FinancialAnalyzer:
    def __init__(self, df):
        """
        Institutional Grade Analyzer for Screener.in data.
        
        Works with corrected data loader structure:
        - 'Report Date' column contains metric names (Sales, Profit, etc.)
        - Date columns contain numeric values for each year
        """
        self.df = df.copy().reset_index(drop=True)
        self.df_transposed = None
        self.date_columns = None
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare data for analysis - transpose to get dates as index."""
        # Identify date columns (all except 'Report Date')
        self.date_columns = [col for col in self.df.columns if col != 'Report Date']
        
        # Transpose: metrics as columns, dates as index
        if len(self.df) > 0:
            self.df_transposed = self.df.set_index('Report Date')[self.date_columns].T
            
            # Standardize all columns to numeric
            for col in self.df_transposed.columns:
                vals = pd.to_numeric(self.df_transposed[col], errors='coerce').fillna(0)
                self.df_transposed[col] = vals.values

    def _get_clean_series(self, keyword):
        """Get a metric series by keyword search."""
        if self.df_transposed is None or len(self.date_columns) == 0:
            return pd.Series(0.0, index=range(len(self.date_columns) if self.date_columns else 0))
        
        for col in self.df_transposed.columns:
            if keyword.lower() in str(col).lower():
                series = self.df_transposed[col]
                if isinstance(series, pd.DataFrame):
                    series = series.iloc[:, 0]
                return series.reset_index(drop=True)
        return pd.Series(0.0, index=range(len(self.date_columns)))

    def get_profitability_metrics(self):
        """Calculates ROE and Margin."""
        metrics = pd.DataFrame()
        
        pat = self._get_clean_series('Net Profit')
        sales = self._get_clean_series('Sales')
        equity = self._get_clean_series('Equity Share Capital') + self._get_clean_series('Reserves')
        
        with np.errstate(divide='ignore', invalid='ignore'):
            metrics['ROE %'] = (pat.values / np.where(equity.values == 0, np.nan, equity.values)) * 100
            metrics['Net Margin %'] = (pat.values / np.where(sales.values == 0, np.nan, sales.values)) * 100
        
        metrics['Year'] = self.date_columns
        return metrics.fillna(0)

    def get_solvency_metrics(self):
        """Calculates debt-to-equity ratio."""
        metrics = pd.DataFrame()
        debt = self._get_clean_series('Borrowings')
        equity = self._get_clean_series('Equity Share Capital') + self._get_clean_series('Reserves')
        
        with np.errstate(divide='ignore', invalid='ignore'):
            metrics['Debt-to-Equity'] = debt.values / np.where(equity.values == 0, np.nan, equity.values)
        
        metrics['Year'] = self.date_columns
        return metrics.fillna(0)

    def get_efficiency_metrics(self):
        """Calculates operational efficiency metrics."""
        metrics = pd.DataFrame()
        
        sales = self._get_clean_series('Sales')
        inventory = self._get_clean_series('Inventory')
        receivables = self._get_clean_series('Receivables')
        
        with np.errstate(divide='ignore', invalid='ignore'):
            # Asset Turnover (normalized for P&L-only data)
            metrics['Asset Turnover'] = np.where(sales.values != 0, sales.values / np.maximum(sales.values, 1), 1)
            
            # Inventory Turnover
            metrics['Inventory Turnover'] = np.where(inventory.values != 0, 
                                                     sales.values / np.maximum(inventory.values, 1), 0)
            metrics['Inventory Turnover'] = metrics['Inventory Turnover'].replace([np.inf, -np.inf], 0)
            
            # Debtor Days
            metrics['Debtor Days'] = (receivables.values / np.where(sales.values != 0, sales.values, 1)) * 365
            metrics['Debtor Days'] = metrics['Debtor Days'].replace([np.inf, -np.inf], 0)
        
        metrics['Year'] = self.date_columns
        return metrics.fillna(0)

    def get_growth_summary(self):
        """Calculates YoY growth rates."""
        metrics = pd.DataFrame()
        
        sales = self._get_clean_series('Sales')
        profit = self._get_clean_series('Profit before tax')
        
        with np.errstate(divide='ignore', invalid='ignore'):
            # Sales Growth %
            sales_growth = np.zeros_like(sales.values, dtype=float)
            sales_growth[1:] = (np.diff(sales.values) / np.maximum(sales.values[:-1], 1)) * 100
            metrics['Sales Growth %'] = sales_growth
            
            # Profit Growth %
            profit_growth = np.zeros_like(profit.values, dtype=float)
            profit_growth[1:] = (np.diff(profit.values) / np.maximum(np.abs(profit.values[:-1]), 1)) * 100
            metrics['Profit Growth %'] = profit_growth
            
            metrics['Sales Growth %'] = metrics['Sales Growth %'].replace([np.inf, -np.inf], 0)
            metrics['Profit Growth %'] = metrics['Profit Growth %'].replace([np.inf, -np.inf], 0)
        
        metrics['Year'] = self.date_columns
        return metrics.fillna(0)

    def get_dilution_metrics(self):
        """Calculates EPS and Book Value per share."""
        metrics = pd.DataFrame()
        
        net_profit = self._get_clean_series('Net profit')
        shares = self._get_clean_series('No. of Equity Shares')
        equity = self._get_clean_series('Equity Share Capital') + self._get_clean_series('Reserves')
        
        with np.errstate(divide='ignore', invalid='ignore'):
            # EPS = Net Profit / Number of Shares (in Crores, so multiply by 100 for per-share)
            metrics['EPS (₹)'] = (net_profit.values / np.where(shares.values != 0, shares.values, 1)) * 100
            metrics['EPS (₹)'] = metrics['EPS (₹)'].replace([np.inf, -np.inf], 0)
            
            # Book Value Per Share = Equity / Number of Shares
            metrics['Book Value/Share (₹)'] = (equity.values / np.where(shares.values != 0, shares.values, 1)) * 100
            metrics['Book Value/Share (₹)'] = metrics['Book Value/Share (₹)'].replace([np.inf, -np.inf], 0)
        
        metrics['Year'] = self.date_columns
        return metrics.fillna(0)
