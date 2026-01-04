# =============================================================================
# value_creation.py - Value Creation Integration Module
# =============================================================================

import pandas as pd
from eva_analysis import EVAAnalyzer
from dcf_valuation import DCFValuation

class ValueCreationAnalyzer:
    """Integrate EVA and DCF for value creation assessment"""
    
    def __init__(self, annual_data, quarterly_data=None):
        self.annual_data = annual_data
        self.quarterly_data = quarterly_data
        self.eva_analyzer = EVAAnalyzer(annual_data, quarterly_data)
        self.dcf_analyzer = DCFValuation(annual_data, quarterly_data)
    
    def get_investment_quality_score(self):
        """Calculate investment quality score (0-100)"""
        score = 0
        
        try:
            # EVA Creation (30 points)
            eva, _, _, _, _ = self.eva_analyzer.calculate_eva()
            if eva.iloc[-1] > 0:
                score += 30
            else:
                score += max(0, 30 * (1 + eva.iloc[-1] / abs(eva.iloc[0])))
            
            # ROIC vs WACC (30 points)
            roic, _, _ = self.eva_analyzer.calculate_roic()
            _, _, wacc = self.eva_analyzer.calculate_wacc()
            spread = roic.iloc[-1] - wacc
            
            if spread > 5:
                score += 30
            elif spread > 2:
                score += 20
            elif spread > 0:
                score += 10
            
            # EVA Trend (20 points)
            eva_growth = (eva.iloc[-1] - eva.iloc[0]) / abs(eva.iloc[0]) if eva.iloc[0] != 0 else 0
            if eva_growth > 0:
                score += 20
            else:
                score += max(0, 20 * (1 + eva_growth))
            
            # Growth Momentum (20 points)
            sales_growth = (self.annual_data['Sales'].iloc[-1] / self.annual_data['Sales'].iloc[0]) ** (1/9) - 1
            if sales_growth > 0.08:
                score += 20
            elif sales_growth > 0.05:
                score += 15
            else:
                score += 10
        
        except:
            score = 50  # Default
        
        return min(100, max(0, score))
    
    def get_value_creation_summary(self):
        """Get comprehensive value creation summary"""
        score = self.get_investment_quality_score()
        
        if score >= 80:
            rating = "⭐⭐⭐⭐⭐ Excellent"
        elif score >= 60:
            rating = "⭐⭐⭐⭐ Very Good"
        elif score >= 40:
            rating = "⭐⭐⭐ Good"
        elif score >= 20:
            rating = "⭐⭐ Fair"
        else:
            rating = "⭐ Poor"
        
        return {
            'Quality Score': f"{score}/100",
            'Rating': rating,
            'Assessment': self._get_assessment(score)
        }
    
    def _get_assessment(self, score):
        """Get text assessment based on score"""
        if score >= 80:
            return "Excellent value creator. Strong EVA, high ROIC spread, and consistent growth."
        elif score >= 60:
            return "Good value creator. Positive EVA and reasonable ROIC spread."
        elif score >= 40:
            return "Moderate value creation. Some positive metrics but mixed signals."
        else:
            return "Weak value creation. Consider deeper analysis needed."
