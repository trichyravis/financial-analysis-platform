
import pandas as pd

class ThesisEngine:
    def __init__(self, data, dcf_val, market_price):
        self.data = data
        self.dcf_val = dcf_val
        self.market_price = market_price

    def generate_verdict(self):
        points = 0
        reasons = []

        # 1. Valuation Check
        if self.dcf_val > self.market_price and self.dcf_val > 0:
            points += 1
            reasons.append("✅ **Value:** Stock is trading below its Intrinsic Value.")
        else:
            reasons.append("❌ **Value:** Stock is potentially overvalued or DCF not set.")

        # 2. ROE Quality Check
        latest_roe = self.data['ROE %'].iloc[-1] if 'ROE %' in self.data.columns else 0
        if latest_roe > 15:
            points += 1
            reasons.append(f"✅ **Quality:** Robust ROE of {latest_roe:.1f}% (Benchmark > 15%).")
        else:
            reasons.append(f"⚠️ **Quality:** ROE of {latest_roe:.1f}% is below institutional standards.")

        # 3. Solvency Check
        equity = (self.data.get('Equity Share Capital', 0) + self.data.get('Reserves', 0)).iloc[-1]
        debt = self.data.get('Borrowings', 0).iloc[-1]
        de_ratio = debt / equity if equity > 0 else 0
        if de_ratio < 1:
            points += 1
            reasons.append(f"✅ **Solvency:** Healthy Debt-to-Equity ratio of {de_ratio:.2f}.")
        else:
            reasons.append(f"⚠️ **Solvency:** High leverage detected ({de_ratio:.2f}).")

        return points, reasons
