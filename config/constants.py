"""
Constants used throughout the Fund Administration Platform
"""

from datetime import datetime

# Current date information
CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_YEAR_STR = str(CURRENT_YEAR)

# Priority levels
PRIORITY_LEVELS = ["High", "Medium", "Low"]
PRIORITY_COLORS = {
    "High": "#d62728",
    "Medium": "#ff7f0e", 
    "Low": "#2ca02c"
}

# Category colors for workstreams
CATEGORY_COLORS = {
    "NAV Calculation": "#1f77b4",
    "Portfolio Valuation": "#ff7f0e", 
    "Trade Capture": "#2ca02c",
    "Reconciliation": "#d62728",
    "Corporate Actions": "#9467bd",
    "Expense Management": "#8c564b",
    "Reporting": "#e377c2"
}

# Financial column patterns
FINANCIAL_PATTERNS = {
    "monthly": r'^{year}_\d{{2}}_([AF]|CP)$',
    "actuals": r'^{year}_\d{{2}}_A$',
    "forecasts": r'^{year}_\d{{2}}_F$',
    "capital_plan": r'^{year}_\d{{2}}_CP$'
}

# Excel template headers
CAPITAL_PROJECT_HEADERS = [
    "PROJECT_ID", "PROJECT_NAME", "PORTFOLIO_OBS_LEVEL1", "SUB_PORTFOLIO_OBS_LEVEL2",
    "PROJECT_MANAGER", "BRS_CLASSIFICATION", "FUND_DECISION", "BUSINESS_ALLOCATION",
    "CURRENT_EAC", "ALL_PRIOR_YEARS_ACTUALS"
]

# Score categories
SCORE_CATEGORIES = {
    "excellent": {"min": 9.0, "color": "#2ca02c", "label": "Excellent (9.0+)"},
    "good": {"min": 7.0, "color": "#ff7f0e", "label": "Good (7.0-8.9)"},
    "average": {"min": 5.0, "color": "#1f77b4", "label": "Average (5.0-6.9)"},
    "poor": {"min": 0, "color": "#d62728", "label": "Poor (<5.0)"}
}

# File paths
DATA_PATHS = {
    "workstream_data": "data/workstream_data.json",
    "templates": "data/templates/"
}

# Error messages
ERROR_MESSAGES = {
    "file_not_found": "The requested file could not be found.",
    "invalid_format": "Invalid file format. Please upload CSV or Excel files only.",
    "data_processing": "An error occurred while processing your data.",
    "insufficient_data": "Insufficient data to generate the requested analysis."
}

# Success messages  
SUCCESS_MESSAGES = {
    "file_uploaded": "File uploaded successfully!",
    "data_processed": "Data processed successfully!",
    "report_generated": "Report generated successfully!"
}