
import pandas as pd

class CapitalAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_dilution_metrics(self):
        """Checks if the company is issuing new shares or buying back."""
        metrics = pd.DataFrame(index=self.df['Report Date'])
        metrics['No. of Shares'] = self.df.get('No. Of Equity Shares', 0)
        metrics['Equity Capital'] = self.df.get('Equity Share Capital', 0)
        
        # Calculate % change in share count
        metrics['Share Count Change %'] = metrics['No. of Shares'].pct_change() * 100
        return metrics
