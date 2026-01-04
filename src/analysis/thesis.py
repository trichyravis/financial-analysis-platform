
class ThesisEngine:
    def __init__(self, data, dcf_val, eva_val):
        self.data = data
        self.dcf_val = dcf_val
        self.eva_val = eva_val

    def generate_scorecard(self):
        score = 0
        checks = []
        
        # 1. Profitability Check
        roe = self.data['ROE %'].iloc[-1]
        if roe > 15:
            score += 1
            checks.append(("✅ Strong Returns", f"ROE of {roe:.1f}% is above the 15% institutional benchmark."))
        else:
            checks.append(("⚠️ Subpar Returns", f"ROE of {roe:.1f}% is below target."))

        # 2. Wealth Creation (EVA)
        if self.eva_val > 0:
            score += 1
            checks.append(("✅ Wealth Creator", "Positive EVA indicates the company earns more than its cost of capital."))
        else:
            checks.append(("❌ Wealth Destroyer", "Negative EVA suggests capital is being eroded."))

        # 3. Solvency Check
        de = (self.data['Borrowings'] / (self.data['Equity Share Capital'] + self.data['Reserves'])).iloc[-1]
        if de < 0.5:
            score += 1
            checks.append(("✅ Safe Leverage", f"Debt-to-Equity is conservative at {de:.2f}x."))
        else:
            checks.append(("⚠️ High Leverage", f"Debt-to-Equity of {de:.2f}x may increase financial risk."))

        return score, checks
