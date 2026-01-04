
"""
config.py - Centralized Configuration for The Mountain Path
🏔️ THE MOUNTAIN PATH - World of Finance
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
# This dictionary is required by src/ui/styles.py
COLORS = {
    "primary_dark": "#002147",      # Deep Navy for Sidebar/Header
    "primary_light": "#004b8d",     # Lighter Blue
    "accent_gold": "#FFD700",       # Gold for accents and borders
    "background": "#F5F5F5",        # Light Gray background
    "text": "#333333"               # Charcoal text
}

# =============================================================================
# NAVIGATION (The 9-Tab Architecture)
# =============================================================================
TABS = [
    "📊 Dashboard",      # Index 0
    "📋 Financials",     # Index 1
    "📈 Profitability",  # Index 2
    "🎯 DCF Valuation",  # Index 3
    "💎 EVA Analysis",   # Index 4
    "⚖️ Solvency",       # Index 5
    "⚡ Efficiency",     # Index 6
    "🚀 Growth",         # Index 7
    "📝 Thesis"          # Index 8
]

# =============================================================================
# FINANCIAL CONSTANTS (Default Assumptions)
# =============================================================================
FINANCIAL_DEFAULTS = {
    "risk_free_rate": 0.07,          # 7.0%
    "market_return": 0.12,           # 12.0%
    "terminal_growth": 0.04,         # 4.0%
    "tax_rate": 0.25,                # 25% Corporate Tax
    "wacc_default": 12.0             # Default WACC percentage
}
