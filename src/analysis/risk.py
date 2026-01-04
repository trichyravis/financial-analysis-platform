import numpy as np
import pandas as pd

class RiskAnalyzer:
    """Calculates VaR and Volatility metrics."""
    
    def __init__(self, sales_data):
        self.returns = sales_data.pct_change().dropna()

    def calculate_metrics(self):
        """Calculates standard risk parameters."""
        volatility = self.returns.std() * np.sqrt(1) # Annualized if using annual data
        
        # Value at Risk (95% Confidence)
        var_95 = np.percentile(self.returns, 5)
        
        return {
            "Volatility (Sales)": f"{volatility*100:.2f}%",
            "VaR (95% Conf)": f"{var_95*100:.2f}%",
            "Max Drawdown (Sales)": f"{(self.returns.min())*100:.2f}%"
        }
