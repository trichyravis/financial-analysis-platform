
"""
thesis.py - Investment Thesis Engine
🏔️ THE MOUNTAIN PATH - World of Finance
CORRECTED: Works with corrected data loader and analyzer structure
"""

import pandas as pd
import numpy as np


class ThesisEngine:
    def __init__(self, data, dcf_val, market_price):
        """
        Investment Thesis Generation Engine.
        
        Args:
            data: DataFrame from UniversalScreenerLoader with structure:
                  'Report Date' column (metric names), date columns (values)
            dcf_val: Intrinsic value from DCF calculation
            market_price: Current market price
        """
        self.data = data
        self.dcf_val = dcf_val
        self.market_price = market_price
        self.metrics = self._extract_metrics()

    def _extract_metrics(self):
        """
        Extract key metrics from data for thesis generation.
        Works with corrected data loader structure.
        """
        metrics = {}
        
        try:
            # Transpose data to get metrics as columns, dates as rows
            df_t = self.data.set_index('Report Date').T
            
            # Get latest values (last row = most recent year)
            if len(df_t) > 0:
                latest = df_t.iloc[-1]
                
                # Extract key metrics
                metrics['net_profit'] = pd.to_numeric(latest.get('Net profit', 0), errors='coerce') or 0
                metrics['sales'] = pd.to_numeric(latest.get('Sales', 0), errors='coerce') or 0
                metrics['equity'] = (pd.to_numeric(latest.get('Equity Share Capital', 0), errors='coerce') or 0) + \
                                   (pd.to_numeric(latest.get('Reserves', 0), errors='coerce') or 0)
                metrics['debt'] = pd.to_numeric(latest.get('Borrowings', 0), errors='coerce') or 0
                metrics['pbt'] = pd.to_numeric(latest.get('Profit before tax', 0), errors='coerce') or 0
                
                # Calculate ROE
                if metrics['equity'] > 0:
                    metrics['roe'] = (metrics['net_profit'] / metrics['equity']) * 100
                else:
                    metrics['roe'] = 0
                
                # Calculate D/E ratio
                if metrics['equity'] > 0:
                    metrics['de_ratio'] = metrics['debt'] / metrics['equity']
                else:
                    metrics['de_ratio'] = 0
                
                # Calculate profit margin
                if metrics['sales'] > 0:
                    metrics['profit_margin'] = (metrics['pbt'] / metrics['sales']) * 100
                else:
                    metrics['profit_margin'] = 0
            
            return metrics
            
        except Exception as e:
            print(f"⚠️  Error extracting metrics for thesis: {e}")
            return {
                'net_profit': 0,
                'sales': 0,
                'equity': 0,
                'debt': 0,
                'pbt': 0,
                'roe': 0,
                'de_ratio': 0,
                'profit_margin': 0
            }

    def generate_verdict(self):
        """
        Generate investment verdict based on:
        1. Valuation (DCF vs Market Price)
        2. Profitability (ROE)
        3. Solvency (D/E Ratio)
        
        Returns:
            score: Integer 0-3 (higher is better)
            reasons: List of rationale strings
        """
        score = 0
        reasons = []

        # 1. VALUATION LOGIC
        if self.dcf_val > 0 and self.market_price > 0:
            if self.dcf_val > self.market_price:
                score += 1
                upside = ((self.dcf_val / self.market_price) - 1) * 100
                reasons.append(f"✅ **Valuation:** {upside:.1f}% Upside (Margin of Safety confirmed).")
            else:
                discount = ((self.market_price / self.dcf_val) - 1) * 100
                reasons.append(f"❌ **Valuation:** {discount:.1f}% Premium pricing (Price > Intrinsic Value).")
        else:
            reasons.append("⚠️  **Valuation:** Insufficient data for valuation assessment.")

        # 2. PROFITABILITY LOGIC (Quality)
        roe = self.metrics.get('roe', 0)
        if roe > 15:
            score += 1
            reasons.append(f"✅ **Profitability:** ROE of {roe:.1f}% exceeds 15% benchmark.")
        elif roe > 10:
            reasons.append(f"⚠️  **Profitability:** ROE of {roe:.1f}% is moderate (Target: >15%).")
        else:
            reasons.append(f"❌ **Profitability:** ROE of {roe:.1f}% indicates poor capital efficiency.")

        # 3. SOLVENCY LOGIC (Risk)
        de_ratio = self.metrics.get('de_ratio', 0)
        if de_ratio < 1.0:
            score += 1
            reasons.append(f"✅ **Solvency:** Healthy D/E ratio of {de_ratio:.2f} (Low bankruptcy risk).")
        elif de_ratio < 2.0:
            reasons.append(f"⚠️  **Solvency:** Moderate leverage (D/E: {de_ratio:.2f}) - watch interest coverage.")
        else:
            reasons.append(f"❌ **Solvency:** High leverage (D/E: {de_ratio:.2f}) - significant financial risk.")

        return score, reasons

    def get_full_analysis(self):
        """Generate comprehensive investment thesis."""
        score, checks = self.generate_verdict()
        
        analysis = {
            'score': score,
            'verdict': self._get_verdict_text(score),
            'checks': checks,
            'metrics': self.metrics,
            'confidence': self._get_confidence_level(score)
        }
        
        return analysis

    def _get_verdict_text(self, score):
        """Get verdict based on score."""
        if score >= 3:
            return "🏔️ STRONG BUY - Investable Grade"
        elif score == 2:
            return "✅ MODERATE BUY - Good Opportunity"
        elif score == 1:
            return "⚠️  HOLD/WATCHLIST - Monitor Closely"
        else:
            return "❌ SELL/AVOID - High Risk"

    def _get_confidence_level(self, score):
        """Calculate confidence level based on available data."""
        # Check how many metrics we have
        metrics_count = sum(1 for v in self.metrics.values() if v != 0)
        
        if metrics_count >= 6:
            return "High"
        elif metrics_count >= 4:
            return "Moderate"
        else:
            return "Low"
