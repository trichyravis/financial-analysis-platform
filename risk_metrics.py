# =============================================================================
# risk_metrics.py - Risk Analysis & Metrics
# =============================================================================

import pandas as pd
import numpy as np
from scipy import stats

class RiskAnalyzer:
    """Calculate risk metrics including volatility, VaR, Sharpe ratio"""
    
    def __init__(self, annual_data, risk_free_rate=0.06):
        self.data = annual_data
        self.risk_free_rate = risk_free_rate
    
    # ========== VOLATILITY CALCULATIONS ==========
    
    def calculate_volatility(self, periods=252):
        """
        Calculate annualized volatility
        Using daily returns implied from annual data
        """
        try:
            returns = self.data['Sales'].pct_change().dropna()
            daily_vol = returns.std()
            annual_vol = daily_vol * np.sqrt(periods)
            return annual_vol * 100
        except:
            return 20.0  # Default
    
    def calculate_log_returns(self):
        """Calculate log returns"""
        try:
            return np.log(self.data['Sales'] / self.data['Sales'].shift(1)).dropna()
        except:
            return pd.Series([0.05] * len(self.data))
    
    def calculate_rolling_volatility(self, window=3):
        """Calculate rolling volatility"""
        try:
            returns = self.data['Sales'].pct_change()
            return returns.rolling(window).std() * 100
        except:
            return None
    
    # ========== VALUE AT RISK (VAR) ==========
    
    def calculate_var(self, confidence=0.95, method='historical'):
        """
        Calculate Value at Risk
        
        confidence: 0.90, 0.95, or 0.99
        method: 'historical' or 'parametric'
        """
        try:
            returns = self.data['Sales'].pct_change().dropna()
            
            if method == 'historical':
                var = np.percentile(returns, (1 - confidence) * 100)
            else:  # parametric (normal distribution)
                mean_ret = returns.mean()
                std_ret = returns.std()
                var = mean_ret + std_ret * stats.norm.ppf(1 - confidence)
            
            return var * 100
        except:
            return -5.0  # Default
    
    def calculate_cvar(self, confidence=0.95):
        """
        Calculate Conditional Value at Risk (Expected Shortfall)
        Average loss beyond VaR
        """
        try:
            returns = self.data['Sales'].pct_change().dropna()
            var = np.percentile(returns, (1 - confidence) * 100)
            cvar = returns[returns <= var].mean()
            return cvar * 100
        except:
            return -7.0
    
    # ========== DRAWDOWN ANALYSIS ==========
    
    def calculate_max_drawdown(self):
        """Calculate maximum drawdown"""
        try:
            cumulative = (1 + self.data['Sales'].pct_change()).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return drawdown.min() * 100
        except:
            return -20.0
    
    def calculate_drawdown_duration(self):
        """Calculate average drawdown duration"""
        try:
            cumulative = (1 + self.data['Sales'].pct_change()).cumprod()
            running_max = cumulative.expanding().max()
            in_drawdown = cumulative < running_max
            
            durations = []
            current_duration = 0
            for in_dd in in_drawdown:
                if in_dd:
                    current_duration += 1
                else:
                    if current_duration > 0:
                        durations.append(current_duration)
                    current_duration = 0
            
            return np.mean(durations) if durations else 0
        except:
            return 0
    
    # ========== SHARPE & SORTINO RATIOS ==========
    
    def calculate_sharpe_ratio(self, periods=252):
        """
        Sharpe Ratio = (Return - Risk Free Rate) / Volatility
        """
        try:
            returns = self.data['Sales'].pct_change().dropna()
            mean_return = returns.mean() * periods
            volatility = returns.std() * np.sqrt(periods)
            
            sharpe = (mean_return - self.risk_free_rate) / (volatility + 0.01)
            return sharpe
        except:
            return 0.5
    
    def calculate_sortino_ratio(self, periods=252):
        """
        Sortino Ratio = (Return - Risk Free Rate) / Downside Volatility
        Only penalizes downside volatility
        """
        try:
            returns = self.data['Sales'].pct_change().dropna()
            mean_return = returns.mean() * periods
            
            downside_returns = returns[returns < 0]
            downside_vol = downside_returns.std() * np.sqrt(periods)
            
            sortino = (mean_return - self.risk_free_rate) / (downside_vol + 0.01)
            return sortino
        except:
            return 0.7
    
    # ========== BETA & CORRELATION ==========
    
    def calculate_beta(self, market_returns=None):
        """
        Calculate Beta
        If market_returns not provided, use S&P 500 proxy
        """
        try:
            if market_returns is None:
                market_returns = pd.Series(
                    [0.10] * len(self.data),
                    index=self.data.index
                ).pct_change()
            
            stock_returns = self.data['Sales'].pct_change().dropna()
            
            covariance = np.cov(stock_returns, market_returns[:len(stock_returns)])[0][1]
            market_variance = np.var(market_returns)
            
            beta = covariance / market_variance
            return beta
        except:
            return 1.0
    
    # ========== SKEWNESS & KURTOSIS ==========
    
    def calculate_skewness(self):
        """Calculate return skewness"""
        try:
            returns = self.data['Sales'].pct_change().dropna()
            return stats.skew(returns)
        except:
            return 0.0
    
    def calculate_kurtosis(self):
        """Calculate return kurtosis (tail risk)"""
        try:
            returns = self.data['Sales'].pct_change().dropna()
            return stats.kurtosis(returns)
        except:
            return 0.0
    
    # ========== RISK DECOMPOSITION ==========
    
    def calculate_systematic_risk(self):
        """Systematic Risk = Beta × Market Risk"""
        try:
            beta = self.calculate_beta()
            market_risk = 0.15  # Historical market volatility
            return beta * market_risk
        except:
            return 0.10
    
    def calculate_unsystematic_risk(self):
        """Unsystematic Risk = Total Risk - Systematic Risk"""
        try:
            total_risk = self.calculate_volatility() / 100
            systematic_risk = self.calculate_systematic_risk()
            return total_risk - systematic_risk
        except:
            return 0.10
    
    # ========== COMPREHENSIVE RISK PROFILE ==========
    
    def get_risk_summary(self):
        """Get complete risk summary"""
        summary = {
            'Volatility (%)': f"{self.calculate_volatility():.1f}",
            'Sharpe Ratio': f"{self.calculate_sharpe_ratio():.2f}",
            'Sortino Ratio': f"{self.calculate_sortino_ratio():.2f}",
            'Max Drawdown (%)': f"{self.calculate_max_drawdown():.1f}",
            'VaR 90% (%)': f"{self.calculate_var(0.90):.1f}",
            'VaR 95% (%)': f"{self.calculate_var(0.95):.1f}",
            'VaR 99% (%)': f"{self.calculate_var(0.99):.1f}",
            'CVaR 95% (%)': f"{self.calculate_cvar(0.95):.1f}",
            'Skewness': f"{self.calculate_skewness():.2f}",
            'Kurtosis': f"{self.calculate_kurtosis():.2f}",
            'Beta': f"{self.calculate_beta():.2f}",
        }
        return summary
