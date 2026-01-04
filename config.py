# =============================================================================
# config.py - Configuration & Constants
# =============================================================================

# Colors - Mountain Path Branding
COLORS = {
    'primary': '#003366',      # Dark Blue
    'secondary': '#ADD8E6',    # Light Blue
    'accent': '#FFD700',       # Gold
    'background': '#f0f2f6',
    'text': '#333333'
}

# Typography
FONTS = {
    'family': 'Arial, sans-serif',
    'title_size': 32,
    'header_size': 24,
    'body_size': 14
}

# Layout
SIDEBAR_WIDTH = 300

# Branding
COMPANY_NAME = "The Mountain Path"
TAGLINE = "World of Finance"
AUTHOR = "Prof. V. Ravichandran"
AUTHOR_DETAILS = "28+ Years Corporate Finance & Banking Experience, 10+ Years Academic Excellence"

# Thresholds & Defaults
DEFAULT_RISK_FREE_RATE = 0.06
DEFAULT_MARKET_RETURN = 0.12
DEFAULT_WACC = 0.10
DEFAULT_TERMINAL_GROWTH = 0.025

# VaR Confidence Levels
VAR_CONFIDENCE_LEVELS = [0.90, 0.95, 0.99]

# Page Config
PAGE_TITLE = "Financial Analysis Platform"
PAGE_ICON = "🏔️"
LAYOUT = "wide"

# Metrics Categories
PROFITABILITY_METRICS = [
    'Gross Profit Margin',
    'EBIT Margin',
    'Net Profit Margin',
    'Return on Equity (ROE)',
    'Return on Assets (ROA)'
]

LIQUIDITY_METRICS = [
    'Current Ratio',
    'Quick Ratio',
    'Cash Ratio'
]

SOLVENCY_METRICS = [
    'Debt-to-Equity',
    'Debt-to-Assets',
    'Interest Coverage Ratio'
]

EFFICIENCY_METRICS = [
    'Asset Turnover',
    'Receivables Turnover',
    'Inventory Turnover'
]

VALUATION_METRICS = [
    'P/E Ratio',
    'P/B Ratio',
    'Dividend Yield',
    'Payout Ratio'
]

RISK_METRICS = [
    'Volatility',
    'Sharpe Ratio',
    'Max Drawdown',
    'Value at Risk (VaR)',
    'Beta'
]

EVA_METRICS = [
    'NOPAT',
    'Invested Capital',
    'WACC',
    'EVA',
    'ROIC',
    'Spread (ROIC - WACC)',
    'MVA'
]

DCF_METRICS = [
    'Free Cash Flow',
    'Terminal Value',
    'Enterprise Value',
    'Equity Value',
    'Fair Value Per Share',
    'Upside/Downside %'
]
