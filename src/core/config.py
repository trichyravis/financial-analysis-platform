
"""
config.py - Centralized Configuration for The Mountain Path
Centralizes branding, colors, and financial assumptions.
"""

# =============================================================================
# BRANDING & IDENTITY
# =============================================================================
COMPANY_NAME = "The Mountain Path"
TAGLINE = "World of Finance"
AUTHOR = "Prof. V. Ravichandran"
AUTHOR_CREDENTIALS = "28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence"

# =============================================================================
# UI COLOR PALETTE (Institutional Theme)
# =============================================================================
COLORS = {
    "primary_dark": "#002147",      # Deep Navy for Sidebar/Header
    "primary_light": "#004b8d",     # Lighter Blue for gradients
    "accent_gold": "#FFD700",       # Gold for accents and borders
    "background": "#F5F5F5",
    "text": "#333333"
}

# =============================================================================
# FINANCIAL CONSTANTS (Default Assumptions)
# =============================================================================
FINANCIAL_DEFAULTS = {
    "risk_free_rate": 0.07,         # 7.0% (India 10Y G-Sec average)
    "market_return": 0.12,          # 12.0% (Nifty 50 long-term avg)
    "terminal_growth": 0.04,        # 4.0% (Long-term inflation target)
    "tax_rate": 0.25                # Standard Corporate Tax
}

# =============================================================================
# NAVIGATION
# =============================================================================
TABS = [
    "📊 Dashboard", "📈 Financials", "📉 Profitability", 
    "🎯 DCF Valuation", "💎 EVA Analysis", "⚖️ Solvency", 
    "⚡ Efficiency", "🛡️ Risk Metrics", "💹 Peers"
]
