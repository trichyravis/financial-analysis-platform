
"""
thesis.py - Investment Decision Engine
🏔️ THE MOUNTAIN PATH
"""

class ThesisEngine:
    def __init__(self, data, dcf_price, current_price):
        self.data = data
        self.dcf_val = dcf_price
        self.market_val = current_price

    def generate_verdict(self):
        points = 0
        reasons = []

        # 1. Valuation Check
        if self.dcf_val > self.market_val:
            points += 1
            upside = ((self.dcf_val / self.market_val) - 1) * 100
            reasons.append(f"✅ Undervalued: DCF suggests {upside:.1f}% upside.")
        else:
            reasons.append("❌ Overvalued: Current price exceeds Intrinsic Value.")

        # 2. Profitability Check (ROE > 15%)
        latest_roe = self.data['ROE %'].iloc[-1] if 'ROE %' in self.data.columns else 0
        if latest_roe > 15:
            points += 1
            reasons.append(f"✅ High Quality: ROE of {latest_roe:.1f}% is robust.")
        else:
            reasons.append(f"⚠️ Low Returns: ROE of {latest_roe:.1f}% is below benchmark.")

        # 3. Debt Check (D/E < 1.0)
        debt = self.data.get('Borrowings', 0).iloc[-1]
        equity = (self.data.get('Equity Share Capital', 0) + self.data.get('Reserves', 0)).iloc[-1]
        de_ratio = debt / equity if equity != 0 else 0
        if de_ratio < 1:
            points += 1
            reasons.append(f"✅ Safe Leverage: Debt-to-Equity is low at {de_ratio:.2f}.")
        else:
            reasons.append(f"⚠️ Risky Leverage: Debt-to-Equity is high at {de_ratio:.2f}.")

        return points, reasons
