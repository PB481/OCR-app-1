"""
Configuration file for Fund Administration Workstream Management Platform
"""

# Application Settings
APP_CONFIG = {
    'page_title': "Operational Workstreams - Fund Administration",
    'page_icon': "🏗️",
    'layout': "wide",
    'version': "2.0.0"
}

# Data Processing Settings
DATA_CONFIG = {
    'default_risk_threshold': 7.0,
    'automation_target': 8.0,
    'investment_limit': 5.0,
    'completion_target': 80.0,
    'cache_ttl': 300,  # 5 minutes
    'max_file_size': 50 * 1024 * 1024  # 50MB
}

# Visualization Settings
VIZ_CONFIG = {
    'default_color_scheme': 'plotly',
    '3d_rotation_speed': 0.1,
    'chart_height': 600,
    'chart_width': 800
}

# Report Settings
REPORT_CONFIG = {
    'excel_engine': 'xlsxwriter',
    'html_template': 'default',
    'include_charts': True,
    'include_summary': True
}

# Categories and Colors
CATEGORY_COLORS = {
    'NAV Calculation': '#1f77b4',
    'Portfolio Valuation': '#ff7f0e',
    'Trade Capture': '#2ca02c',
    'Reconciliation': '#d62728',
    'Corporate Actions': '#9467bd',
    'Expense Management': '#8c564b',
    'Reporting': '#e377c2'
}

# Priority Levels
PRIORITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']

# Risk Categories
RISK_CATEGORIES = {
    'Low': (1, 3),
    'Medium': (4, 6),
    'High': (7, 8),
    'Critical': (9, 10)
} 