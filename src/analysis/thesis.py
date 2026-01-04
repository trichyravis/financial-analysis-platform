
import pandas as pd

class ThesisEngine:
    def __init__(self, data, dcf_val, market_price):
        self.data = data
        self.dcf_val = dcf_val
        self.market_price = market_price

    def generate_verdict(self):
        score = 0
        reasons = []

        # 1. Valuation Logic
        if self.dcf_val > self.market_price:
            score += 1
            upside = ((self.dcf_val / self.market_price) - 1) * 100
            reasons.append(f"✅ **Valuation:** {upside:.1f}% Upside (Margin of Safety confirmed).")
        else:
            reasons.append("❌ **Valuation:** Premium pricing (Current price > Intrinsic Value).")

        # 2. ROE Logic (Quality)
        latest_roe = self.data['ROE %'].iloc[-1] if 'ROE %' in self.data.columns else 0
        if latest_roe > 15:
            score += 1
            reasons.append(f"✅ **Profitability:** ROE of {latest_roe:.1f}% exceeds 15% benchmark.")
        else:
            reasons.append(f"⚠️ **Profitability:** ROE of {latest_roe:.1f}% suggests low capital efficiency.")

        # 3. Debt Logic (Risk)
        equity = (self.data.get('Equity Share Capital', 0) + self.data.get('Reserves', 0)).iloc[-1]
        debt = self.data.get('Borrowings', 0).iloc[-1]
        de_ratio = debt / equity if equity > 0 else 0
        
        if de_ratio < 1.0:
            score += 1
            reasons.append(f"✅ **Solvency:** Healthy D/E ratio of {de_ratio:.2f} (Low bankruptcy risk).")
        else:
            reasons.append(f"⚠️ **Solvency:** High leverage ({de_ratio:.2f}) - check interest coverage.")

        return score, reasons
