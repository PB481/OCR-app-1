"""
Configuration settings for the Fund Administration Platform
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Operational Workstreams - Fund Administration",
    "page_icon": "🏗️",
    "layout": "wide"
}

# File Upload Settings
UPLOAD_CONFIG = {
    "max_file_size": 200,  # MB
    "allowed_extensions": [".csv", ".xlsx", ".xls"],
    "chunk_size": 10000  # For large file processing
}

# Chart Configuration
CHART_CONFIG = {
    "default_height": 600,
    "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    "template": "plotly_white"
}

# Data Processing
DATA_CONFIG = {
    "date_formats": ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"],
    "numeric_columns_pattern": r'^(20\d{2}_\d{2}_(A|F|CP)(_\d+)?|ALL_PRIOR_YEARS_ACTUALS|BUSINESS_ALLOCATION|CURRENT_EAC)$',
    "cache_timeout": 3600  # seconds
}

# Report Generation
REPORT_CONFIG = {
    "excel_engine": "xlsxwriter",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "currency_format": "${:,.2f}"
}

# Business Case Scoring
SCORING_CONFIG = {
    "weights": {
        "financial": 0.25,
        "strategic": 0.20,
        "feasibility": 0.20,
        "impact": 0.20,
        "resource": 0.15
    },
    "thresholds": {
        "high": 8.0,
        "medium": 6.0,
        "low": 4.0
    }
}

# Session State Keys
SESSION_KEYS = {
    "workstream_data": "workstream_data",
    "capital_project_data": "capital_project_data",
    "pl_data": "pl_data",
    "competitors_data": "competitors_data",
    "business_cases": "business_cases",
    "comments": {
        "variance": "comment_variance",
        "impact": "comment_impact",
        "bottom5": "comment_bottom5"
    }
}