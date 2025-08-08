import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import json
from datetime import datetime, timedelta
import io
import re
import inspect

# Page Configuration
st.set_page_config(
    page_title="Operational Workstreams - Fund Administration",
    page_icon="🏗️",
    layout="wide"
)

# Initialize session state for workstream data
if 'workstream_data' not in st.session_state:
    st.session_state.workstream_data = [
        # NAV Calculation Workstreams
        {'id': 'nav_001', 'name': 'Capstock Processing', 'category': 'NAV Calculation', 'complexity': 6, 'automation': 4, 'risk': 5, 'investment': 2.5, 'completion': 65, 'priority': 'Medium', 'description': 'Processing of capital stock transactions and subscriptions/redemptions'},
        {'id': 'nav_002', 'name': 'NAV Calculation & Publication', 'category': 'NAV Calculation', 'complexity': 8, 'automation': 7, 'risk': 8, 'investment': 4.2, 'completion': 80, 'priority': 'High', 'description': 'Core NAV calculation engine and publication workflow'},
        {'id': 'nav_003', 'name': 'Income Equalisation', 'category': 'NAV Calculation', 'complexity': 7, 'automation': 3, 'risk': 6, 'investment': 1.8, 'completion': 45, 'priority': 'Medium', 'description': 'Income equalisation calculations for unit pricing'},
        {'id': 'nav_004', 'name': 'Swing Pricing', 'category': 'NAV Calculation', 'complexity': 9, 'automation': 2, 'risk': 7, 'investment': 3.1, 'completion': 25, 'priority': 'High', 'description': 'Dynamic swing pricing mechanism implementation'},
        
        # Portfolio Valuation Workstreams
        {'id': 'val_001', 'name': 'Exchange Listed Securities', 'category': 'Portfolio Valuation', 'complexity': 5, 'automation': 8, 'risk': 3, 'investment': 1.5, 'completion': 90, 'priority': 'Low', 'description': 'Automated valuation of exchange-traded securities'},
        {'id': 'val_002', 'name': 'OTC Securities Valuation', 'category': 'Portfolio Valuation', 'complexity': 8, 'automation': 4, 'risk': 8, 'investment': 3.8, 'completion': 55, 'priority': 'High', 'description': 'Over-the-counter securities pricing and valuation'},
        {'id': 'val_003', 'name': 'FX Rates Processing', 'category': 'Portfolio Valuation', 'complexity': 4, 'automation': 9, 'risk': 2, 'investment': 0.8, 'completion': 95, 'priority': 'Low', 'description': 'Foreign exchange rate feeds and processing'},
        
        # Trade Capture Workstreams
        {'id': 'trade_001', 'name': 'Cash Trade Processing', 'category': 'Trade Capture', 'complexity': 5, 'automation': 7, 'risk': 4, 'investment': 2.0, 'completion': 75, 'priority': 'Medium', 'description': 'Cash transaction capture and processing'},
        {'id': 'trade_002', 'name': 'Derivative Trade Capture', 'category': 'Trade Capture', 'complexity': 9, 'automation': 5, 'risk': 9, 'investment': 4.5, 'completion': 40, 'priority': 'High', 'description': 'Complex derivative instrument trade processing'},
        {'id': 'trade_003', 'name': 'FX Hedging Operations', 'category': 'Trade Capture', 'complexity': 7, 'automation': 6, 'risk': 6, 'investment': 2.8, 'completion': 60, 'priority': 'Medium', 'description': 'Foreign exchange hedging trade management'},
        
        # Reconciliation Workstreams
        {'id': 'recon_001', 'name': 'Stock Reconciliation', 'category': 'Reconciliation', 'complexity': 6, 'automation': 5, 'risk': 6, 'investment': 2.2, 'completion': 70, 'priority': 'Medium', 'description': 'Stock position reconciliation with custodians'},
        {'id': 'recon_002', 'name': 'Cash Reconciliation', 'category': 'Reconciliation', 'complexity': 5, 'automation': 6, 'risk': 5, 'investment': 1.9, 'completion': 80, 'priority': 'Medium', 'description': 'Cash balance reconciliation across accounts'},
        {'id': 'recon_003', 'name': 'Fund Reconciliation', 'category': 'Reconciliation', 'complexity': 8, 'automation': 3, 'risk': 8, 'investment': 3.5, 'completion': 35, 'priority': 'High', 'description': 'Fund-level reconciliation and break analysis'},
        
        # Corporate Actions
        {'id': 'corp_001', 'name': 'Mandatory Corp Actions', 'category': 'Corporate Actions', 'complexity': 6, 'automation': 7, 'risk': 5, 'investment': 2.1, 'completion': 85, 'priority': 'Low', 'description': 'Automatic processing of mandatory corporate actions'},
        {'id': 'corp_002', 'name': 'Voluntary Corp Actions', 'category': 'Corporate Actions', 'complexity': 8, 'automation': 4, 'risk': 7, 'investment': 3.2, 'completion': 50, 'priority': 'High', 'description': 'Complex voluntary corporate action elections'},
        
        # Expense Management
        {'id': 'exp_001', 'name': 'Performance Fees', 'category': 'Expense Management', 'complexity': 9, 'automation': 3, 'risk': 8, 'investment': 4.0, 'completion': 30, 'priority': 'High', 'description': 'Performance fee calculations and accruals'},
        {'id': 'exp_002', 'name': 'Invoice Management', 'category': 'Expense Management', 'complexity': 4, 'automation': 8, 'risk': 3, 'investment': 1.2, 'completion': 90, 'priority': 'Low', 'description': 'Automated invoice processing and approval'},
        
        # Reporting
        {'id': 'rep_001', 'name': 'Regulatory Reporting', 'category': 'Reporting', 'complexity': 8, 'automation': 5, 'risk': 9, 'investment': 3.8, 'completion': 55, 'priority': 'High', 'description': 'Automated regulatory report generation'},
        {'id': 'rep_002', 'name': 'Client Reporting', 'category': 'Reporting', 'complexity': 6, 'automation': 6, 'risk': 4, 'investment': 2.3, 'completion': 75, 'priority': 'Medium', 'description': 'Customized client report generation'},
    ]

# Initialize session state for capital projects
if 'capital_project_data' not in st.session_state:
    st.session_state.capital_project_data = pd.DataFrame()
if 'comment_variance' not in st.session_state:
    st.session_state.comment_variance = ""
if 'comment_impact' not in st.session_state:
    st.session_state.comment_impact = ""
if 'comment_bottom5' not in st.session_state:
    st.session_state.comment_bottom5 = ""
if 'reports_ready' not in st.session_state:
    st.session_state.reports_ready = False

# Initialize session state for P&L Analysis
if 'pl_data' not in st.session_state:
    st.session_state.pl_data = pd.DataFrame()
if 'pl_template_downloaded' not in st.session_state:
    st.session_state.pl_template_downloaded = False

# Initialize session state for Competitors Analysis
if 'competitors_data' not in st.session_state:
    st.session_state.competitors_data = pd.DataFrame()
if 'competitors_template_downloaded' not in st.session_state:
    st.session_state.competitors_template_downloaded = False

# Initialize session state for Business Cases
if 'business_cases' not in st.session_state:
    st.session_state.business_cases = []
if 'business_case_data' not in st.session_state:
    st.session_state.business_case_data = pd.DataFrame()
if 'parking_lot' not in st.session_state:
    st.session_state.parking_lot = []
if 'backlog' not in st.session_state:
    st.session_state.backlog = []
if 'roadmap' not in st.session_state:
    st.session_state.roadmap = []

@st.cache_data
def load_capital_project_data(uploaded_file: io.BytesIO) -> pd.DataFrame:
    """
    Loads and preprocesses capital project data from a CSV or Excel file.
    """
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_year_str = str(current_year)
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

    def clean_col_name(col_name: str) -> str:
        """Cleans a single column name."""
        col_name = str(col_name).strip().replace(' ', '_').replace('+', '_').replace('.', '_').replace('-', '_')
        col_name = '_'.join(filter(None, col_name.split('_')))
        col_name = col_name.upper()
        corrections = {
            'PROJEC_TID': 'PROJECT_ID', 'INI_MATIVE_PROGRAM': 'INITIATIVE_PROGRAM',
            'ALL_PRIOR_YEARS_A': 'ALL_PRIOR_YEARS_ACTUALS', 'C_URRENT_EAC': 'CURRENT_EAC',
            'QE_RUN_RATE': 'QE_RUN_RATE', 'RATE_1': 'RATE_SUPPLEMENTARY'
        }
        return corrections.get(col_name, col_name)

    df.columns = [clean_col_name(col) for col in df.columns]

    cols = []
    seen = {}
    for col in df.columns:
        original_col = col
        count = seen.get(col, 0)
        if count > 0:
            col = f"{col}_{count}"
        cols.append(col)
        seen[original_col] = count + 1
    df.columns = cols

    financial_pattern = r'^(20\d{2}_\d{2}_(A|F|CP)(_\d+)?|ALL_PRIOR_YEARS_ACTUALS|BUSINESS_ALLOCATION|CURRENT_EAC|QE_FORECAST_VS_QE_PLAN|FORECAST_VS_BA|YE_RUN|RATE|QE_RUN|RATE_SUPPLEMENTARY)$'
    financial_cols_to_convert = [col for col in df.columns if pd.Series([col]).str.contains(financial_pattern, regex=True).any()]

    for col in financial_cols_to_convert:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip().replace('', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    monthly_col_pattern = re.compile(rf'^{current_year}_\d{{2}}_([AF]|CP)$')
    monthly_actuals_cols, monthly_forecasts_cols, monthly_plan_cols = [], [], []
    for col in df.columns:
        match = monthly_col_pattern.match(col)
        if match:
            col_type = match.group(1)
            if col_type == 'A': monthly_actuals_cols.append(col)
            elif col_type == 'F': monthly_forecasts_cols.append(col)
            elif col_type == 'CP': monthly_plan_cols.append(col)

    for col_list in [monthly_actuals_cols, monthly_forecasts_cols, monthly_plan_cols]:
        for col in col_list:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df[f'TOTAL_{current_year}_ACTUALS'] = df[monthly_actuals_cols].sum(axis=1) if monthly_actuals_cols else 0
    df[f'TOTAL_{current_year}_FORECASTS'] = df[monthly_forecasts_cols].sum(axis=1) if monthly_forecasts_cols else 0
    df[f'TOTAL_{current_year}_CAPITAL_PLAN'] = df[monthly_plan_cols].sum(axis=1) if monthly_plan_cols else 0

    if 'ALL_PRIOR_YEARS_ACTUALS' in df.columns:
        df['TOTAL_ACTUALS_TO_DATE'] = df['ALL_PRIOR_YEARS_ACTUALS'] + df[f'TOTAL_{current_year}_ACTUALS']
    else:
        df['TOTAL_ACTUALS_TO_DATE'] = df[f'TOTAL_{current_year}_ACTUALS']
        st.warning("Column 'ALL_PRIOR_YEARS_ACTUALS' not found.")

    ytd_actual_cols = [col for col in monthly_actuals_cols if int(col.split('_')[1]) <= current_month]
    df['SUM_ACTUAL_SPEND_YTD'] = df[ytd_actual_cols].sum(axis=1) if ytd_actual_cols else 0
    df['SUM_OF_FORECASTED_NUMBERS'] = df[f'TOTAL_{current_year}_FORECASTS']
    df['RUN_RATE_PER_MONTH'] = (df[f'TOTAL_{current_year}_ACTUALS'] + df[f'TOTAL_{current_year}_FORECASTS']) / 12

    if 'BUSINESS_ALLOCATION' in df.columns:
        df['CAPITAL_VARIANCE'] = df['BUSINESS_ALLOCATION'] - df[f'TOTAL_{current_year}_FORECASTS']
        df['CAPITAL_UNDERSPEND'] = df['CAPITAL_VARIANCE'].apply(lambda x: x if x > 0 else 0)
        df['CAPITAL_OVERSPEND'] = df['CAPITAL_VARIANCE'].apply(lambda x: abs(x) if x < 0 else 0)
    else:
        df['CAPITAL_VARIANCE'], df['CAPITAL_UNDERSPEND'], df['CAPITAL_OVERSPEND'] = 0, 0, 0
        st.warning("Column 'BUSINESS_ALLOCATION' not found.")

    df['NET_REALLOCATION_AMOUNT'] = df['CAPITAL_UNDERSPEND'] - df['CAPITAL_OVERSPEND']
    
    num_actual_months = len(ytd_actual_cols) if ytd_actual_cols else 1
    num_forecast_months = len(monthly_forecasts_cols) if monthly_forecasts_cols else 1
    df['AVG_ACTUAL_SPEND'] = df['SUM_ACTUAL_SPEND_YTD'] / num_actual_months
    df['AVG_FORECAST_SPEND'] = df[f'TOTAL_{current_year}_FORECASTS'] / num_forecast_months
    df['TOTAL_SPEND_VARIANCE'] = df[f'TOTAL_{current_year}_ACTUALS'] - df[f'TOTAL_{current_year}_FORECASTS']

    monthly_af_variance_cols = []
    for i in range(1, 13):
        actual_col, forecast_col = f'{current_year}_{i:02d}_A', f'{current_year}_{i:02d}_F'
        if actual_col in df.columns and forecast_col in df.columns:
            variance_col_name = f'{current_year}_{i:02d}_AF_VARIANCE'
            df[variance_col_name] = df[actual_col] - df[forecast_col]
            monthly_af_variance_cols.append(variance_col_name)

    df['AVERAGE_MONTHLY_SPREAD_SCORE'] = df[monthly_af_variance_cols].abs().mean(axis=1) if monthly_af_variance_cols else 0
    return df

def generate_capital_html_report(metrics, filtered_df):
    """Generates a comprehensive HTML report of capital project dashboard state."""
    current_year = datetime.now().year
    
    report_html = f"""
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Capital Project Report</title><style>
    body{{font-family:sans-serif;margin:20px;color:#333}}h1,h2,h3{{color:#004d40}}.metric-container{{display:flex;justify-content:space-around;flex-wrap:wrap;margin-bottom:20px}}
    .metric-box{{border:1px solid #ddd;border-radius:8px;padding:15px;margin:10px;flex:1;min-width:200px;text-align:center;background-color:#f9f9f9}}
    .metric-label{{font-size:0.9em;color:#555}}.metric-value{{font-size:1.5em;font-weight:bold;color:#222;margin-top:5px}}
    table{{width:100%;border-collapse:collapse;margin-top:20px}}th,td{{border:1px solid #ddd;padding:8px;text-align:left}}th{{background-color:#e6f2f0}}
    footer{{text-align:center;margin-top:50px;padding-top:20px;border-top:1px solid #eee;font-size:0.8em;color:#777}}
    </style></head><body>
    <h1>Capital Project Portfolio Report</h1><p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <h2>Key Metrics Overview</h2><div class="metric-container">
    {''.join([f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>' for label, value in metrics.items()])}
    </div>
    <h2>Project Portfolio Summary</h2>
    {filtered_df.head(10).to_html(index=False, classes='table')}
    <footer><p>Generated by Capital Project Portfolio Dashboard</p></footer>
    </body></html>"""
    return report_html

def generate_capital_excel_report(metrics, filtered_df):
    """Generates a multi-sheet Excel report for capital projects."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        summary_df = pd.DataFrame([metrics])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        filtered_df.to_excel(writer, sheet_name='Project_Details', index=False)
    return output.getvalue()

# P&L Analysis Functions
def create_pl_template():
    """Create a comprehensive P&L template for Fund Admin/Accounting Product."""
    
    # Sample data structure for P&L analysis
    template_data = {
        # Client Information
        'Client_Name': ['Global Asset Management', 'Private Equity Fund A', 'Hedge Fund Beta', 'Real Estate Fund C', 'Infrastructure Fund D'],
        'Fund_Name': ['Global Equity Fund', 'PE Growth Fund', 'Long/Short Equity', 'Commercial RE Fund', 'Infrastructure Debt'],
        'Fund_AUM_USD_Millions': [2500, 800, 1200, 600, 1500],
        'Number_of_Funds': [15, 3, 8, 4, 6],
        'Service_Start_Date': ['2023-01-01', '2023-03-15', '2022-11-01', '2024-01-01', '2023-06-01'],
        
        # Revenue Components
        'Total_Annual_Revenue_USD': [750000, 240000, 380000, 180000, 450000],
        'Fund_Accounting_Revenue_USD': [300000, 96000, 152000, 72000, 180000],
        'Fund_Administration_Revenue_USD': [225000, 72000, 114000, 54000, 135000],
        'Transfer_Agency_Revenue_USD': [150000, 48000, 76000, 36000, 90000],
        'Regulatory_Reporting_Revenue_USD': [75000, 24000, 38000, 18000, 45000],
        
        # Rate Card Information
        'Fund_Accounting_Rate_Per_Fund': [20000, 32000, 19000, 18000, 30000],
        'Administration_Rate_Per_Fund': [15000, 24000, 14250, 13500, 22500],
        'Transfer_Agency_Rate_Per_Investor': [150, 200, 127, 120, 188],
        'Number_of_Investors': [1000, 240, 600, 300, 480],
        
        # Direct Labor Costs
        'Fund_Accountants_Required': [3.0, 1.0, 2.0, 1.0, 2.0],
        'Average_Accountant_Salary_USD': [85000, 85000, 85000, 85000, 85000],
        'Fully_Burdened_Cost_Multiplier': [1.4, 1.4, 1.4, 1.4, 1.4],
        'Senior_Manager_Time_Percent': [15, 20, 18, 25, 20],
        'Manager_Hourly_Rate_USD': [150, 150, 150, 150, 150],
        
        # Operational Metrics
        'Monthly_NAV_Calculations': [15, 3, 8, 4, 6],
        'Investor_Transactions_Per_Month': [200, 50, 120, 60, 80],
        'Change_Requests_Per_Month': [25, 8, 15, 6, 12],
        'Regulatory_Reports_Per_Quarter': [12, 6, 9, 6, 8],
        
        # Technology & Infrastructure Costs
        'Software_License_Cost_USD': [15000, 8000, 12000, 6000, 10000],
        'Data_Provider_Costs_USD': [25000, 10000, 18000, 8000, 15000],
        'Cloud_Infrastructure_USD': [8000, 3000, 5000, 2500, 4500],
        
        # Overhead Allocation Drivers
        'Office_Space_Allocation_SqFt': [1200, 400, 800, 400, 600],
        'Compliance_Hours_Per_Month': [40, 15, 25, 10, 20],
        'Risk_Management_Hours_Per_Month': [30, 10, 20, 8, 15],
        
        # Quality & SLA Metrics
        'NAV_Accuracy_Percentage': [99.95, 99.90, 99.93, 99.88, 99.92],
        'On_Time_Delivery_Percentage': [98.5, 97.8, 98.2, 96.5, 97.9],
        'Client_Satisfaction_Score': [4.8, 4.6, 4.7, 4.4, 4.5],
        
        # Additional Revenue Streams
        'Ad_Hoc_Services_Revenue_USD': [25000, 8000, 15000, 5000, 12000],
        'Training_Services_Revenue_USD': [5000, 2000, 3000, 1000, 2500],
        'Consulting_Revenue_USD': [15000, 5000, 8000, 3000, 7000]
    }
    
    return pd.DataFrame(template_data)

def load_pl_data(uploaded_file):
    """Load and validate P&L data from uploaded file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic validation
        required_columns = ['Client_Name', 'Fund_Name', 'Total_Annual_Revenue_USD', 'Fund_AUM_USD_Millions']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

def calculate_pl_metrics(df):
    """Calculate comprehensive P&L metrics and allocations."""
    if df.empty:
        return pd.DataFrame()
    
    # Create a copy for calculations
    df_calc = df.copy()
    
    # Calculate direct labor costs
    df_calc['Total_Direct_Labor_Cost'] = (
        df_calc['Fund_Accountants_Required'] * 
        df_calc['Average_Accountant_Salary_USD'] * 
        df_calc['Fully_Burdened_Cost_Multiplier']
    )
    
    # Calculate manager oversight costs
    df_calc['Manager_Oversight_Cost'] = (
        df_calc['Senior_Manager_Time_Percent'] / 100 * 
        df_calc['Manager_Hourly_Rate_USD'] * 
        2080  # Annual hours
    )
    
    # Calculate technology costs per client
    df_calc['Total_Technology_Cost'] = (
        df_calc['Software_License_Cost_USD'] + 
        df_calc['Data_Provider_Costs_USD'] + 
        df_calc['Cloud_Infrastructure_USD']
    )
    
    # Calculate total direct costs
    df_calc['Total_Direct_Costs'] = (
        df_calc['Total_Direct_Labor_Cost'] + 
        df_calc['Manager_Oversight_Cost'] + 
        df_calc['Total_Technology_Cost']
    )
    
    # Calculate overhead allocation (15% of total revenue as example)
    df_calc['Overhead_Allocation'] = df_calc['Total_Annual_Revenue_USD'] * 0.15
    
    # Calculate total costs
    df_calc['Total_Costs'] = df_calc['Total_Direct_Costs'] + df_calc['Overhead_Allocation']
    
    # Calculate profitability metrics
    df_calc['Gross_Profit'] = df_calc['Total_Annual_Revenue_USD'] - df_calc['Total_Costs']
    df_calc['Gross_Margin_Percent'] = (df_calc['Gross_Profit'] / df_calc['Total_Annual_Revenue_USD']) * 100
    
    # Calculate revenue per fund metrics
    df_calc['Revenue_Per_Fund'] = df_calc['Total_Annual_Revenue_USD'] / df_calc['Number_of_Funds']
    df_calc['Cost_Per_Fund'] = df_calc['Total_Costs'] / df_calc['Number_of_Funds']
    df_calc['Profit_Per_Fund'] = df_calc['Gross_Profit'] / df_calc['Number_of_Funds']
    
    # Calculate AUM-based metrics
    df_calc['Revenue_Per_AUM_BPS'] = (df_calc['Total_Annual_Revenue_USD'] / (df_calc['Fund_AUM_USD_Millions'] * 1000000)) * 10000
    df_calc['Cost_Per_AUM_BPS'] = (df_calc['Total_Costs'] / (df_calc['Fund_AUM_USD_Millions'] * 1000000)) * 10000
    
    return df_calc

def create_pl_summary_charts(df):
    """Create comprehensive P&L visualization charts."""
    if df.empty:
        return None, None, None, None
    
    # Revenue breakdown chart
    revenue_fig = go.Figure(data=[
        go.Bar(name='Fund Accounting', x=df['Client_Name'], y=df['Fund_Accounting_Revenue_USD']),
        go.Bar(name='Fund Administration', x=df['Client_Name'], y=df['Fund_Administration_Revenue_USD']),
        go.Bar(name='Transfer Agency', x=df['Client_Name'], y=df['Transfer_Agency_Revenue_USD']),
        go.Bar(name='Regulatory Reporting', x=df['Client_Name'], y=df['Regulatory_Reporting_Revenue_USD'])
    ])
    revenue_fig.update_layout(
        title="Revenue Breakdown by Service Line",
        barmode='stack',
        xaxis_title="Client",
        yaxis_title="Revenue (USD)",
        height=500
    )
    
    # Cost allocation chart
    cost_fig = go.Figure(data=[
        go.Bar(name='Direct Labor', x=df['Client_Name'], y=df['Total_Direct_Labor_Cost']),
        go.Bar(name='Manager Oversight', x=df['Client_Name'], y=df['Manager_Oversight_Cost']),
        go.Bar(name='Technology', x=df['Client_Name'], y=df['Total_Technology_Cost']),
        go.Bar(name='Overhead', x=df['Client_Name'], y=df['Overhead_Allocation'])
    ])
    cost_fig.update_layout(
        title="Cost Allocation by Category",
        barmode='stack',
        xaxis_title="Client",
        yaxis_title="Cost (USD)",
        height=500
    )
    
    # Profitability analysis
    profit_fig = go.Figure()
    profit_fig.add_trace(go.Bar(
        name='Revenue',
        x=df['Client_Name'],
        y=df['Total_Annual_Revenue_USD'],
        marker_color='lightblue'
    ))
    profit_fig.add_trace(go.Bar(
        name='Costs',
        x=df['Client_Name'],
        y=df['Total_Costs'],
        marker_color='lightcoral'
    ))
    profit_fig.add_trace(go.Scatter(
        name='Gross Margin %',
        x=df['Client_Name'],
        y=df['Gross_Margin_Percent'],
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='green', width=3),
        marker=dict(size=8)
    ))
    profit_fig.update_layout(
        title="Revenue vs Costs Analysis",
        xaxis_title="Client",
        yaxis_title="Amount (USD)",
        yaxis2=dict(title="Gross Margin (%)", overlaying='y', side='right'),
        height=500
    )
    
    # AUM efficiency chart
    aum_fig = go.Figure()
    aum_fig.add_trace(go.Scatter(
        x=df['Fund_AUM_USD_Millions'],
        y=df['Revenue_Per_AUM_BPS'],
        mode='markers',
        marker=dict(
            size=df['Number_of_Funds'] * 3,
            color=df['Gross_Margin_Percent'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Gross Margin %")
        ),
        text=df['Client_Name'],
        hovertemplate='<b>%{text}</b><br>' +
                      'AUM: $%{x}M<br>' +
                      'Revenue per AUM: %{y:.1f} bps<br>' +
                      '<extra></extra>'
    ))
    aum_fig.update_layout(
        title="Revenue Efficiency: Revenue per AUM vs Total AUM",
        xaxis_title="Fund AUM (USD Millions)",
        yaxis_title="Revenue per AUM (Basis Points)",
        height=500
    )
    
    return revenue_fig, cost_fig, profit_fig, aum_fig

def generate_pl_excel_report(df, summary_stats):
    """Generate comprehensive P&L Excel report."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write main data
        df.to_excel(writer, sheet_name='Detailed_PL_Analysis', index=False)
        
        # Write summary statistics
        summary_df = pd.DataFrame([summary_stats])
        summary_df.to_excel(writer, sheet_name='Executive_Summary', index=False)
        
        # Write service line breakdown
        service_breakdown = df.groupby('Client_Name')[
            ['Fund_Accounting_Revenue_USD', 'Fund_Administration_Revenue_USD', 
             'Transfer_Agency_Revenue_USD', 'Regulatory_Reporting_Revenue_USD']
        ].sum()
        service_breakdown.to_excel(writer, sheet_name='Service_Line_Breakdown')
        
        # Write profitability ranking
        profitability_ranking = df[['Client_Name', 'Fund_Name', 'Gross_Profit', 'Gross_Margin_Percent']].sort_values('Gross_Margin_Percent', ascending=False)
        profitability_ranking.to_excel(writer, sheet_name='Profitability_Ranking', index=False)
    
    return output.getvalue()

# Competitors Analysis Functions
def create_competitors_template():
    """Create a comprehensive competitors analysis template."""
    
    template_data = {
        # Competitor Information
        'Competitor_Name': [
            'State Street', 'JPMorgan Chase', 'BNY Mellon', 'HSBC', 'Citi',
            'Northern Trust', 'Deutsche Bank', 'Credit Suisse', 'UBS', 'Goldman Sachs'
        ],
        'Competitor_Type': [
            'Custody Bank', 'Universal Bank', 'Custody Bank', 'Universal Bank', 'Universal Bank',
            'Custody Bank', 'Universal Bank', 'Universal Bank', 'Universal Bank', 'Investment Bank'
        ],
        'Market_Cap_USD_Billions': [65.2, 460.3, 45.8, 130.7, 102.5, 18.9, 15.2, 8.1, 55.4, 118.3],
        'Headquarters': [
            'Boston, USA', 'New York, USA', 'New York, USA', 'London, UK', 'New York, USA',
            'Chicago, USA', 'Frankfurt, Germany', 'Zurich, Switzerland', 'Zurich, Switzerland', 'New York, USA'
        ],
        'Founded_Year': [1792, 1799, 1784, 1865, 1812, 1889, 1870, 1856, 1862, 1869],
        
        # Fund Administration Metrics
        'Assets_Under_Administration_USD_Trillions': [40.0, 30.0, 46.7, 4.9, 22.0, 15.8, 1.4, 1.8, 4.4, 2.8],
        'Number_of_Funds_Administered': [15000, 8000, 18000, 3500, 7500, 6000, 1200, 1800, 2800, 2200],
        'Fund_Accounting_Clients': [2800, 1500, 3200, 800, 1600, 1200, 300, 450, 650, 480],
        'Transfer_Agency_Services': ['Yes', 'Yes', 'Yes', 'Limited', 'Yes', 'Yes', 'No', 'Limited', 'Limited', 'No'],
        'Regulatory_Reporting_Automation': ['High', 'High', 'High', 'Medium', 'High', 'Medium', 'Low', 'Medium', 'Medium', 'Low'],
        
        # Technology & Innovation
        'Cloud_Native_Platform': ['Yes', 'Partial', 'Yes', 'No', 'Partial', 'Yes', 'No', 'No', 'Partial', 'No'],
        'AI_ML_Capabilities': ['Advanced', 'Advanced', 'Intermediate', 'Basic', 'Advanced', 'Intermediate', 'Basic', 'Basic', 'Intermediate', 'Advanced'],
        'API_Integration_Score': [9, 8, 9, 6, 8, 7, 5, 6, 7, 8],
        'Digital_Transformation_Stage': ['Leader', 'Leader', 'Leader', 'Follower', 'Leader', 'Challenger', 'Follower', 'Follower', 'Challenger', 'Leader'],
        'Blockchain_Capabilities': ['Yes', 'Yes', 'Limited', 'No', 'Yes', 'Limited', 'No', 'Limited', 'Yes', 'Yes'],
        
        # Market Position & Strategy
        'Market_Share_Percent': [18.5, 14.2, 22.1, 2.3, 10.4, 7.5, 0.7, 0.9, 2.1, 1.3],
        'Geographic_Presence': ['Global', 'Global', 'Global', 'Global', 'Global', 'US/Europe', 'Europe', 'Global', 'Global', 'Global'],
        'Target_Client_Segment': ['Institutional', 'All', 'Institutional', 'All', 'All', 'Institutional', 'Institutional', 'UHNW/Institutional', 'UHNW/Institutional', 'Institutional'],
        'Pricing_Strategy': ['Premium', 'Competitive', 'Premium', 'Competitive', 'Competitive', 'Premium', 'Competitive', 'Premium', 'Premium', 'Premium'],
        'ESG_Focus_Score': [8.5, 7.8, 8.2, 7.1, 7.5, 8.0, 6.8, 7.3, 7.9, 8.1],
        
        # Operational Metrics
        'Employee_Count': [39000, 271000, 48000, 220000, 240000, 22000, 82000, 45000, 72000, 45000],
        'Revenue_USD_Billions': [12.2, 119.5, 16.2, 50.4, 75.3, 6.8, 28.8, 15.3, 34.7, 47.4],
        'Technology_Investment_Percent': [15.2, 12.8, 16.1, 9.5, 13.4, 18.5, 8.2, 10.1, 11.7, 14.3],
        'Client_Satisfaction_Score': [8.2, 7.1, 8.4, 7.3, 7.0, 8.6, 6.8, 7.5, 7.8, 7.2],
        'Net_Promoter_Score': [42, 25, 48, 31, 22, 52, 18, 35, 39, 28],
        
        # Competitive Advantages & Disadvantages
        'Key_Strengths': [
            'Scale, Technology Innovation, Global Reach',
            'Universal Banking, Capital, Brand Recognition',
            'Custody Leadership, Client Service, Heritage',
            'Global Network, Trade Finance, Emerging Markets',
            'Universal Banking, Technology, Innovation',
            'Client Service, Technology, Niche Focus',
            'European Strength, Corporate Banking',
            'Wealth Management, Swiss Heritage',
            'Wealth Management, Global Presence',
            'Investment Banking, Technology Innovation'
        ],
        'Key_Weaknesses': [
            'Complex Structure, Regulatory Scrutiny',
            'Regulatory Issues, Complexity',
            'Technology Lag, Cost Structure',
            'Regulatory Issues, Profitability',
            'Regulatory Issues, Cost Structure',
            'Scale Limitations, Geographic Reach',
            'Profitability Issues, Limited Scale',
            'Regulatory Issues, Limited Scale',
            'Compliance Issues, Cost Structure',
            'Limited Fund Admin Focus, Volatility'
        ],
        
        # Recent Developments
        'Recent_Acquisitions': [
            'Brown Brothers Harriman Investor Services',
            'Global Shares',
            'Pershing Prime Services',
            'None (Recent)',
            'None (Recent)',
            'UBS Asset Services',
            'None (Recent)',
            'None (Recent)',
            'Wealthfront',
            'NextCapital'
        ],
        'Technology_Initiatives': [
            'State Street Alpha Platform',
            'JPM Coin, Blockchain',
            'BNY Mellon Digital',
            'HSBC Digital Vault',
            'Citi Cloud Platform',
            'Northern Trust Edge',
            'Deutsche Bank dbFlow',
            'Credit Suisse Digital',
            'UBS Neo',
            'Goldman Sachs Digital'
        ]
    }
    
    return pd.DataFrame(template_data)

def load_competitors_data(uploaded_file):
    """Load and validate competitors data from uploaded file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic validation
        required_columns = ['Competitor_Name', 'Assets_Under_Administration_USD_Trillions', 'Market_Share_Percent']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

def create_competitive_positioning_chart(df):
    """Create competitive positioning bubble chart."""
    if df.empty:
        return None
    
    fig = go.Figure()
    
    # Create bubble chart: Market Share vs Assets Under Administration
    fig.add_trace(go.Scatter(
        x=df['Assets_Under_Administration_USD_Trillions'],
        y=df['Market_Share_Percent'],
        mode='markers+text',
        marker=dict(
            size=df['Technology_Investment_Percent'] * 5,  # Size by tech investment
            color=df['Client_Satisfaction_Score'],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Client Satisfaction"),
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        text=df['Competitor_Name'],
        textposition="middle center",
        hovertemplate='<b>%{text}</b><br>' +
                     'AUA: $%{x:.1f}T<br>' +
                     'Market Share: %{y:.1f}%<br>' +
                     'Tech Investment: %{customdata[0]:.1f}%<br>' +
                     'Client Satisfaction: %{customdata[1]:.1f}/10<br>' +
                     'NPS: %{customdata[2]}<br>' +
                     '<extra></extra>',
        customdata=list(zip(df['Technology_Investment_Percent'], 
                           df['Client_Satisfaction_Score'],
                           df['Net_Promoter_Score']))
    ))
    
    fig.update_layout(
        title="Competitive Positioning: Assets Under Administration vs Market Share",
        xaxis_title="Assets Under Administration (USD Trillions)",
        yaxis_title="Market Share (%)",
        height=600,
        hovermode='closest'
    )
    
    return fig

def create_technology_capability_radar(df):
    """Create technology capability radar chart for top competitors."""
    if df.empty:
        return None
    
    # Select top 5 competitors by AUA
    top_competitors = df.nlargest(5, 'Assets_Under_Administration_USD_Trillions')
    
    fig = go.Figure()
    
    # Technology metrics for radar chart
    tech_metrics = ['API_Integration_Score', 'Technology_Investment_Percent', 'Client_Satisfaction_Score']
    
    for _, competitor in top_competitors.iterrows():
        values = [
            competitor['API_Integration_Score'],
            competitor['Technology_Investment_Percent'],
            competitor['Client_Satisfaction_Score']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=['API Integration (1-10)', 'Tech Investment (%)', 'Client Satisfaction (1-10)'],
            fill='toself',
            name=competitor['Competitor_Name'],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 20])
        ),
        title="Technology Capabilities Comparison - Top 5 Competitors",
        height=600
    )
    
    return fig

def create_market_evolution_analysis(df):
    """Create market evolution and trend analysis."""
    if df.empty:
        return None
    
    # Categorize by digital transformation stage
    stages = df['Digital_Transformation_Stage'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=stages.index,
            y=stages.values,
            marker_color=['#2E8B57', '#4682B4', '#DAA520', '#DC143C'],
            text=stages.values,
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Digital Transformation Maturity Distribution",
        xaxis_title="Transformation Stage",
        yaxis_title="Number of Competitors",
        height=400
    )
    
    return fig

def generate_competitive_insights(df):
    """Generate strategic competitive insights."""
    if df.empty:
        return {}
    
    insights = {}
    
    # Market concentration
    top_3_share = df.nlargest(3, 'Market_Share_Percent')['Market_Share_Percent'].sum()
    insights['market_concentration'] = f"Top 3 players control {top_3_share:.1f}% of market"
    
    # Technology leaders
    tech_leaders = df[df['AI_ML_Capabilities'] == 'Advanced']['Competitor_Name'].tolist()
    insights['tech_leaders'] = f"AI/ML Leaders: {', '.join(tech_leaders)}"
    
    # Client satisfaction winners
    top_satisfaction = df.nlargest(3, 'Client_Satisfaction_Score')
    insights['satisfaction_leaders'] = top_satisfaction[['Competitor_Name', 'Client_Satisfaction_Score']].to_dict('records')
    
    # Geographic diversification
    global_players = len(df[df['Geographic_Presence'] == 'Global'])
    insights['geographic_reach'] = f"{global_players} competitors have global presence"
    
    # Innovation focus
    cloud_native = len(df[df['Cloud_Native_Platform'] == 'Yes'])
    insights['cloud_adoption'] = f"{cloud_native}/{len(df)} competitors are cloud-native"
    
    return insights

def generate_competitors_excel_report(df, insights):
    """Generate comprehensive competitors analysis Excel report."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Main competitor data
        df.to_excel(writer, sheet_name='Competitor_Analysis', index=False)
        
        # Market positioning data
        positioning_df = df[['Competitor_Name', 'Market_Share_Percent', 'Assets_Under_Administration_USD_Trillions', 
                           'Technology_Investment_Percent', 'Client_Satisfaction_Score']].copy()
        positioning_df.to_excel(writer, sheet_name='Market_Positioning', index=False)
        
        # Technology comparison
        tech_df = df[['Competitor_Name', 'AI_ML_Capabilities', 'API_Integration_Score', 'Cloud_Native_Platform', 
                     'Digital_Transformation_Stage']].copy()
        tech_df.to_excel(writer, sheet_name='Technology_Analysis', index=False)
        
        # Strategic insights
        insights_df = pd.DataFrame.from_dict(insights, orient='index', columns=['Insight'])
        insights_df.to_excel(writer, sheet_name='Strategic_Insights')
    
    return output.getvalue()

# Business Case Development Functions
def create_business_case_template():
    """Create a comprehensive business case template with qualifying examples.
    
    Template includes 5 sample business cases optimized to meet the ≥70 score 
    threshold for automatic promotion to the Parking Lot stage.
    """
    
    template_data = {
        # Project Information
        'Case_ID': ['BC_2024_001', 'BC_2024_002', 'BC_2024_003', 'BC_2024_004', 'BC_2024_005'],
        'Case_Title': [
            'AI-Powered NAV Calculation Enhancement',
            'Real-Time Regulatory Reporting Platform',
            'Client Portal Modernization Initiative',
            'Automated Reconciliation System',
            'Cloud Migration for Fund Administration'
        ],
        'Business_Owner': ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Lisa Brown', 'David Wilson'],
        'Region': ['North America', 'Europe', 'Asia Pacific', 'Global', 'North America'],
        'Priority_Level': ['High', 'Medium', 'High', 'Low', 'Medium'],
        'Request_Date': ['2024-01-15', '2024-02-01', '2024-01-30', '2024-02-15', '2024-03-01'],
        
        # Financial Information - Optimized for high scores
        'Estimated_Investment_USD': [2500000, 1800000, 3200000, 950000, 4500000],
        'Expected_Annual_Savings_USD': [1200000, 900000, 1600000, 600000, 2200000],  # Increased savings
        'Implementation_Duration_Months': [18, 12, 24, 8, 36],
        'ROI_Percentage': [48.0, 50.0, 50.0, 63.2, 48.9],  # Higher ROI for better Financial scores
        'Payback_Period_Months': [25, 24, 24, 19, 24],  # Shorter payback periods
        
        # Strategic Alignment - Enhanced for qualification
        'Strategic_Alignment_Score': [9.2, 8.8, 9.5, 8.5, 9.0],  # Higher strategic alignment
        'Technology_Complexity_Score': [6, 4, 7, 3, 5],  # Lower complexity scores higher
        'Implementation_Risk_Score': [5, 3, 6, 2, 4],  # Lower risk scores higher  
        'Client_Impact_Score': [9.5, 9.0, 9.8, 8.5, 9.2],  # High client impact
        'Regulatory_Impact_Score': [9, 10, 8, 9, 8],
        
        # Resource Requirements
        'FTE_Required': [12, 8, 15, 4, 20],
        'External_Vendor_Required': ['Yes', 'Yes', 'Yes', 'No', 'Yes'],
        'Technology_Investment_Percent': [60, 70, 55, 80, 65],
        'Change_Management_Effort': ['High', 'Medium', 'High', 'Low', 'Medium'],
        
        # Business Justification
        'Problem_Statement': [
            'Current NAV calculation process is manual and error-prone, taking 4 hours daily',
            'Regulatory reporting requires 15 FTE with high risk of errors and delays',
            'Legacy client portal has 2.3/10 satisfaction score and limited functionality',
            'Daily reconciliation process requires 6 FTE and has 15% error rate',
            'On-premise infrastructure limits scalability and increases operational risk'
        ],
        'Proposed_Solution': [
            'Implement AI/ML NAV calculation engine with real-time validation',
            'Deploy cloud-native regulatory reporting platform with automated workflows',
            'Build modern client portal with self-service capabilities and mobile access',
            'Implement automated reconciliation system with exception-based processing',
            'Migrate to cloud infrastructure with enhanced security and scalability'
        ],
        'Expected_Benefits': [
            'Reduce NAV calculation time by 85%, eliminate manual errors, improve accuracy to 99.9%',
            'Reduce regulatory reporting FTE by 60%, improve accuracy, ensure compliance',
            'Increase client satisfaction to 8.5/10, reduce support calls by 40%',
            'Reduce reconciliation FTE by 75%, improve accuracy to 98%',
            'Reduce infrastructure costs by 30%, improve system availability to 99.9%'
        ],
        
        # Current State Analysis - Designed for strong gap analysis
        'Current_Process_Efficiency': [4, 5, 3, 5, 4],  # Moderate current efficiency
        'Current_Error_Rate_Percent': [8, 6, 15, 10, 7],  # Reduced current error rates
        'Current_Client_Satisfaction': [6.8, 7.5, 4.2, 7.0, 7.2],  # Improved baseline satisfaction
        'Current_FTE_Count': [10, 12, 8, 6, 15],  # Current staffing levels
        
        # Target State Goals - Ambitious but achievable targets
        'Target_Process_Efficiency': [9, 9, 9, 9, 9],  # High target efficiency
        'Target_Error_Rate_Percent': [0.5, 0.2, 1.0, 1.0, 0.3],  # Low target error rates  
        'Target_Client_Satisfaction': [9.0, 8.8, 8.5, 8.2, 8.7],  # High target satisfaction
        'Target_FTE_Count': [4, 5, 4, 2, 6]  # Optimized FTE targets
    }
    
    # Create the main template DataFrame
    template_df = pd.DataFrame(template_data)
    
    # Add detailed example and calculation guide as additional sheets/rows
    example_case = pd.DataFrame({
        'Case_ID': ['EXAMPLE_CASE'],
        'Case_Title': ['📊 EXAMPLE: Digital Trade Processing Platform'],
        'Business_Owner': ['Example: Sarah Johnson'],
        'Region': ['Global'],
        'Priority_Level': ['High'],
        'Request_Date': ['2024-03-15'],
        
        # Financial - Designed to score ~85/100 in Financial category
        'Estimated_Investment_USD': [3000000],  # $3M investment
        'Expected_Annual_Savings_USD': [1800000],  # $1.8M annual savings  
        'Implementation_Duration_Months': [15],
        'ROI_Percentage': [60.0],  # High ROI: 60% scores 10/10 → Financial component: (10*0.6) = 6
        'Payback_Period_Months': [20],  # Good payback: 20mo scores 6.7/10 → Financial component: (6.7*0.4) = 2.7
        # Total Financial Score: (6 + 2.7) = 8.7/10 → Weighted: 8.7 * 30% = 2.61 points
        
        # Strategic - Designed to score ~90/100 
        'Strategic_Alignment_Score': [9.5],  # Excellent strategic fit → (9.5*0.7) = 6.65
        'Technology_Complexity_Score': [3],  # Low complexity scores high in feasibility 
        'Implementation_Risk_Score': [2],  # Very low risk
        'Client_Impact_Score': [9.0],  # High client impact → (9.0*0.3) = 2.7  
        'Regulatory_Impact_Score': [8],
        # Total Strategic Score: (6.65 + 2.7) = 9.35/10 → Weighted: 9.35 * 25% = 2.34 points
        
        # Resource Requirements
        'FTE_Required': [8],
        'External_Vendor_Required': ['Yes'],
        'Technology_Investment_Percent': [70],
        'Change_Management_Effort': ['Medium'],
        
        # Business Justification  
        'Problem_Statement': ['Current trade processing requires 48 hours with 8% error rate, causing client dissatisfaction and regulatory concerns. Manual processes consume 15 FTE and limit scalability for growth.'],
        'Proposed_Solution': ['Implement AI-powered digital trade processing platform with real-time validation, automated workflow routing, and integrated regulatory reporting capabilities.'],
        'Expected_Benefits': ['Reduce processing time to 2 hours (96% improvement), decrease error rate to 0.5% (94% reduction), improve client satisfaction from 6.5 to 9.0, reduce FTE requirement by 60%.'],
        
        # Current vs Target State - Designed for strong gap analysis
        'Current_Process_Efficiency': [3],  # Low current efficiency
        'Current_Error_Rate_Percent': [8],  # High current error rate
        'Current_Client_Satisfaction': [6.5],  # Moderate satisfaction
        'Current_FTE_Count': [15],  # High current staffing
        
        'Target_Process_Efficiency': [9],  # High target: Gap = 6 points → Impact score component
        'Target_Error_Rate_Percent': [0.5],  # Low target: Gap = 7.5% reduction → Impact score component  
        'Target_Client_Satisfaction': [9.0],  # High target: Gap = 2.5 points improvement
        'Target_FTE_Count': [6]  # Optimized: Gap = 9 FTE reduction → Resource score = 9*2 = 18 (capped at 10)
        # Impact Score: ((6*0.6) + (7.5*0.4)) = 6.6/10 → Weighted: 6.6 * 15% = 0.99 points
        # Resource Score: 10/10 → Weighted: 10 * 10% = 1.0 points
        # Feasibility Score: ((10-3)/10*10*0.5) + ((10-2)/10*10*0.5) = (3.5 + 4.0) = 7.5/10 → Weighted: 7.5 * 20% = 1.5 points
        
        # TOTAL EXAMPLE SCORE: 2.61 + 2.34 + 1.5 + 0.99 + 1.0 = 8.44/10 = 84.4/100 ✅ QUALIFIES FOR PARKING LOT
    })
    
    # Combine template with example
    full_template = pd.concat([template_df, example_case], ignore_index=True)
    
    return full_template

def load_business_case_data(uploaded_file):
    """Load and validate business case data from uploaded file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic validation
        required_columns = ['Case_Title', 'Estimated_Investment_USD', 'Expected_Annual_Savings_USD']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

def calculate_business_case_score(case_data):
    """Calculate comprehensive business case score with gap analysis."""
    
    scores = {}
    
    # Financial Score (30% weight)
    roi_score = min(case_data.get('ROI_Percentage', 0) / 50 * 10, 10)  # Normalize ROI to 10-point scale
    payback_score = max(10 - (case_data.get('Payback_Period_Months', 60) / 6), 0)  # Better score for shorter payback
    financial_score = (roi_score * 0.6 + payback_score * 0.4)
    scores['Financial'] = financial_score
    
    # Strategic Alignment Score (25% weight)
    strategic_score = case_data.get('Strategic_Alignment_Score', 5)
    client_impact = case_data.get('Client_Impact_Score', 5)
    strategic_combined = (strategic_score * 0.7 + client_impact * 0.3)
    scores['Strategic'] = strategic_combined
    
    # Implementation Feasibility Score (20% weight)
    complexity_penalty = (10 - case_data.get('Technology_Complexity_Score', 5)) / 10 * 10
    risk_penalty = (10 - case_data.get('Implementation_Risk_Score', 5)) / 10 * 10
    feasibility_score = (complexity_penalty * 0.5 + risk_penalty * 0.5)
    scores['Feasibility'] = feasibility_score
    
    # Business Impact Score (15% weight)
    efficiency_gain = (case_data.get('Target_Process_Efficiency', 5) - case_data.get('Current_Process_Efficiency', 5))
    error_reduction = max(0, case_data.get('Current_Error_Rate_Percent', 0) - case_data.get('Target_Error_Rate_Percent', 0))
    impact_score = min((efficiency_gain * 0.6 + error_reduction * 0.4), 10)
    scores['Impact'] = impact_score
    
    # Resource Efficiency Score (10% weight)
    fte_efficiency = max(0, case_data.get('Current_FTE_Count', 0) - case_data.get('Target_FTE_Count', 0))
    resource_score = min(fte_efficiency * 2, 10)  # Max 10 points
    scores['Resource'] = resource_score
    
    # Calculate overall score
    weights = {'Financial': 0.30, 'Strategic': 0.25, 'Feasibility': 0.20, 'Impact': 0.15, 'Resource': 0.10}
    overall_score = sum(scores[category] * weights[category] for category in scores)
    
    return overall_score, scores

def create_gap_analysis(case_data):
    """Perform detailed gap analysis between current and target state."""
    
    gaps = {}
    
    # Process Efficiency Gap
    efficiency_gap = case_data.get('Target_Process_Efficiency', 5) - case_data.get('Current_Process_Efficiency', 5)
    gaps['Process_Efficiency'] = {
        'current': case_data.get('Current_Process_Efficiency', 5),
        'target': case_data.get('Target_Process_Efficiency', 5),
        'gap': efficiency_gap,
        'improvement_percent': (efficiency_gap / case_data.get('Current_Process_Efficiency', 5)) * 100 if case_data.get('Current_Process_Efficiency', 5) > 0 else 0
    }
    
    # Error Rate Gap
    error_gap = case_data.get('Current_Error_Rate_Percent', 0) - case_data.get('Target_Error_Rate_Percent', 0)
    gaps['Error_Rate'] = {
        'current': case_data.get('Current_Error_Rate_Percent', 0),
        'target': case_data.get('Target_Error_Rate_Percent', 0),
        'gap': error_gap,
        'improvement_percent': (error_gap / case_data.get('Current_Error_Rate_Percent', 1)) * 100 if case_data.get('Current_Error_Rate_Percent', 1) > 0 else 0
    }
    
    # Client Satisfaction Gap
    satisfaction_gap = case_data.get('Target_Client_Satisfaction', 5) - case_data.get('Current_Client_Satisfaction', 5)
    gaps['Client_Satisfaction'] = {
        'current': case_data.get('Current_Client_Satisfaction', 5),
        'target': case_data.get('Target_Client_Satisfaction', 5),
        'gap': satisfaction_gap,
        'improvement_percent': (satisfaction_gap / case_data.get('Current_Client_Satisfaction', 5)) * 100 if case_data.get('Current_Client_Satisfaction', 5) > 0 else 0
    }
    
    # FTE Efficiency Gap
    fte_gap = case_data.get('Current_FTE_Count', 0) - case_data.get('Target_FTE_Count', 0)
    gaps['FTE_Count'] = {
        'current': case_data.get('Current_FTE_Count', 0),
        'target': case_data.get('Target_FTE_Count', 0),
        'gap': fte_gap,
        'improvement_percent': (fte_gap / case_data.get('Current_FTE_Count', 1)) * 100 if case_data.get('Current_FTE_Count', 1) > 0 else 0
    }
    
    return gaps

def integrate_supporting_data(case_data):
    """Integrate relevant data from other tabs to support the business case."""
    
    supporting_data = {}
    
    # Workstream Data Integration
    if st.session_state.workstream_data:
        workstream_df = pd.DataFrame(st.session_state.workstream_data)
        
        # Find related workstreams
        case_title = case_data.get('Case_Title', '').lower()
        related_workstreams = []
        
        for _, ws in workstream_df.iterrows():
            ws_name = ws['name'].lower()
            # Simple keyword matching
            if any(keyword in ws_name for keyword in ['nav', 'calculation', 'reporting', 'reconciliation']):
                related_workstreams.append({
                    'name': ws['name'],
                    'complexity': ws['complexity'],
                    'automation': ws['automation'],
                    'risk': ws['risk'],
                    'investment': ws['investment'],
                    'completion': ws['completion']
                })
        
        supporting_data['related_workstreams'] = related_workstreams
    
    # P&L Data Integration
    if not st.session_state.pl_data.empty:
        pl_df = st.session_state.pl_data
        
        # Calculate potential revenue impact
        avg_revenue_per_client = pl_df['Total_Annual_Revenue_USD'].mean()
        total_clients = len(pl_df)
        
        supporting_data['revenue_context'] = {
            'avg_revenue_per_client': avg_revenue_per_client,
            'total_clients': total_clients,
            'potential_revenue_at_risk': avg_revenue_per_client * 0.1  # Assume 10% at risk
        }
    
    # Competitors Data Integration
    if not st.session_state.competitors_data.empty:
        comp_df = st.session_state.competitors_data
        
        # Technology investment benchmarks
        avg_tech_investment = comp_df['Technology_Investment_Percent'].mean()
        tech_leaders = comp_df[comp_df['AI_ML_Capabilities'] == 'Advanced']['Competitor_Name'].tolist()
        
        supporting_data['competitive_context'] = {
            'avg_tech_investment': avg_tech_investment,
            'tech_leaders': tech_leaders,
            'market_pressure': len(tech_leaders) / len(comp_df) * 100
        }
    
    return supporting_data

def generate_business_case_document(case_data, score_data, gap_analysis, supporting_data):
    """Generate a comprehensive Word document for the business case."""
    
    # Since python-docx might not be available, we'll create a comprehensive text document
    # that can be easily converted to Word format
    
    document_content = f"""
# BUSINESS CASE DOCUMENT
## {case_data.get('Case_Title', 'Untitled Business Case')}

---

## EXECUTIVE SUMMARY

**Case ID:** {case_data.get('Case_ID', 'N/A')}
**Business Owner:** {case_data.get('Business_Owner', 'N/A')}
**Region:** {case_data.get('Region', 'N/A')}
**Priority Level:** {case_data.get('Priority_Level', 'N/A')}
**Request Date:** {case_data.get('Request_Date', 'N/A')}

**Overall Business Case Score:** {score_data[0]:.2f}/10

### Investment Summary
- **Total Investment:** ${case_data.get('Estimated_Investment_USD', 0):,.0f}
- **Expected Annual Savings:** ${case_data.get('Expected_Annual_Savings_USD', 0):,.0f}
- **ROI:** {case_data.get('ROI_Percentage', 0):.1f}%
- **Payback Period:** {case_data.get('Payback_Period_Months', 0)} months
- **Implementation Duration:** {case_data.get('Implementation_Duration_Months', 0)} months

---

## BUSINESS JUSTIFICATION

### Problem Statement
{case_data.get('Problem_Statement', 'No problem statement provided.')}

### Proposed Solution
{case_data.get('Proposed_Solution', 'No solution description provided.')}

### Expected Benefits
{case_data.get('Expected_Benefits', 'No benefits description provided.')}

---

## SCORING ANALYSIS

### Detailed Scores
"""
    
    for category, score in score_data[1].items():
        document_content += f"- **{category}:** {score:.2f}/10\n"
    
    document_content += f"""

### Score Interpretation
- **8.0-10.0:** Excellent - High priority for immediate implementation
- **6.0-7.9:** Good - Consider for next planning cycle
- **4.0-5.9:** Fair - Requires improvement or postponement
- **0.0-3.9:** Poor - Not recommended for implementation

**Current Score: {score_data[0]:.2f}/10 - {get_score_category(score_data[0])}**

---

## GAP ANALYSIS

### Current State vs Target State Analysis
"""
    
    for metric, gap_data in gap_analysis.items():
        document_content += f"""
#### {metric.replace('_', ' ')}
- **Current State:** {gap_data['current']}
- **Target State:** {gap_data['target']}
- **Gap:** {gap_data['gap']:.2f}
- **Improvement:** {gap_data['improvement_percent']:.1f}%
"""
    
    document_content += f"""

---

## SUPPORTING DATA ANALYSIS

### Related Workstreams
"""
    
    if supporting_data.get('related_workstreams'):
        for ws in supporting_data['related_workstreams']:
            document_content += f"""
- **{ws['name']}**
  - Complexity: {ws['complexity']}/10
  - Automation: {ws['automation']}/10
  - Risk: {ws['risk']}/10
  - Investment: ${ws['investment']:.1f}M
  - Completion: {ws['completion']}%
"""
    else:
        document_content += "No related workstreams identified.\n"
    
    if supporting_data.get('revenue_context'):
        rev_ctx = supporting_data['revenue_context']
        document_content += f"""

### Revenue Impact Analysis
- **Average Revenue per Client:** ${rev_ctx['avg_revenue_per_client']:,.0f}
- **Total Client Base:** {rev_ctx['total_clients']}
- **Potential Revenue at Risk:** ${rev_ctx['potential_revenue_at_risk']:,.0f}
"""
    
    if supporting_data.get('competitive_context'):
        comp_ctx = supporting_data['competitive_context']
        document_content += f"""

### Competitive Context
- **Industry Avg Tech Investment:** {comp_ctx['avg_tech_investment']:.1f}%
- **Technology Leaders:** {', '.join(comp_ctx['tech_leaders'][:3]) if comp_ctx['tech_leaders'] else 'None identified'}
- **Market Pressure Score:** {comp_ctx['market_pressure']:.1f}%
"""
    
    document_content += f"""

---

## IMPLEMENTATION PLAN

### Resource Requirements
- **FTE Required:** {case_data.get('FTE_Required', 0)}
- **External Vendor:** {case_data.get('External_Vendor_Required', 'TBD')}
- **Technology Investment:** {case_data.get('Technology_Investment_Percent', 0)}%
- **Change Management Effort:** {case_data.get('Change_Management_Effort', 'TBD')}

### Risk Assessment
- **Technology Complexity Score:** {case_data.get('Technology_Complexity_Score', 5)}/10
- **Implementation Risk Score:** {case_data.get('Implementation_Risk_Score', 5)}/10

---

## RECOMMENDATIONS

Based on the analysis, this business case scores **{score_data[0]:.2f}/10**.

"""
    
    if score_data[0] >= 8.0:
        document_content += "**RECOMMENDATION: APPROVE FOR IMMEDIATE IMPLEMENTATION**\n"
        document_content += "This case demonstrates exceptional value and should be prioritized for the current planning cycle.\n"
    elif score_data[0] >= 6.0:
        document_content += "**RECOMMENDATION: CONSIDER FOR NEXT CYCLE**\n"
        document_content += "This case shows good potential and should be considered for the next planning cycle with minor improvements.\n"
    elif score_data[0] >= 4.0:
        document_content += "**RECOMMENDATION: REVISE AND RESUBMIT**\n"
        document_content += "This case requires significant improvements before it can be recommended for implementation.\n"
    else:
        document_content += "**RECOMMENDATION: REJECT**\n"
        document_content += "This case does not meet the minimum criteria for implementation at this time.\n"
    
    document_content += f"""

---

**Document Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Generated By:** Iluvalcar 2.0 Business Case Development System
"""
    
    return document_content

def get_score_category(score):
    """Get score category description."""
    if score >= 8.0:
        return "Excellent"
    elif score >= 6.0:
        return "Good"
    elif score >= 4.0:
        return "Fair"
    else:
        return "Poor"

def move_to_parking_lot(case_data, score, threshold=6.0):
    """Move qualifying business cases to parking lot."""
    if score >= threshold:
        parking_item = {
            'case_id': case_data.get('Case_ID'),
            'title': case_data.get('Case_Title'),
            'score': score,
            'investment': case_data.get('Estimated_Investment_USD'),
            'roi': case_data.get('ROI_Percentage'),
            'priority': case_data.get('Priority_Level'),
            'region': case_data.get('Region'),
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'status': 'Parking Lot'
        }
        
        if parking_item not in st.session_state.parking_lot:
            st.session_state.parking_lot.append(parking_item)
        
        return True
    return False

def promote_to_backlog(parking_item):
    """Promote item from parking lot to backlog."""
    backlog_item = parking_item.copy()
    backlog_item['status'] = 'Backlog'
    backlog_item['date_promoted'] = datetime.now().strftime('%Y-%m-%d')
    
    if backlog_item not in st.session_state.backlog:
        st.session_state.backlog.append(backlog_item)
    
    # Remove from parking lot
    if parking_item in st.session_state.parking_lot:
        st.session_state.parking_lot.remove(parking_item)

def add_to_roadmap(backlog_item, quarter, year):
    """Add item from backlog to roadmap."""
    roadmap_item = backlog_item.copy()
    roadmap_item['status'] = 'Roadmap'
    roadmap_item['planned_quarter'] = quarter
    roadmap_item['planned_year'] = year
    roadmap_item['date_scheduled'] = datetime.now().strftime('%Y-%m-%d')
    
    if roadmap_item not in st.session_state.roadmap:
        st.session_state.roadmap.append(roadmap_item)
    
    # Remove from backlog
    if backlog_item in st.session_state.backlog:
        st.session_state.backlog.remove(backlog_item)

def get_category_color(category):
    """Return color for each workstream category"""
    color_map = {
        'NAV Calculation': '#FF6B6B',
        'Portfolio Valuation': '#4ECDC4', 
        'Trade Capture': '#45B7D1',
        'Reconciliation': '#96CEB4',
        'Corporate Actions': '#FFEAA7',
        'Expense Management': '#DDA0DD',
        'Reporting': '#98D8C8'
    }
    return color_map.get(category, '#B0B0B0')

def create_workstream_matrix_view():
    """Create a strategic matrix view of workstreams"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    fig = go.Figure()
    
    # Create bubble chart: Risk vs Automation with size = Investment
    for category in df['category'].unique():
        category_data = df[df['category'] == category]
        
        fig.add_trace(go.Scatter(
            x=category_data['automation'],
            y=category_data['risk'],
            mode='markers+text',
            marker=dict(
                size=category_data['investment'] * 12,
                color=get_category_color(category),
                line=dict(width=2, color='white'),
                opacity=0.7
            ),
            text=[f"<b>{name[:12]}{'...' if len(name) > 12 else ''}</b>" for name in category_data['name']],
            textposition="middle center",
            textfont=dict(size=9, color='white'),
            name=category,
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Automation: %{x}/10<br>' +
                         'Risk: %{y}/10<br>' +
                         'Investment: $%{customdata[1]:.1f}M<br>' +
                         'Completion: %{customdata[2]}%<br>' +
                         'Priority: %{customdata[3]}<br>' +
                         '<extra></extra>',
            customdata=list(zip(category_data['name'], category_data['investment'], 
                               category_data['completion'], category_data['priority']))
        ))
    
    # Add quadrant lines
    fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=2.5, y=8.5, text="<b>High Risk<br>Low Auto</b><br>🚨 Critical", 
                      showarrow=False, bgcolor="rgba(255,0,0,0.1)", bordercolor="red")
    fig.add_annotation(x=7.5, y=8.5, text="<b>High Risk<br>High Auto</b><br>⚡ Monitor", 
                      showarrow=False, bgcolor="rgba(255,165,0,0.1)", bordercolor="orange")
    fig.add_annotation(x=2.5, y=2.5, text="<b>Low Risk<br>Low Auto</b><br>🔧 Enhance", 
                      showarrow=False, bgcolor="rgba(255,255,0,0.1)", bordercolor="gold")
    fig.add_annotation(x=7.5, y=2.5, text="<b>Low Risk<br>High Auto</b><br>✅ Stable", 
                      showarrow=False, bgcolor="rgba(0,255,0,0.1)", bordercolor="green")
    
    fig.update_layout(
        title="Workstream Strategic Matrix - Risk vs Automation",
        xaxis_title="Automation Level (1-10)",
        yaxis_title="Risk Level (1-10)",
        width=900,
        height=600,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_workstream_timeline():
    """Create a timeline/roadmap view of workstreams"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Calculate estimated completion dates based on current completion
    current_date = pd.Timestamp.now()
    df['days_remaining'] = ((100 - df['completion']) * 2)  # Rough estimate: 2 days per %
    df['target_date'] = current_date + pd.to_timedelta(df['days_remaining'], unit='D')
    
    fig = go.Figure()
    
    # Sort by target date
    df_sorted = df.sort_values('target_date')
    
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        # Progress bar for each workstream
        fig.add_trace(go.Scatter(
            x=[current_date, row['target_date']],
            y=[i, i],
            mode='lines',
            line=dict(color='lightgray', width=20),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Completed portion
        completed_date = current_date + pd.Timedelta(days=int(row['days_remaining'] * (row['completion']/100)))
        fig.add_trace(go.Scatter(
            x=[current_date, completed_date],
            y=[i, i],
            mode='lines',
            line=dict(color=get_category_color(row['category']), width=20),
            showlegend=False,
            hovertemplate=f"<b>{row['name']}</b><br>" +
                         f"Category: {row['category']}<br>" +
                         f"Completion: {row['completion']}%<br>" +
                         f"Investment: ${row['investment']:.1f}M<br>" +
                         f"Priority: {row['priority']}<br>" +
                         f"Target: {row['target_date'].strftime('%Y-%m-%d')}<extra></extra>"
        ))
        
        # Priority indicator
        priority_color = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}[row['priority']]
        fig.add_trace(go.Scatter(
            x=[row['target_date']],
            y=[i],
            mode='markers',
            marker=dict(
                size=15,
                color=priority_color,
                symbol='diamond',
                line=dict(width=2, color='white')
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title="Workstream Completion Timeline & Roadmap",
        xaxis_title="Timeline",
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(len(df_sorted))),
            ticktext=[f"{name[:25]}{'...' if len(name) > 25 else ''}" for name in df_sorted['name']],
            tickfont=dict(size=10)
        ),
        width=1000,
        height=max(400, len(df_sorted) * 40),
        margin=dict(l=200, r=50, t=80, b=80)
    )
    
    return fig

def create_workstream_hierarchy():
    """Create a hierarchical/tree view of workstreams by category"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    fig = go.Figure()
    
    # Create sunburst chart
    categories = []
    workstreams = []
    parents = []
    values = []
    colors = []
    
    # Add categories
    for category in df['category'].unique():
        categories.append(category)
        parents.append("")
        values.append(df[df['category'] == category]['investment'].sum())
        colors.append(get_category_color(category))
    
    # Add workstreams
    for _, row in df.iterrows():
        workstreams.append(f"{row['name'][:20]}{'...' if len(row['name']) > 20 else ''}")
        parents.append(row['category'])
        values.append(row['investment'])
        colors.append(get_category_color(row['category']))
    
    all_labels = categories + workstreams
    all_parents = parents
    all_values = values
    
    fig = go.Figure(go.Sunburst(
        labels=all_labels,
        parents=all_parents,
        values=all_values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Investment: $%{value:.1f}M<br><extra></extra>',
        maxdepth=2,
    ))
    
    fig.update_layout(
        title="Workstream Hierarchy - Investment Distribution",
        width=700,
        height=700
    )
    
    return fig

def create_workstream_dashboard():
    """Create a comprehensive dashboard view"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Investment by Category', 'Completion Progress', 'Risk vs Complexity', 'Priority Distribution'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # 1. Investment by Category (Bar Chart)
    category_investment = df.groupby('category')['investment'].sum().sort_values(ascending=True)
    fig.add_trace(
        go.Bar(x=category_investment.values, y=category_investment.index, orientation='h',
               marker_color=[get_category_color(cat) for cat in category_investment.index],
               name="Investment"),
        row=1, col=1
    )
    
    # 2. Completion Progress (Bar Chart)
    completion_avg = df.groupby('category')['completion'].mean().sort_values(ascending=True)
    fig.add_trace(
        go.Bar(x=completion_avg.values, y=completion_avg.index, orientation='h',
               marker_color=[get_category_color(cat) for cat in completion_avg.index],
               name="Completion"),
        row=1, col=2
    )
    
    # 3. Risk vs Complexity Scatter
    fig.add_trace(
        go.Scatter(x=df['complexity'], y=df['risk'],
                   mode='markers',
                   marker=dict(
                       size=df['investment']*8,
                       color=[get_category_color(cat) for cat in df['category']],
                       opacity=0.7,
                       line=dict(width=1, color='white')
                   ),
                   text=df['name'],
                   name="Workstreams"),
        row=2, col=1
    )
    
    # 4. Priority Distribution (Pie Chart)
    priority_counts = df['priority'].value_counts()
    priority_colors = {'High': '#FF4444', 'Medium': '#FFA500', 'Low': '#44AA44'}
    fig.add_trace(
        go.Pie(labels=priority_counts.index, values=priority_counts.values,
               marker_colors=[priority_colors[p] for p in priority_counts.index],
               name="Priority"),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text="Workstream Analytics Dashboard",
        showlegend=False,
        height=800,
        width=1200
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Investment ($M)", row=1, col=1)
    fig.update_xaxes(title_text="Completion (%)", row=1, col=2)
    fig.update_xaxes(title_text="Complexity", row=2, col=1)
    fig.update_yaxes(title_text="Risk", row=2, col=1)
    
    return fig

def create_legend_info():
    """Create legend information as a separate component"""
    return """
    ### 📖 Legend & Guide:
    
    **Priority Levels:**
    - 🔴 **High Priority**: Critical workstreams requiring immediate attention
    - 🟡 **Medium Priority**: Important workstreams with moderate urgency  
    - 🟢 **Low Priority**: Stable workstreams with lower risk/complexity
    
    **Element Information:**
    - **Position**: X-axis shows complexity level (1-10), Y-axis shows category
    - **Size**: Marker size represents investment amount (larger = more investment)
    - **Color**: Each category has a distinct color for easy identification
    - **Hover**: Hover over any element for detailed information
    
    **Categories:**
    """

def create_3d_complexity_automation_risk():
    """Enhanced 3D: Complexity vs Automation vs Risk"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    fig = go.Figure()
    
    # Add workstreams by priority level
    for priority in ['High', 'Medium', 'Low']:
        priority_data = df[df['priority'] == priority]
        if len(priority_data) > 0:
            priority_colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}
            priority_symbols = {'High': 'diamond', 'Medium': 'circle', 'Low': 'square'}
            
            fig.add_trace(go.Scatter3d(
                x=priority_data['complexity'],
                y=priority_data['automation'],
                z=priority_data['risk'],
                mode='markers+text',
                marker=dict(
                    size=priority_data['investment'] * 4,
                    color=priority_colors[priority],
                    symbol=priority_symbols[priority],
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                text=[name[:10] + '...' if len(name) > 10 else name for name in priority_data['name']],
                textposition="top center",
                name=f"{priority} Priority",
                hovertemplate='<b>%{customdata[0]}</b><br>' +
                             'Complexity: %{x}/10<br>' +
                             'Automation: %{y}/10<br>' +
                             'Risk: %{z}/10<br>' +
                             'Investment: $%{customdata[1]:.1f}M<br>' +
                             'Completion: %{customdata[2]}%<br>' +
                             'Category: %{customdata[3]}<br>' +
                             '<extra></extra>',
                customdata=list(zip(priority_data['name'], priority_data['investment'], 
                                  priority_data['completion'], priority_data['category']))
            ))
    
    # Add reference planes
    x_range = [1, 10]
    y_range = [1, 10]
    z_range = [1, 10]
    
    # Risk threshold plane (z=7)
    fig.add_trace(go.Mesh3d(
        x=[1, 10, 10, 1, 1, 10, 10, 1],
        y=[1, 1, 10, 10, 1, 1, 10, 10],
        z=[7, 7, 7, 7, 7, 7, 7, 7],
        opacity=0.15,
        color='red',
        name='High Risk Threshold',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title="3D Strategic Analysis: Complexity × Automation × Risk",
        scene=dict(
            xaxis_title="Complexity Level →",
            yaxis_title="Automation Level →", 
            zaxis_title="Risk Level →",
            xaxis=dict(range=[0, 11]),
            yaxis=dict(range=[0, 11]),
            zaxis=dict(range=[0, 11]),
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.2)
            ),
            annotations=[
                dict(x=9, y=9, z=2, text="✅ Optimal Zone", showarrow=False, 
                     bgcolor="rgba(0,255,0,0.2)", bordercolor="green"),
                dict(x=2, y=2, z=9, text="🚨 Critical Zone", showarrow=False,
                     bgcolor="rgba(255,0,0,0.2)", bordercolor="red")
            ]
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_pl_profitability_analysis():
    """3D P&L Analysis: Revenue vs Costs vs AUM with Profitability Insights"""
    # Check if P&L data is available
    if st.session_state.pl_data.empty:
        return None
    
    # Calculate P&L metrics
    pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
    if pl_analysis.empty:
        return None
    
    fig = go.Figure()
    
    # Create traces by service line dominance
    service_lines = ['Fund_Accounting', 'Fund_Administration', 'Transfer_Agency', 'Regulatory_Reporting']
    service_colors = {'Fund_Accounting': '#FF6B6B', 'Fund_Administration': '#4ECDC4', 
                     'Transfer_Agency': '#45B7D1', 'Regulatory_Reporting': '#96CEB4'}
    
    # Check if we have valid data
    if len(pl_analysis) == 0:
        return None
    
    # Determine dominant service line for each client
    for _, row in pl_analysis.iterrows():
        revenues = [row['Fund_Accounting_Revenue_USD'], row['Fund_Administration_Revenue_USD'],
                   row['Transfer_Agency_Revenue_USD'], row['Regulatory_Reporting_Revenue_USD']]
        dominant_service = service_lines[revenues.index(max(revenues))]
        
        fig.add_trace(go.Scatter3d(
            x=[row['Total_Annual_Revenue_USD']],
            y=[row['Total_Costs']],
            z=[row['Fund_AUM_USD_Millions']],
            mode='markers+text',
            marker=dict(
                size=max(5, min(30, abs(row['Gross_Margin_Percent']) * 0.8 + 5)),  # Size by profitability, clamped between 5-30
                color=service_colors.get(dominant_service, '#B0B0B0'),
                opacity=0.8,
                line=dict(width=2, color='white'),
                symbol='diamond' if row['Gross_Margin_Percent'] > 25 else 'circle'
            ),
            text=[row['Client_Name'][:8] + '...' if len(row['Client_Name']) > 8 else row['Client_Name']],
            textposition="top center",
            name=f"{dominant_service.replace('_', ' ')} Focused",
            showlegend=True,
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Revenue: $%{x:,.0f}<br>' +
                         'Costs: $%{y:,.0f}<br>' +
                         'AUM: $%{z:,.0f}M<br>' +
                         'Gross Margin: %{customdata[1]:.1f}%<br>' +
                         'Revenue per AUM: %{customdata[2]:.1f} bps<br>' +
                         'Dominant Service: %{customdata[3]}<br>' +
                         '<extra></extra>',
            customdata=[[row['Client_Name'], row['Gross_Margin_Percent'], 
                        row['Revenue_Per_AUM_BPS'], dominant_service.replace('_', ' ')]]
        ))
    
    # Add profitability planes
    revenue_range = [pl_analysis['Total_Annual_Revenue_USD'].min(), pl_analysis['Total_Annual_Revenue_USD'].max()]
    cost_range = [pl_analysis['Total_Costs'].min(), pl_analysis['Total_Costs'].max()]
    aum_range = [pl_analysis['Fund_AUM_USD_Millions'].min(), pl_analysis['Fund_AUM_USD_Millions'].max()]
    
    # Break-even plane (Revenue = Costs)
    fig.add_trace(go.Mesh3d(
        x=[revenue_range[0], revenue_range[1], revenue_range[1], revenue_range[0]],
        y=[revenue_range[0], revenue_range[1], revenue_range[1], revenue_range[0]],
        z=[aum_range[0], aum_range[0], aum_range[1], aum_range[1]],
        opacity=0.15,
        color='red',
        name='Break-Even Plane',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title="3D P&L Analysis: Revenue × Costs × AUM",
        scene=dict(
            xaxis_title="Total Annual Revenue (USD) →",
            yaxis_title="Total Costs (USD) →",
            zaxis_title="Fund AUM (USD Millions) →",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            annotations=[
                dict(x=revenue_range[1]*0.8, y=cost_range[0]*1.2, z=aum_range[1]*0.8, 
                     text="💰 High Profit Zone", showarrow=False, 
                     bgcolor="rgba(0,255,0,0.2)", bordercolor="green"),
                dict(x=revenue_range[0]*1.2, y=cost_range[1]*0.8, z=aum_range[0]*1.2,
                     text="⚠️ Loss Zone", showarrow=False,
                     bgcolor="rgba(255,0,0,0.2)", bordercolor="red")
            ]
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_service_line_analysis():
    """3D Service Line Analysis: Service Mix vs Profitability vs Efficiency"""
    if st.session_state.pl_data.empty:
        return None
    
    pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
    if pl_analysis.empty:
        return None
    
    fig = go.Figure()
    
    # Calculate service line diversity index (Shannon entropy)
    for idx, row in pl_analysis.iterrows():
        revenues = [row['Fund_Accounting_Revenue_USD'], row['Fund_Administration_Revenue_USD'],
                   row['Transfer_Agency_Revenue_USD'], row['Regulatory_Reporting_Revenue_USD']]
        total_rev = sum(revenues)
        if total_rev > 0:
            proportions = [r/total_rev for r in revenues if r > 0]
            diversity_index = -sum([p * np.log(p) for p in proportions if p > 0])
        else:
            diversity_index = 0
        
        pl_analysis.loc[idx, 'Service_Diversity_Index'] = diversity_index
    
    # Create scatter plot
    fig.add_trace(go.Scatter3d(
        x=pl_analysis['Service_Diversity_Index'],
        y=pl_analysis['Gross_Margin_Percent'],
        z=pl_analysis['Revenue_Per_AUM_BPS'],
        mode='markers+text',
        marker=dict(
            size=np.clip(pl_analysis['Total_Annual_Revenue_USD'] / 20000, 5, 30),  # Size by revenue, clamped between 5-30
            color=pl_analysis['Number_of_Funds'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Number of Funds"),
            opacity=0.8,
            line=dict(width=2, color='white')
        ),
        text=[name[:6] + '...' if len(name) > 6 else name for name in pl_analysis['Client_Name']],
        textposition="middle center",
        name="Clients",
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                     'Service Diversity: %{x:.2f}<br>' +
                     'Gross Margin: %{y:.1f}%<br>' +
                     'Revenue per AUM: %{z:.1f} bps<br>' +
                     'Number of Funds: %{customdata[1]}<br>' +
                     'Total Revenue: $%{customdata[2]:,.0f}<br>' +
                     '<extra></extra>',
        customdata=list(zip(pl_analysis['Client_Name'], pl_analysis['Number_of_Funds'], 
                           pl_analysis['Total_Annual_Revenue_USD']))
    ))
    
    fig.update_layout(
        title="3D Service Line Analysis: Diversity × Profitability × Efficiency",
        scene=dict(
            xaxis_title="Service Line Diversity Index →",
            yaxis_title="Gross Margin (%) →",
            zaxis_title="Revenue per AUM (bps) →",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_cost_efficiency_analysis():
    """3D Cost Analysis: Labor vs Technology vs Overhead Efficiency"""
    if st.session_state.pl_data.empty:
        return None
    
    pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
    if pl_analysis.empty:
        return None
    
    fig = go.Figure()
    
    # Calculate efficiency ratios with safe division
    pl_analysis['Labor_Efficiency'] = np.where(
        pl_analysis['Total_Direct_Labor_Cost'] > 0, 
        pl_analysis['Total_Annual_Revenue_USD'] / pl_analysis['Total_Direct_Labor_Cost'],
        0
    )
    pl_analysis['Tech_Efficiency'] = np.where(
        pl_analysis['Total_Technology_Cost'] > 0,
        pl_analysis['Total_Annual_Revenue_USD'] / pl_analysis['Total_Technology_Cost'],
        0
    )
    pl_analysis['Overhead_Ratio'] = np.where(
        pl_analysis['Total_Annual_Revenue_USD'] > 0,
        pl_analysis['Overhead_Allocation'] / pl_analysis['Total_Annual_Revenue_USD'],
        0
    )
    
    # Create traces by profitability quartiles (with fallback for small datasets)
    try:
        quartiles = pd.qcut(pl_analysis['Gross_Margin_Percent'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
    except ValueError:
        # Fallback for small datasets - use simple binning
        quartiles = pd.cut(pl_analysis['Gross_Margin_Percent'], bins=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
    colors = {'Low': 'red', 'Medium-Low': 'orange', 'Medium-High': 'lightgreen', 'High': 'darkgreen'}
    
    for quartile in ['Low', 'Medium-Low', 'Medium-High', 'High']:
        quartile_data = pl_analysis[quartiles == quartile]
        
        if not quartile_data.empty:
            fig.add_trace(go.Scatter3d(
                x=quartile_data['Labor_Efficiency'],
                y=quartile_data['Tech_Efficiency'],
                z=quartile_data['Overhead_Ratio'] * 100,  # Convert to percentage
                mode='markers+text',
                marker=dict(
                    size=np.clip(quartile_data['Fund_AUM_USD_Millions'] / 100, 5, 30),  # Size by AUM, clamped between 5-30
                    color=colors[quartile],
                    opacity=0.8,
                    line=dict(width=2, color='white'),
                    symbol='diamond' if quartile == 'High' else 'circle'
                ),
                text=[name[:5] + '...' if len(name) > 5 else name for name in quartile_data['Client_Name']],
                textposition="top center",
                name=f"{quartile} Profitability",
                hovertemplate='<b>%{customdata[0]}</b><br>' +
                             'Labor Efficiency: %{x:.2f}x<br>' +
                             'Tech Efficiency: %{y:.2f}x<br>' +
                             'Overhead Ratio: %{z:.1f}%<br>' +
                             'Gross Margin: %{customdata[1]:.1f}%<br>' +
                             'AUM: $%{customdata[2]:,.0f}M<br>' +
                             '<extra></extra>',
                customdata=list(zip(quartile_data['Client_Name'], quartile_data['Gross_Margin_Percent'],
                               quartile_data['Fund_AUM_USD_Millions']))
            ))
    
    fig.update_layout(
        title="3D Cost Efficiency Analysis: Labor × Technology × Overhead",
        scene=dict(
            xaxis_title="Labor Efficiency (Revenue/Labor Cost) →",
            yaxis_title="Technology Efficiency (Revenue/Tech Cost) →",
            zaxis_title="Overhead Ratio (%) →",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_investment_performance():
    """3D: Investment vs Performance vs Timeline"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Calculate performance score
    df['performance_score'] = (df['automation'] * 0.4 + (11-df['risk']) * 0.3 + df['completion']/10 * 0.3)
    
    # Calculate timeline (days to completion)
    df['timeline_days'] = (100 - df['completion']) * 2
    
    fig = go.Figure()
    
    # Create traces by category
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        
        fig.add_trace(go.Scatter3d(
            x=cat_data['investment'],
            y=cat_data['performance_score'],
            z=cat_data['timeline_days'],
            mode='markers+text',
            marker=dict(
                size=cat_data['completion']/3,  # Size by completion
                color=get_category_color(category),
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            text=[f"{name[:8]}..." if len(name) > 8 else name for name in cat_data['name']],
            textposition="middle center",
            name=category,
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Investment: $%{x:.1f}M<br>' +
                         'Performance Score: %{y:.2f}/10<br>' +
                         'Timeline: %{z:.0f} days<br>' +
                         'Completion: %{customdata[1]}%<br>' +
                         'Priority: %{customdata[2]}<br>' +
                         '<extra></extra>',
            customdata=list(zip(cat_data['name'], cat_data['completion'], cat_data['priority']))
        ))
    
    fig.update_layout(
        title="3D Investment Analysis: Investment × Performance × Timeline",
        scene=dict(
            xaxis_title="Investment Amount ($M) →",
            yaxis_title="Performance Score →",
            zaxis_title="Days to Completion →",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_roi_analysis():
    """3D: ROI Analysis with Risk and Completion"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Calculate estimated ROI based on automation gain and risk reduction
    df['roi_estimate'] = ((df['automation'] - 3) * 0.5 + (8 - df['risk']) * 0.3) * df['investment']
    df['roi_estimate'] = df['roi_estimate'].clip(lower=-5, upper=20)  # Reasonable bounds
    
    fig = go.Figure()
    
    # Create surface plot for ROI landscape
    try:
        investment_range = np.linspace(df['investment'].min(), df['investment'].max(), 20)
        completion_range = np.linspace(df['completion'].min(), df['completion'].max(), 20)
        
        Investment, Completion = np.meshgrid(investment_range, completion_range)
        ROI_surface = Investment * (Completion/100) * 2  # Simplified ROI calculation for surface
        
        fig.add_trace(go.Surface(
            x=investment_range,
            y=completion_range,
            z=ROI_surface,
            opacity=0.3,
            colorscale='Viridis',
            showscale=False,
            name='ROI Landscape',
            hoverinfo='skip'
        ))
    except Exception as e:
        # Skip surface if there's an issue, just show scatter points
        pass
    
    # Add actual workstreams
    for priority in ['High', 'Medium', 'Low']:
        priority_data = df[df['priority'] == priority]
        if len(priority_data) > 0:
            priority_colors = {'High': 'red', 'Medium': 'orange', 'Low': 'lightgreen'}
            
            fig.add_trace(go.Scatter3d(
                x=priority_data['investment'],
                y=priority_data['completion'],
                z=priority_data['roi_estimate'],
                mode='markers+text',
                marker=dict(
                    size=15,
                    color=priority_colors[priority],
                    opacity=0.9,
                    line=dict(width=2, color='white'),
                    symbol='diamond' if priority == 'High' else 'circle'
                ),
                text=[name[:8] + '...' if len(name) > 8 else name for name in priority_data['name']],
                textposition="top center",
                name=f"{priority} Priority",
                hovertemplate='<b>%{customdata[0]}</b><br>' +
                             'Investment: $%{x:.1f}M<br>' +
                             'Completion: %{y}%<br>' +
                             'Est. ROI: $%{z:.1f}M<br>' +
                             'Risk: %{customdata[1]}/10<br>' +
                             'Automation: %{customdata[2]}/10<br>' +
                             '<extra></extra>',
                customdata=list(zip(priority_data['name'], priority_data['risk'], priority_data['automation']))
            ))
    
    fig.update_layout(
        title="3D ROI Analysis: Investment × Completion × Estimated ROI",
        scene=dict(
            xaxis_title="Investment Amount ($M) →",
            yaxis_title="Completion Percentage % →",
            zaxis_title="Estimated ROI ($M) →",
            camera=dict(eye=dict(x=1.2, y=1.2, z=1.5))
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_scenario_analysis():
    """3D: What-if Scenario Analysis"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    fig = go.Figure()
    
    # Current state
    fig.add_trace(go.Scatter3d(
        x=df['complexity'],
        y=df['completion'],
        z=df['risk'],
        mode='markers',
        marker=dict(
            size=12,
            color=[get_category_color(cat) for cat in df['category']],
            opacity=0.8,
            line=dict(width=2, color='white')
        ),
        name='Current State',
        text=df['name'],
        hovertemplate='<b>%{text}</b><br>' +
                     'Complexity: %{x}/10<br>' +
                     'Completion: %{y}%<br>' +
                     'Risk: %{z}/10<br>' +
                     '<extra></extra>'
    ))
    
    # Future state (optimistic scenario - more completion, less risk)
    df_future = df.copy()
    df_future['completion_future'] = np.minimum(100, df_future['completion'] + 30).astype(int)
    df_future['risk_future'] = np.maximum(1, df_future['risk'] - 2).astype(int)
    
    fig.add_trace(go.Scatter3d(
        x=df_future['complexity'],
        y=df_future['completion_future'],
        z=df_future['risk_future'],
        mode='markers',
        marker=dict(
            size=12,
            color=[get_category_color(cat) for cat in df_future['category']],
            opacity=0.5,
            symbol='diamond',
            line=dict(width=2, color='green')
        ),
        name='Optimistic Future',
        text=df_future['name'],
        hovertemplate='<b>%{text}</b> (Future)<br>' +
                     'Complexity: %{x}/10<br>' +
                     'Completion: %{y}%<br>' +
                     'Risk: %{z}/10<br>' +
                     '<extra></extra>'
    ))
    
    # Add trajectory lines
    for i in range(len(df)):
        fig.add_trace(go.Scatter3d(
            x=[df.iloc[i]['complexity'], df_future.iloc[i]['complexity']],
            y=[df.iloc[i]['completion'], df_future.iloc[i]['completion_future']],
            z=[df.iloc[i]['risk'], df_future.iloc[i]['risk_future']],
            mode='lines',
            line=dict(color='gray', width=3, dash='dot'),
            opacity=0.3,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title="3D Scenario Analysis: Current vs Future State Projections",
        scene=dict(
            xaxis_title="Complexity Level →",
            yaxis_title="Completion Percentage % →",
            zaxis_title="Risk Level →",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=900,
        height=700
    )
    
    return fig

def create_3d_network_analysis():
    """3D: Workstream Interdependency Network"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Create artificial dependencies based on categories and complexity
    fig = go.Figure()
    
    # Position nodes in 3D space
    positions = {}
    for i, (_, row) in enumerate(df.iterrows()):
        angle = i * (2 * np.pi / len(df))
        radius = row['complexity']
        x = radius * np.cos(angle)
        y = radius * np.sin(angle) 
        z = row['risk']
        positions[row['name']] = (x, y, z)
    
    # Add dependency connections (simplified - connect similar categories)
    for cat in df['category'].unique():
        cat_workstreams = df[df['category'] == cat]
        if len(cat_workstreams) > 1:
            for i in range(len(cat_workstreams) - 1):
                name1 = cat_workstreams.iloc[i]['name']
                name2 = cat_workstreams.iloc[i + 1]['name']
                
                x1, y1, z1 = positions[name1]
                x2, y2, z2 = positions[name2]
                
                fig.add_trace(go.Scatter3d(
                    x=[x1, x2],
                    y=[y1, y2],
                    z=[z1, z2],
                    mode='lines',
                    line=dict(color=get_category_color(cat), width=4),
                    opacity=0.5,
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    # Add workstream nodes
    for _, row in df.iterrows():
        x, y, z = positions[row['name']]
        
        fig.add_trace(go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode='markers+text',
            marker=dict(
                size=row['investment'] * 5,
                color=get_category_color(row['category']),
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            text=row['name'][:8] + '...' if len(row['name']) > 8 else row['name'],
            textposition="middle center",
            name=row['category'],
            showlegend=False,
            hovertemplate='<b>%{text}</b><br>' +
                         'Category: ' + row['category'] + '<br>' +
                         'Investment: $' + f"{row['investment']:.1f}" + 'M<br>' +
                         'Complexity: ' + f"{row['complexity']}" + '/10<br>' +
                         'Risk: ' + f"{row['risk']}" + '/10<br>' +
                         '<extra></extra>'
        ))
    
    fig.update_layout(
        title="3D Network Analysis: Workstream Interdependencies",
        scene=dict(
            xaxis_title="Network Position X",
            yaxis_title="Network Position Y",
            zaxis_title="Risk Level →",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2))
        ),
        width=900,
        height=700
    )
    
    return fig

def workstream_management_interface():
    """Create interface for managing workstreams"""
    st.subheader("🛠️ Manage Workstreams - Add/Edit/Delete/Load Data")
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add New", "✏️ Edit Existing", "🗑️ Delete", "📂 Load Data"])
    
    with tab1:
        st.markdown("### Add New Workstream")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Workstream Name", key="add_name")
            new_category = st.selectbox("Category", [
                'NAV Calculation', 'Portfolio Valuation', 'Trade Capture',
                'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting'
            ], key="add_category")
            new_complexity = st.slider("Complexity Level", 1, 10, 5, key="add_complexity")
            new_automation = st.slider("Automation Level", 1, 10, 5, key="add_automation")
            new_risk = st.slider("Risk Level", 1, 10, 5, key="add_risk")
        
        with col2:
            new_investment = st.number_input("Investment ($M)", 0.0, 50.0, 1.0, 0.1, key="add_investment")
            new_completion = st.slider("Completion %", 0, 100, 50, key="add_completion")
            new_priority = st.selectbox("Priority", ['High', 'Medium', 'Low'], key="add_priority")
            new_description = st.text_area("Description", key="add_description")
        
        if st.button("Add Workstream", type="primary", key="add_workstream_btn"):
            if new_name:
                new_id = f"custom_{len(st.session_state.workstream_data):03d}"
                new_workstream = {
                    'id': new_id,
                    'name': new_name,
                    'category': new_category,
                    'complexity': new_complexity,
                    'automation': new_automation,
                    'risk': new_risk,
                    'investment': new_investment,
                    'completion': new_completion,
                    'priority': new_priority,
                    'description': new_description
                }
                st.session_state.workstream_data.append(new_workstream)
                st.success(f"Added workstream: {new_name}")
                st.rerun()
            else:
                st.error("Please provide a workstream name")
    
    with tab2:
        st.markdown("### Edit Existing Workstream")
        
        df = pd.DataFrame(st.session_state.workstream_data)
        workstream_names = [f"{row['name']} ({row['category']})" for _, row in df.iterrows()]
        
        selected_workstream = st.selectbox("Select Workstream to Edit", workstream_names, key="edit_select_workstream")
        
        if selected_workstream:
            selected_idx = workstream_names.index(selected_workstream)
            workstream = st.session_state.workstream_data[selected_idx]
            
            col1, col2 = st.columns(2)
            
            with col1:
                edit_name = st.text_input("Name", value=workstream['name'], key="edit_name")
                edit_category = st.selectbox("Category", [
                    'NAV Calculation', 'Portfolio Valuation', 'Trade Capture',
                    'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting'
                ], index=['NAV Calculation', 'Portfolio Valuation', 'Trade Capture',
                         'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting'].index(workstream['category']), key="edit_category")
                edit_complexity = st.slider("Complexity", 1, 10, workstream['complexity'], key="edit_complexity")
                edit_automation = st.slider("Automation", 1, 10, workstream['automation'], key="edit_automation")
                edit_risk = st.slider("Risk", 1, 10, workstream['risk'], key="edit_risk")
            
            with col2:
                edit_investment = st.number_input("Investment ($M)", 0.0, 50.0, workstream['investment'], 0.1, key="edit_investment")
                edit_completion = st.slider("Completion %", 0, 100, workstream['completion'], key="edit_completion")
                edit_priority = st.selectbox("Priority", ['High', 'Medium', 'Low'], 
                                           index=['High', 'Medium', 'Low'].index(workstream['priority']), key="edit_priority")
                edit_description = st.text_area("Description", value=workstream['description'], key="edit_description")
            
            if st.button("Update Workstream", type="primary", key="update_workstream_btn"):
                st.session_state.workstream_data[selected_idx].update({
                    'name': edit_name,
                    'category': edit_category,
                    'complexity': edit_complexity,
                    'automation': edit_automation,
                    'risk': edit_risk,
                    'investment': edit_investment,
                    'completion': edit_completion,
                    'priority': edit_priority,
                    'description': edit_description
                })
                st.success("Workstream updated successfully!")
                st.rerun()
    
    with tab3:
        st.markdown("### Delete Workstream")
        
        df = pd.DataFrame(st.session_state.workstream_data)
        workstream_names = [f"{row['name']} ({row['category']})" for _, row in df.iterrows()]
        
        delete_workstream = st.selectbox("Select Workstream to Delete", workstream_names, key="delete_select_workstream")
        
        if delete_workstream:
            selected_idx = workstream_names.index(delete_workstream)
            workstream = st.session_state.workstream_data[selected_idx]
            
            st.warning(f"Are you sure you want to delete: **{workstream['name']}**?")
            st.info(f"Category: {workstream['category']} | Investment: ${workstream['investment']}M")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Confirm Delete", type="secondary", key="confirm_delete_btn"):
                    del st.session_state.workstream_data[selected_idx]
                    st.success(f"Deleted workstream: {workstream['name']}")
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", key="cancel_delete_btn"):
                    st.info("Delete cancelled")
    
    with tab4:
        st.markdown("### 📂 Load Workstream Data from Excel")
        
        # Show current data format
        st.markdown("#### 📋 Required Excel Format")
        st.info("Your Excel file must contain the following columns with these exact headers:")
        
        # Create sample data structure
        sample_data = pd.DataFrame([
            {
                'id': 'nav_001',
                'name': 'NAV Calculation & Publication',
                'category': 'NAV Calculation', 
                'complexity': 8,
                'automation': 7,
                'risk': 8,
                'investment': 4.2,
                'completion': 80,
                'priority': 'High',
                'description': 'Core NAV calculation engine and publication workflow'
            },
            {
                'id': 'val_001',
                'name': 'Exchange Listed Securities',
                'category': 'Portfolio Valuation',
                'complexity': 5,
                'automation': 8,
                'risk': 3,
                'investment': 1.5,
                'completion': 90,
                'priority': 'Low',
                'description': 'Automated valuation of exchange-traded securities'
            }
        ])
        
        st.dataframe(sample_data, use_container_width=True)
        
        # Column definitions
        st.markdown("#### 📖 Column Definitions")
        
        col_def1, col_def2 = st.columns(2)
        
        with col_def1:
            st.markdown("""
            **Required Columns:**
            - **id**: Unique identifier (text, e.g., 'nav_001')
            - **name**: Workstream name (text, max 50 characters)
            - **category**: Must be one of:
              - NAV Calculation
              - Portfolio Valuation
              - Trade Capture
              - Reconciliation
              - Corporate Actions
              - Expense Management
              - Reporting
            - **complexity**: Integer from 1-10
            - **automation**: Integer from 1-10
            """)
        
        with col_def2:
            st.markdown("""
            **Required Columns (continued):**
            - **risk**: Integer from 1-10
            - **investment**: Decimal number (in millions, e.g., 4.2)
            - **completion**: Integer from 0-100 (percentage)
            - **priority**: Must be one of:
              - High
              - Medium  
              - Low
            - **description**: Text description (max 200 characters)
            """)
        
        # Download template with comprehensive examples
        st.markdown("#### 📥 Download Enhanced Workstream Template")
        
        # Create comprehensive template with 5 realistic examples
        template_data = pd.DataFrame([
            {
                'id': 'WS_001',
                'name': 'AI-Enhanced NAV Calculation Platform',
                'category': 'NAV Calculation',
                'complexity': 8,
                'automation': 9,
                'risk': 4,
                'investment': 4.2,
                'completion': 75,
                'priority': 'High',
                'description': 'Implement AI/ML algorithms for enhanced NAV calculation accuracy, real-time processing, and automated validation with 99.9% accuracy target'
            },
            {
                'id': 'WS_002', 
                'name': 'Real-Time Trade Settlement System',
                'category': 'Trade Capture',
                'complexity': 7,
                'automation': 8,
                'risk': 5,
                'investment': 3.1,
                'completion': 60,
                'priority': 'High',
                'description': 'Deploy T+0 settlement capability with blockchain integration for instant trade confirmation and reduced counterparty risk'
            },
            {
                'id': 'WS_003',
                'name': 'Automated Reconciliation Engine',
                'category': 'Reconciliation', 
                'complexity': 6,
                'automation': 9,
                'risk': 3,
                'investment': 2.8,
                'completion': 85,
                'priority': 'Medium',
                'description': 'Exception-based automated reconciliation system reducing manual intervention by 90% with intelligent break resolution'
            },
            {
                'id': 'WS_004',
                'name': 'Digital Client Reporting Portal',
                'category': 'Reporting',
                'complexity': 5,
                'automation': 8,
                'risk': 3,
                'investment': 2.0,
                'completion': 90,
                'priority': 'Medium',
                'description': 'Self-service client portal with real-time reporting, custom dashboards, and mobile access for enhanced client experience'
            },
            {
                'id': 'WS_005',
                'name': 'Blockchain Custody Integration',
                'category': 'Portfolio Valuation',
                'complexity': 9,
                'automation': 6,
                'risk': 7,
                'investment': 5.5,
                'completion': 40,
                'priority': 'High',
                'description': 'Integration of blockchain technology for secure digital asset custody, smart contract execution, and immutable audit trails'
            }
        ])
        
        # Create enhanced Excel file with multiple sheets
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            # Main template sheet
            template_data.to_excel(writer, sheet_name='Workstream_Examples', index=False)
            
            # Instructions sheet
            instructions = pd.DataFrame({
                'Field': ['id', 'name', 'category', 'complexity', 'automation', 'risk', 'investment', 'completion', 'priority', 'description'],
                'Description': [
                    'Unique workstream identifier (e.g., WS_001)',
                    'Descriptive name of the workstream/project',
                    'Category: NAV Calculation, Portfolio Valuation, Trade Capture, Reconciliation, Corporate Actions, Expense Management, Reporting',
                    'Technical complexity (1-10): 1=Simple, 10=Highly Complex',
                    'Automation level (1-10): 1=Manual, 10=Fully Automated',
                    'Risk level (1-10): 1=Low Risk, 10=High Risk',
                    'Investment required in millions USD (e.g., 2.5 = $2.5M)',
                    'Current completion percentage (0-100%)',
                    'Priority: High, Medium, Low',
                    'Detailed description of objectives and scope'
                ],
                'Valid_Values': [
                    'Text (unique)',
                    'Text (descriptive)',
                    'NAV Calculation | Portfolio Valuation | Trade Capture | Reconciliation | Corporate Actions | Expense Management | Reporting',
                    '1-10 (integer)',
                    '1-10 (integer)',
                    '1-10 (integer)', 
                    'Number (decimal, e.g., 2.5)',
                    '0-100 (integer)',
                    'High | Medium | Low',
                    'Text (detailed description)'
                ]
            })
            instructions.to_excel(writer, sheet_name='Field_Instructions', index=False)
            
            # Scoring guide
            scoring_guide = pd.DataFrame({
                'Metric': ['Complexity Score', 'Automation Score', 'Risk Score', 'Investment Impact', 'Completion Status'],
                'Scale': ['1-10', '1-10', '1-10', '$M', '0-100%'],
                'Low_End': ['Simple/Basic', 'Fully Manual', 'Minimal Risk', 'Under $1M', '0-25%'],
                'Mid_Range': ['Moderate', 'Semi-Automated', 'Moderate Risk', '$1M-$5M', '26-75%'],
                'High_End': ['Highly Complex', 'Fully Automated', 'High Risk', 'Over $5M', '76-100%'],
                'Best_Practice': [
                    'Start with 6-8 for new initiatives',
                    'Target 7+ for efficiency gains', 
                    'Keep under 6 for feasibility',
                    'Balance ROI with strategic value',
                    'Update regularly for accuracy'
                ]
            })
            scoring_guide.to_excel(writer, sheet_name='Scoring_Guide', index=False)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.download_button(
                label="📥 Download Enhanced Template",
                data=excel_buffer.getvalue(),
                file_name="Enhanced_Workstream_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_template"
            )
            
            st.info("💡 **Template includes:** 5 realistic examples, field instructions, and scoring guide across 3 Excel sheets")
        
        with col2:
            # Template preview
            st.markdown("**📊 Template Preview:**")
            
            # Show key metrics
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Sample Workstreams", len(template_data))
                st.metric("Total Investment", f"${template_data['investment'].sum():.1f}M")
            with col_b:
                st.metric("Avg Completion", f"{template_data['completion'].mean():.0f}%")
                high_priority = len(template_data[template_data['priority'] == 'High'])
                st.metric("High Priority", f"{high_priority}/{len(template_data)}")
            
            # Preview table
            preview_cols = ['name', 'category', 'investment', 'completion', 'priority']
            st.dataframe(template_data[preview_cols], use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # File upload
        st.markdown("#### 📤 Upload Your Excel File")
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="Upload an Excel file with workstream data using the format shown above",
            key="workstream_upload"
        )
        
        if uploaded_file is not None:
            try:
                # Read the Excel file
                df_uploaded = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File uploaded successfully! Found {len(df_uploaded)} rows.")
                
                # Display uploaded data preview
                st.markdown("#### 👀 Data Preview")
                st.dataframe(df_uploaded.head(), use_container_width=True)
                
                # Validate data format
                st.markdown("#### ✅ Data Validation")
                
                required_columns = ['id', 'name', 'category', 'complexity', 'automation', 'risk', 'investment', 'completion', 'priority', 'description']
                valid_categories = ['NAV Calculation', 'Portfolio Valuation', 'Trade Capture', 'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting']
                valid_priorities = ['High', 'Medium', 'Low']
                
                validation_errors = []
                
                # Check required columns
                missing_columns = [col for col in required_columns if col not in df_uploaded.columns]
                if missing_columns:
                    validation_errors.append(f"Missing columns: {', '.join(missing_columns)}")
                
                if not validation_errors:  # Only validate data if columns are present
                    # Validate data types and ranges
                    for index, row in df_uploaded.iterrows():
                        row_num = index + 2  # Excel row number (accounting for header)
                        
                        # Check category values
                        if row['category'] not in valid_categories:
                            validation_errors.append(f"Row {row_num}: Invalid category '{row['category']}'")
                        
                        # Check priority values
                        if row['priority'] not in valid_priorities:
                            validation_errors.append(f"Row {row_num}: Invalid priority '{row['priority']}'")
                        
                        # Check numeric ranges
                        try:
                            if not (1 <= int(row['complexity']) <= 10):
                                validation_errors.append(f"Row {row_num}: Complexity must be 1-10")
                            if not (1 <= int(row['automation']) <= 10):
                                validation_errors.append(f"Row {row_num}: Automation must be 1-10")
                            if not (1 <= int(row['risk']) <= 10):
                                validation_errors.append(f"Row {row_num}: Risk must be 1-10")
                            if not (0 <= int(row['completion']) <= 100):
                                validation_errors.append(f"Row {row_num}: Completion must be 0-100")
                            if not (0 <= float(row['investment']) <= 50):
                                validation_errors.append(f"Row {row_num}: Investment must be 0-50")
                        except (ValueError, TypeError):
                            validation_errors.append(f"Row {row_num}: Invalid numeric values")
                        
                        # Check for required text fields
                        if pd.isna(row['id']) or str(row['id']).strip() == '':
                            validation_errors.append(f"Row {row_num}: ID is required")
                        if pd.isna(row['name']) or str(row['name']).strip() == '':
                            validation_errors.append(f"Row {row_num}: Name is required")
                
                # Display validation results
                if validation_errors:
                    st.error("❌ Data validation failed!")
                    for error in validation_errors[:10]:  # Show first 10 errors
                        st.error(f"• {error}")
                    if len(validation_errors) > 10:
                        st.error(f"... and {len(validation_errors) - 10} more errors")
                else:
                    st.success("✅ All data validation checks passed!")
                    
                    # Load options
                    st.markdown("#### 🔄 Load Options")
                    
                    col_load1, col_load2 = st.columns(2)
                    
                    with col_load1:
                        load_option = st.radio(
                            "How would you like to load the data?",
                            ["Replace all existing data", "Add to existing data"],
                            key="load_option"
                        )
                    
                    with col_load2:
                        st.info(f"**Current data**: {len(st.session_state.workstream_data)} workstreams")
                        st.info(f"**Upload data**: {len(df_uploaded)} workstreams")
                        if load_option == "Replace all existing data":
                            st.warning(f"**Result**: {len(df_uploaded)} workstreams (replaces all)")
                        else:
                            st.success(f"**Result**: {len(st.session_state.workstream_data) + len(df_uploaded)} workstreams (adds to existing)")
                    
                    # Confirmation and load button
                    st.markdown("---")
                    if st.button(f"🚀 Confirm and Load Data", type="primary", key="confirm_load"):
                        try:
                            # Convert uploaded data to the required format
                            new_workstream_data = []
                            
                            for _, row in df_uploaded.iterrows():
                                workstream = {
                                    'id': str(row['id']),
                                    'name': str(row['name']),
                                    'category': str(row['category']),
                                    'complexity': int(row['complexity']),
                                    'automation': int(row['automation']),
                                    'risk': int(row['risk']),
                                    'investment': float(row['investment']),
                                    'completion': int(row['completion']),
                                    'priority': str(row['priority']),
                                    'description': str(row['description'])
                                }
                                new_workstream_data.append(workstream)
                            
                            # Update session state based on load option
                            if load_option == "Replace all existing data":
                                st.session_state.workstream_data = new_workstream_data
                                st.success(f"✅ Successfully replaced all data! Loaded {len(new_workstream_data)} workstreams.")
                            else:
                                # Add to existing data, avoiding duplicates by ID
                                existing_ids = {ws['id'] for ws in st.session_state.workstream_data}
                                added_count = 0
                                updated_count = 0
                                
                                for new_ws in new_workstream_data:
                                    if new_ws['id'] in existing_ids:
                                        # Update existing workstream
                                        for i, existing_ws in enumerate(st.session_state.workstream_data):
                                            if existing_ws['id'] == new_ws['id']:
                                                st.session_state.workstream_data[i] = new_ws
                                                updated_count += 1
                                                break
                                    else:
                                        # Add new workstream
                                        st.session_state.workstream_data.append(new_ws)
                                        added_count += 1
                                
                                st.success(f"✅ Successfully processed data! Added {added_count} new workstreams, updated {updated_count} existing workstreams.")
                            
                            # Refresh the app to show updated data
                            st.info("🔄 Page will refresh to show updated data...")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error loading data: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error reading Excel file: {str(e)}")
                st.error("Please make sure your file is a valid Excel file (.xlsx or .xls) with the correct format.")

# Initialize session state for capital projects comments
if 'cap_comment_variance' not in st.session_state:
    st.session_state.cap_comment_variance = ""
if 'cap_comment_impact' not in st.session_state:
    st.session_state.cap_comment_impact = ""
if 'cap_comment_bottom5' not in st.session_state:
    st.session_state.cap_comment_bottom5 = ""
if 'cap_reports_ready' not in st.session_state:
    st.session_state.cap_reports_ready = False

# Define current_year and current_month for capital projects
cap_current_year = datetime.now().year
cap_current_month = datetime.now().month
cap_current_year_str = str(cap_current_year)

# --- Capital Project Data Loading and Cleaning ---
@st.cache_data
def load_capital_project_data(uploaded_file: io.BytesIO) -> pd.DataFrame:
    """Loads and preprocesses capital project data from a CSV or Excel file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

    def clean_col_name(col_name: str) -> str:
        """Cleans a single column name."""
        col_name = str(col_name).strip().replace(' ', '_').replace('+', '_').replace('.', '_').replace('-', '_')
        col_name = '_'.join(filter(None, col_name.split('_')))
        col_name = col_name.upper()
        corrections = {
            'PROJEC_TID': 'PROJECT_ID', 'INI_MATIVE_PROGRAM': 'INITIATIVE_PROGRAM',
            'ALL_PRIOR_YEARS_A': 'ALL_PRIOR_YEARS_ACTUALS', 'C_URRENT_EAC': 'CURRENT_EAC',
            'QE_RUN_RATE': 'QE_RUN_RATE', 'RATE_1': 'RATE_SUPPLEMENTARY'
        }
        return corrections.get(col_name, col_name)

    df.columns = [clean_col_name(col) for col in df.columns]

    cols = []
    seen = {}
    for col in df.columns:
        original_col = col
        count = seen.get(col, 0)
        if count > 0:
            col = f"{col}_{count}"
        cols.append(col)
        seen[original_col] = count + 1
    df.columns = cols

    financial_pattern = r'^(20\d{2}_\d{2}_(A|F|CP)(_\d+)?|ALL_PRIOR_YEARS_ACTUALS|BUSINESS_ALLOCATION|CURRENT_EAC|QE_FORECAST_VS_QE_PLAN|FORECAST_VS_BA|YE_RUN|RATE|QE_RUN|RATE_SUPPLEMENTARY)$'
    financial_cols_to_convert = [col for col in df.columns if pd.Series([col]).str.contains(financial_pattern, regex=True).any()]

    for col in financial_cols_to_convert:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip().replace('', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    monthly_col_pattern = re.compile(rf'^{cap_current_year}_\d{{2}}_([AF]|CP)$')
    monthly_actuals_cols, monthly_forecasts_cols, monthly_plan_cols = [], [], []
    for col in df.columns:
        match = monthly_col_pattern.match(col)
        if match:
            col_type = match.group(1)
            if col_type == 'A': monthly_actuals_cols.append(col)
            elif col_type == 'F': monthly_forecasts_cols.append(col)
            elif col_type == 'CP': monthly_plan_cols.append(col)

    for col_list in [monthly_actuals_cols, monthly_forecasts_cols, monthly_plan_cols]:
        for col in col_list:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df[f'TOTAL_{cap_current_year}_ACTUALS'] = df[monthly_actuals_cols].sum(axis=1) if monthly_actuals_cols else 0
    df[f'TOTAL_{cap_current_year}_FORECASTS'] = df[monthly_forecasts_cols].sum(axis=1) if monthly_forecasts_cols else 0
    df[f'TOTAL_{cap_current_year}_CAPITAL_PLAN'] = df[monthly_plan_cols].sum(axis=1) if monthly_plan_cols else 0

    if 'ALL_PRIOR_YEARS_ACTUALS' in df.columns:
        df['TOTAL_ACTUALS_TO_DATE'] = df['ALL_PRIOR_YEARS_ACTUALS'] + df[f'TOTAL_{cap_current_year}_ACTUALS']
    else:
        df['TOTAL_ACTUALS_TO_DATE'] = df[f'TOTAL_{cap_current_year}_ACTUALS']

    ytd_actual_cols = [col for col in monthly_actuals_cols if int(col.split('_')[1]) <= cap_current_month]
    df['SUM_ACTUAL_SPEND_YTD'] = df[ytd_actual_cols].sum(axis=1) if ytd_actual_cols else 0
    df['SUM_OF_FORECASTED_NUMBERS'] = df[f'TOTAL_{cap_current_year}_FORECASTS']
    df['RUN_RATE_PER_MONTH'] = (df[f'TOTAL_{cap_current_year}_ACTUALS'] + df[f'TOTAL_{cap_current_year}_FORECASTS']) / 12

    if 'BUSINESS_ALLOCATION' in df.columns:
        df['CAPITAL_VARIANCE'] = df['BUSINESS_ALLOCATION'] - df[f'TOTAL_{cap_current_year}_FORECASTS']
        df['CAPITAL_UNDERSPEND'] = df['CAPITAL_VARIANCE'].apply(lambda x: x if x > 0 else 0)
        df['CAPITAL_OVERSPEND'] = df['CAPITAL_VARIANCE'].apply(lambda x: abs(x) if x < 0 else 0)
    else:
        df['CAPITAL_VARIANCE'], df['CAPITAL_UNDERSPEND'], df['CAPITAL_OVERSPEND'] = 0, 0, 0

    df['NET_REALLOCATION_AMOUNT'] = df['CAPITAL_UNDERSPEND'] - df['CAPITAL_OVERSPEND']
    
    num_actual_months = len(ytd_actual_cols) if ytd_actual_cols else 1
    num_forecast_months = len(monthly_forecasts_cols) if monthly_forecasts_cols else 1
    df['AVG_ACTUAL_SPEND'] = df['SUM_ACTUAL_SPEND_YTD'] / num_actual_months
    df['AVG_FORECAST_SPEND'] = df[f'TOTAL_{cap_current_year}_FORECASTS'] / num_forecast_months
    df['TOTAL_SPEND_VARIANCE'] = df[f'TOTAL_{cap_current_year}_ACTUALS'] - df[f'TOTAL_{cap_current_year}_FORECASTS']

    monthly_af_variance_cols = []
    for i in range(1, 13):
        actual_col, forecast_col = f'{cap_current_year}_{i:02d}_A', f'{cap_current_year}_{i:02d}_F'
        if actual_col in df.columns and forecast_col in df.columns:
            variance_col_name = f'{cap_current_year}_{i:02d}_AF_VARIANCE'
            df[variance_col_name] = df[actual_col] - df[forecast_col]
            monthly_af_variance_cols.append(variance_col_name)

    df['AVERAGE_MONTHLY_SPREAD_SCORE'] = df[monthly_af_variance_cols].abs().mean(axis=1) if monthly_af_variance_cols else 0
    return df

# --- Capital Project Report Generation Functions ---
def generate_capital_html_report(metrics, figures, tables, comments, project_details_html=None):
    """Generates a comprehensive HTML report of the capital dashboard state."""
    monthly_trends_html = figures['monthly_trends'].to_html(full_html=False, include_plotlyjs='cdn') if figures.get('monthly_trends') else '<p>No monthly trend data available.</p>'
    
    def create_comment_block(title, comment_text):
        if comment_text and comment_text.strip():
            comment_text_html = comment_text.replace('\n', '<br>')
            return f"<h3>{title}</h3><p style='white-space: pre-wrap; background-color:#f0f2f6; padding: 10px; border-radius: 5px;'>{comment_text_html}</p>"
        return ""

    report_html = f"""
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Capital Project Report</title><style>
    body{{font-family:sans-serif;margin:20px;color:#333}}h1,h2,h3{{color:#004d40}}.metric-container{{display:flex;justify-content:space-around;flex-wrap:wrap;margin-bottom:20px}}
    .metric-box{{border:1px solid #ddd;border-radius:8px;padding:15px;margin:10px;flex:1;min-width:200px;text-align:center;background-color:#f9f9f9}}
    .metric-label{{font-size:0.9em;color:#555}}.metric-value{{font-size:1.5em;font-weight:bold;color:#222;margin-top:5px}}
    table{{width:100%;border-collapse:collapse;margin-top:20px}}th,td{{border:1px solid #ddd;padding:8px;text-align:left}}th{{background-color:#e6f2f0}}
    .chart-container{{margin-top:30px;page-break-inside:avoid;}}.section-title{{margin-top:40px;border-bottom:2px solid #004d40;padding-bottom:10px;page-break-after:avoid;}}
    footer{{text-align:center;margin-top:50px;padding-top:20px;border-top:1px solid #eee;font-size:0.8em;color:#777}}
    .flex-container{{display:flex;justify-content:space-between;gap:20px;page-break-inside:avoid;}}.flex-child{{flex:1;min-width:45%;}}
    </style></head><body>
    <h1>Capital Project Portfolio Report</h1><p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <h2 class="section-title">Key Metrics Overview</h2><div class="metric-container">
    {''.join([f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>' for label, value in metrics.items()])}
    </div>
    <h2 class="section-title">Filtered Project Details</h2>{tables['project_details']}
    <h2 class="section-title">{cap_current_year} Monthly Spend Trends</h2><div class="chart-container">{monthly_trends_html}</div>
    <h2 class="section-title">Project Spend Variance Analysis</h2>{create_comment_block('Analyst Comments', comments['variance'])}<div class="flex-container">
    <div class="flex-child"><h3>Total Spend</h3>{figures['total_spend'].to_html(full_html=False, include_plotlyjs='cdn') if figures['total_spend'] else '<p>N/A</p>'}</div>
    <div class="flex-child"><h3>Average Spend</h3>{figures['avg_spend'].to_html(full_html=False, include_plotlyjs='cdn') if figures['avg_spend'] else '<p>N/A</p>'}</div>
    </div>
    <h2 class="section-title">Budget Impact & Reallocation</h2>{create_comment_block('Analyst Comments', comments['impact'])}<div class="flex-container">
    <div class="flex-child"><h3>Largest Forecasted Overspend</h3>{tables['overspend']}</div>
    <div class="flex-child"><h3>Largest Potential Underspend</h3>{tables['underspend']}</div>
    </div>
    {project_details_html if project_details_html else ''}
    <h2 class="section-title">Project Performance</h2>{create_comment_block('Analyst Comments on Bottom 5 Projects', comments['bottom5'])}<div class="flex-container">
    <div class="flex-child"><h3>Top 5 Best Behaving</h3>{tables['top_5']}</div>
    <div class="flex-child"><h3>Bottom 5 Worst Behaving</h3>{tables['bottom_5']}</div>
    </div>
    <footer><p>Generated by Iluvalcar 2.0 - Capital Project Portfolio Dashboard</p></footer>
    </body></html>"""
    return report_html

def generate_capital_excel_report(metrics, tables, comments):
    """Generates a multi-sheet Excel report for capital projects."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        summary_df = pd.DataFrame([metrics])
        comments_df = pd.DataFrame.from_dict(comments, orient='index', columns=['Comments'])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        comments_df.to_excel(writer, sheet_name='Summary', startrow=len(summary_df) + 2)

        for name, df in tables.items():
            if not df.empty:
                sheet_name = re.sub(r'[\\/*?:"<>|]', "", name)[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    return output.getvalue()

# Main App Layout
st.title("🏗️ Operational Workstreams - Fund Administration Periodic Table")

st.markdown("""
### Interactive Workstream Management & 3D Analysis Platform

This application provides a comprehensive view of fund administration operational workstreams with interactive management capabilities and real-time 3D analysis.
""")

# Create tabs for different sections
main_tab1, main_tab2, main_tab3, main_tab4, main_tab5, main_tab6, main_tab7, main_tab8 = st.tabs([
    "🧪 Workstream Views",
    "📊 3D Analysis", 
    "⚙️ Manage Workstreams",
    "💰 Capital Projects",
    "📄 Source Code",
    "💼 P&L Analysis",
    "🏆 Competitors Analysis",
    "📋 Business Cases"
])

with main_tab1:
    st.markdown("### 🎯 Workstream Visualization Hub")
    st.markdown("*Choose from multiple professional visualization options to analyze your fund administration workstreams.*")
    
    # Visualization selector
    viz_option = st.selectbox(
        "Select Visualization Type:",
        ["🎯 Strategic Matrix", "📊 Analytics Dashboard", "📅 Timeline Roadmap", "🌞 Hierarchy View"],
        key="viz_selector"
    )
    
    if viz_option == "🎯 Strategic Matrix":
        st.markdown("""
        **Strategic Risk vs Automation Matrix**
        - **Quadrant Analysis**: Identify workstreams by risk/automation levels
        - **Investment Sizing**: Bubble size shows investment amount
        - **Category Grouping**: Colors represent different workstream categories
        - **Strategic Insights**: Clear quadrants show priority actions needed
        """)
        
        fig = create_workstream_matrix_view()
        st.plotly_chart(fig, use_container_width=True)
        
        # Strategic insights
        df = pd.DataFrame(st.session_state.workstream_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🚨 Critical Attention Needed")
            critical = df[(df['risk'] > 5) & (df['automation'] < 5)]
            for _, row in critical.iterrows():
                st.warning(f"**{row['name']}** - Risk: {row['risk']}/10, Auto: {row['automation']}/10")
        
        with col2:
            st.markdown("#### ✅ Well Performing")
            stable = df[(df['risk'] <= 5) & (df['automation'] >= 7)]
            for _, row in stable.iterrows():
                st.success(f"**{row['name']}** - Risk: {row['risk']}/10, Auto: {row['automation']}/10")
    
    elif viz_option == "📊 Analytics Dashboard":
        st.markdown("""
        **Comprehensive Analytics Dashboard**
        - **Investment Analysis**: See where money is allocated across categories
        - **Progress Tracking**: Monitor completion rates by category
        - **Risk Assessment**: Understand complexity vs risk relationships
        - **Priority Overview**: Visual breakdown of priority distribution
        """)
        
        fig = create_workstream_dashboard()
        st.plotly_chart(fig, use_container_width=True)
        
        # Key metrics summary
        df = pd.DataFrame(st.session_state.workstream_data)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Investment", f"${df['investment'].sum():.1f}M")
        with col2:
            st.metric("Avg Completion", f"{df['completion'].mean():.1f}%")
        with col3:
            st.metric("High Risk Items", len(df[df['risk'] >= 7]))
        with col4:
            st.metric("Low Automation", len(df[df['automation'] <= 4]))
    
    elif viz_option == "📅 Timeline Roadmap":
        st.markdown("""
        **Project Timeline & Completion Roadmap**
        - **Progress Bars**: Visual completion status for each workstream
        - **Target Dates**: Estimated completion dates based on current progress
        - **Priority Indicators**: Diamond markers show priority levels
        - **Category Colors**: Easy identification of workstream types
        """)
        
        fig = create_workstream_timeline()
        st.plotly_chart(fig, use_container_width=True)
        
        # Timeline insights
        df = pd.DataFrame(st.session_state.workstream_data)
        current_date = pd.Timestamp.now()
        df['days_remaining'] = ((100 - df['completion']) * 2)
        df['target_date'] = current_date + pd.to_timedelta(df['days_remaining'], unit='D')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ⏰ Upcoming Completions (Next 30 Days)")
            upcoming = df[df['days_remaining'] <= 30].sort_values('days_remaining')
            for _, row in upcoming.iterrows():
                days_left = int(row['days_remaining'])
                st.info(f"**{row['name']}** - {days_left} days remaining")
        
        with col2:
            st.markdown("#### 🐌 Longest Timeline")
            longest = df.nlargest(3, 'days_remaining')
            for _, row in longest.iterrows():
                days_left = int(row['days_remaining'])
                st.warning(f"**{row['name']}** - {days_left} days remaining")
    
    elif viz_option == "🌞 Hierarchy View":
        st.markdown("""
        **Investment Hierarchy & Distribution**
        - **Sunburst Design**: Hierarchical view of categories and workstreams
        - **Investment Sizing**: Segment size represents investment amount
        - **Category Grouping**: Inner ring shows categories, outer ring shows workstreams
        - **Interactive**: Click to drill down into specific categories
        """)
        
        fig = create_workstream_hierarchy()
        st.plotly_chart(fig, use_container_width=True)
        
        # Investment breakdown
        df = pd.DataFrame(st.session_state.workstream_data)
        
        st.markdown("#### 💰 Investment Breakdown by Category")
        
        investment_summary = df.groupby('category').agg({
            'investment': 'sum',
            'name': 'count',
            'completion': 'mean'
        }).round(2)
        investment_summary.columns = ['Total Investment ($M)', 'Number of Workstreams', 'Avg Completion (%)']
        investment_summary = investment_summary.sort_values('Total Investment ($M)', ascending=False)
        
        st.dataframe(investment_summary, use_container_width=True)
    
    # Summary metrics
    df = pd.DataFrame(st.session_state.workstream_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Workstreams", len(df))
    
    with col2:
        avg_completion = df['completion'].mean()
        st.metric("Avg Completion", f"{avg_completion:.1f}%")
    
    with col3:
        total_investment = df['investment'].sum()
        st.metric("Total Investment", f"${total_investment:.1f}M")
    
    with col4:
        high_priority = len(df[df['priority'] == 'High'])
        st.metric("High Priority", f"{high_priority} workstreams")

with main_tab2:
    st.markdown("### 🎲 Advanced 3D Workstream Analysis")
    st.markdown("*Explore multi-dimensional relationships with sophisticated 3D analysis tools. Each visualization reveals different strategic insights.*")
    
    # Check if P&L data is available for additional analyses
    pl_available = not st.session_state.pl_data.empty
    
    # Base workstream analysis options
    base_options = [
        "🎯 Strategic Analysis (Complexity × Automation × Risk)",
        "💰 Investment Performance (Investment × Performance × Timeline)", 
        "📊 ROI Analysis (Investment × Completion × ROI)",
        "🔮 Scenario Planning (Current vs Future Projections)",
        "🌐 Network Dependencies (Workstream Interdependencies)"
    ]
    
    # P&L analysis options
    pl_options = [
        "💼 P&L Profitability (Revenue × Costs × AUM)",
        "💼 Service Line Diversity (Diversity × Profitability × Efficiency)",
        "💼 Cost Efficiency (Labor × Technology × Overhead)"
    ]
    
    if pl_available:
        all_options = base_options + ["---"] + pl_options
        st.success("🎯 P&L Analysis enabled! Advanced financial 3D visualizations available.")
    else:
        all_options = base_options
        st.info("💡 Upload P&L data in the P&L Analysis tab to unlock advanced financial 3D visualizations.")
    
    # 3D Analysis selector
    analysis_type = st.selectbox(
        "Select 3D Analysis Type:",
        all_options,
        key="analysis_selector"
    )
    
    if "Strategic Analysis" in analysis_type:
        st.markdown("""
        **Enhanced Strategic 3D Analysis**
        - **Priority Grouping**: Different shapes and colors by priority level
        - **Reference Planes**: Visual risk threshold indicators  
        - **Optimal Zones**: Green zones show ideal automation/low risk areas
        - **Critical Zones**: Red zones highlight high-risk, low-automation areas
        """)
        
        fig = create_3d_complexity_automation_risk()
        st.plotly_chart(fig, use_container_width=True)
        
        # Strategic recommendations
        df = pd.DataFrame(st.session_state.workstream_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🎯 Strategic Recommendations")
            optimal = df[(df['automation'] >= 7) & (df['risk'] <= 5)]
            critical = df[(df['automation'] <= 4) & (df['risk'] >= 6)]
            
            if len(optimal) > 0:
                st.success(f"**{len(optimal)} workstreams** in optimal zone")
            if len(critical) > 0:
                st.error(f"**{len(critical)} workstreams** need immediate attention")
        
        with col2:
            st.markdown("#### 💡 Key Insights")
            avg_automation = df['automation'].mean()
            avg_risk = df['risk'].mean()
            st.info(f"Portfolio Avg: {avg_automation:.1f}/10 automation, {avg_risk:.1f}/10 risk")
    
    elif "Investment Performance" in analysis_type:
        st.markdown("""
        **Investment Performance 3D Analysis**
        - **Performance Score**: Calculated from automation, risk, and completion
        - **Timeline Projection**: Days to completion based on current progress
        - **Investment Efficiency**: See which investments yield best performance
        - **Category Clustering**: Visualize performance by workstream category
        """)
        
        fig = create_3d_investment_performance()
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance insights
        df = pd.DataFrame(st.session_state.workstream_data)
        df['performance_score'] = (df['automation'] * 0.4 + (11-df['risk']) * 0.3 + df['completion']/10 * 0.3)
        df['timeline_days'] = (100 - df['completion']) * 2
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏆 Top Performers")
            top_performers = df.nlargest(3, 'performance_score')
            for _, row in top_performers.iterrows():
                st.success(f"**{row['name']}** - Score: {row['performance_score']:.2f}/10")
        
        with col2:
            st.markdown("#### ⚡ Quick Wins (Short Timeline)")
            quick_wins = df.nsmallest(3, 'timeline_days')
            for _, row in quick_wins.iterrows():
                st.info(f"**{row['name']}** - {int(row['timeline_days'])} days")
    
    elif "ROI Analysis" in analysis_type:
        st.markdown("""
        **Return on Investment 3D Analysis**
        - **ROI Surface**: 3D landscape showing ROI potential across investment/completion space
        - **Actual Positions**: Current workstreams positioned on ROI landscape
        - **Investment Efficiency**: Compare expected returns vs investment amounts
        - **Priority Indicators**: High-priority items shown as diamonds
        """)
        
        fig = create_3d_roi_analysis()
        st.plotly_chart(fig, use_container_width=True)
        
        # ROI insights
        df = pd.DataFrame(st.session_state.workstream_data)
        df['roi_estimate'] = ((df['automation'] - 3) * 0.5 + (8 - df['risk']) * 0.3) * df['investment']
        df['roi_estimate'] = df['roi_estimate'].clip(lower=-5, upper=20)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💰 Best ROI Opportunities")
            best_roi = df.nlargest(3, 'roi_estimate')
            for _, row in best_roi.iterrows():
                st.success(f"**{row['name']}** - Est. ROI: ${row['roi_estimate']:.1f}M")
        
        with col2:
            st.markdown("#### ⚠️ ROI Concerns")
            low_roi = df.nsmallest(3, 'roi_estimate')
            for _, row in low_roi.iterrows():
                st.warning(f"**{row['name']}** - Est. ROI: ${row['roi_estimate']:.1f}M")
    
    elif "Scenario Planning" in analysis_type:
        st.markdown("""
        **Future Scenario 3D Projections**
        - **Current State**: Solid markers show current workstream positions
        - **Future Projections**: Diamond markers show optimistic future state
        - **Trajectory Lines**: Dotted lines connect current to future positions
        - **Progress Visualization**: See potential improvement paths for each workstream
        """)
        
        fig = create_3d_scenario_analysis()
        st.plotly_chart(fig, use_container_width=True)
        
        # Scenario insights
        df = pd.DataFrame(st.session_state.workstream_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📈 Projected Improvements")
            st.info("**Optimistic Scenario Assumptions:**")
            st.write("• +30% completion increase")
            st.write("• -2 points risk reduction")
            st.write("• Complexity remains constant")
        
        with col2:
            st.markdown("#### 🎯 Biggest Opportunity")
            biggest_gaps = df[df['completion'] < 50]
            if len(biggest_gaps) > 0:
                for _, row in biggest_gaps.head(3).iterrows():
                    st.warning(f"**{row['name']}** - {row['completion']}% complete")
    
    elif "Network Dependencies" in analysis_type:
        st.markdown("""
        **Workstream Interdependency Network 3D**
        - **Network Layout**: Workstreams positioned by complexity (radius) and risk (height)
        - **Category Connections**: Lines connect related workstreams within categories
        - **Dependency Visualization**: See which workstreams are interconnected
        - **Investment Sizing**: Node size represents investment amount
        """)
        
        fig = create_3d_network_analysis()
        st.plotly_chart(fig, use_container_width=True)
        
        # Network insights
        df = pd.DataFrame(st.session_state.workstream_data)
        category_counts = df['category'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌐 Network Statistics")
            st.info(f"**{len(df)}** total workstreams")
            st.info(f"**{len(category_counts)}** categories")
            st.info(f"**{category_counts.max()}** max per category")
        
        with col2:
            st.markdown("#### 🔗 Dependency Insights")
            st.warning("**High Complexity Categories** may create bottlenecks")
            complex_categories = df.groupby('category')['complexity'].mean().sort_values(ascending=False)
            for cat, complexity in complex_categories.head(3).items():
                st.write(f"• {cat}: {complexity:.1f}/10")
    
    elif "P&L Profitability" in analysis_type:
        st.markdown("""
        **P&L Profitability 3D Analysis**
        - **Revenue vs Costs**: Shows the relationship between revenue and costs
        - **AUM Dimension**: Assets Under Management as the third dimension
        - **Service Line Coloring**: Colors represent dominant service line
        - **Profitability Sizing**: Marker size represents gross margin percentage
        - **Break-Even Plane**: Visual reference for break-even threshold
        """)
        
        fig = create_3d_pl_profitability_analysis()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # P&L insights
            pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
            if not pl_analysis.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 💰 Profitability Insights")
                    avg_margin = pl_analysis['Gross_Margin_Percent'].mean()
                    high_margin_count = len(pl_analysis[pl_analysis['Gross_Margin_Percent'] > 25])
                    st.info(f"**{avg_margin:.1f}%** average gross margin")
                    st.info(f"**{high_margin_count}** high-margin clients (>25%)")
                
                with col2:
                    st.markdown("#### 🎯 Service Line Focus")
                    service_revenues = [
                        pl_analysis['Fund_Accounting_Revenue_USD'].sum(),
                        pl_analysis['Fund_Administration_Revenue_USD'].sum(),
                        pl_analysis['Transfer_Agency_Revenue_USD'].sum(),
                        pl_analysis['Regulatory_Reporting_Revenue_USD'].sum()
                    ]
                    service_names = ['Fund Accounting', 'Fund Administration', 'Transfer Agency', 'Regulatory Reporting']
                    dominant = service_names[service_revenues.index(max(service_revenues))]
                    st.success(f"**{dominant}** is the dominant service line")
        else:
            st.warning("P&L data is required for this analysis. Please upload data in the P&L Analysis tab.")
    
    elif "Service Line Diversity" in analysis_type:
        st.markdown("""
        **Service Line Diversity 3D Analysis**
        - **Diversity Index**: Shannon entropy measuring service line mix
        - **Profitability**: Gross margin percentage
        - **Efficiency**: Revenue per AUM in basis points
        - **Fund Count**: Color scale represents number of funds managed
        - **Revenue Sizing**: Marker size proportional to total revenue
        """)
        
        fig = create_3d_service_line_analysis()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Service diversity insights
            pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
            if not pl_analysis.empty:
                # Calculate diversity scores
                diversity_scores = []
                for _, row in pl_analysis.iterrows():
                    revenues = [row['Fund_Accounting_Revenue_USD'], row['Fund_Administration_Revenue_USD'],
                               row['Transfer_Agency_Revenue_USD'], row['Regulatory_Reporting_Revenue_USD']]
                    total_rev = sum(revenues)
                    if total_rev > 0:
                        proportions = [r/total_rev for r in revenues if r > 0]
                        diversity_index = -sum([p * np.log(p) for p in proportions if p > 0])
                    else:
                        diversity_index = 0
                    diversity_scores.append(diversity_index)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🌈 Diversity Analysis")
                    avg_diversity = np.mean(diversity_scores)
                    max_diversity = np.log(4)  # Maximum possible for 4 service lines
                    st.info(f"**{avg_diversity:.2f}** average diversity index")
                    st.info(f"**{(avg_diversity/max_diversity)*100:.1f}%** of maximum diversity")
                
                with col2:
                    st.markdown("#### 📈 Performance Correlation")
                    high_diversity = [i for i, d in enumerate(diversity_scores) if d > avg_diversity]
                    if high_diversity:
                        high_div_margin = pl_analysis.iloc[high_diversity]['Gross_Margin_Percent'].mean()
                        st.success(f"High-diversity clients avg **{high_div_margin:.1f}%** margin")
        else:
            st.warning("P&L data is required for this analysis. Please upload data in the P&L Analysis tab.")
    
    elif "Cost Efficiency" in analysis_type:
        st.markdown("""
        **Cost Efficiency 3D Analysis**
        - **Labor Efficiency**: Revenue divided by direct labor costs
        - **Technology Efficiency**: Revenue divided by technology costs  
        - **Overhead Ratio**: Overhead as percentage of revenue
        - **Profitability Quartiles**: Color-coded by gross margin quartiles
        - **AUM Sizing**: Marker size represents Assets Under Management
        """)
        
        fig = create_3d_cost_efficiency_analysis()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost efficiency insights
            pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
            if not pl_analysis.empty:
                # Calculate efficiency metrics with safe division
                pl_analysis['Labor_Efficiency'] = np.where(
                    pl_analysis['Total_Direct_Labor_Cost'] > 0, 
                    pl_analysis['Total_Annual_Revenue_USD'] / pl_analysis['Total_Direct_Labor_Cost'],
                    0
                )
                pl_analysis['Tech_Efficiency'] = np.where(
                    pl_analysis['Total_Technology_Cost'] > 0,
                    pl_analysis['Total_Annual_Revenue_USD'] / pl_analysis['Total_Technology_Cost'],
                    0
                )
                pl_analysis['Overhead_Ratio'] = np.where(
                    pl_analysis['Total_Annual_Revenue_USD'] > 0,
                    pl_analysis['Overhead_Allocation'] / pl_analysis['Total_Annual_Revenue_USD'],
                    0
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### ⚡ Efficiency Benchmarks")
                    avg_labor_eff = pl_analysis['Labor_Efficiency'].mean()
                    avg_tech_eff = pl_analysis['Tech_Efficiency'].mean()
                    avg_overhead = pl_analysis['Overhead_Ratio'].mean() * 100
                    st.info(f"**{avg_labor_eff:.2f}x** average labor efficiency")
                    st.info(f"**{avg_tech_eff:.2f}x** average tech efficiency")
                    st.info(f"**{avg_overhead:.1f}%** average overhead ratio")
                
                with col2:
                    st.markdown("#### 🏆 Top Performers")
                    top_labor = pl_analysis.nlargest(1, 'Labor_Efficiency').iloc[0]
                    top_tech = pl_analysis.nlargest(1, 'Tech_Efficiency').iloc[0]
                    st.success(f"**Labor**: {top_labor['Client_Name']} ({top_labor['Labor_Efficiency']:.2f}x)")
                    st.success(f"**Tech**: {top_tech['Client_Name']} ({top_tech['Tech_Efficiency']:.2f}x)")
        else:
            st.warning("P&L data is required for this analysis. Please upload data in the P&L Analysis tab.")
    
    # Advanced controls
    st.markdown("---")
    st.markdown("### 🎛️ Advanced Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reset Camera View", key="reset_camera"):
            st.info("Refresh the page to reset 3D camera positions")
    
    with col2:
        show_insights = st.checkbox("📊 Show Data Insights", value=True, key="show_insights")
    
    with col3:
        export_3d = st.button("💾 Export 3D Data", key="export_3d")
        if export_3d:
            df = pd.DataFrame(st.session_state.workstream_data)
            st.download_button(
                "Download 3D Analysis Data",
                df.to_csv(index=False),
                "3d_workstream_analysis.csv",
                "text/csv"
            )
    
    # Analysis insights
    df = pd.DataFrame(st.session_state.workstream_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Key Insights")
        
        # High complexity, low automation workstreams
        high_complex_low_auto = df[(df['complexity'] >= 7) & (df['automation'] <= 4)]
        if not high_complex_low_auto.empty:
            st.warning("**High Complexity, Low Automation Workstreams:**")
            for _, row in high_complex_low_auto.iterrows():
                st.write(f"• {row['name']} - Investment: ${row['investment']}M")
        
        # High risk workstreams
        high_risk = df[df['risk'] >= 7]
        if not high_risk.empty:
            st.error("**High Risk Workstreams Requiring Attention:**")
            for _, row in high_risk.iterrows():
                st.write(f"• {row['name']} - Risk Level: {row['risk']}/10")
    
    with col2:
        st.markdown("#### 🎯 Recommendations")
        
        # Investment recommendations
        low_investment_high_risk = df[(df['investment'] <= 2.0) & (df['risk'] >= 6)]
        if not low_investment_high_risk.empty:
            st.info("**Consider Increased Investment:**")
            for _, row in low_investment_high_risk.iterrows():
                st.write(f"• {row['name']} - Current: ${row['investment']}M")
        
        # Automation opportunities
        low_automation = df[df['automation'] <= 4].sort_values('complexity', ascending=False)
        if not low_automation.empty:
            st.success("**Automation Opportunities:**")
            for _, row in low_automation.head(3).iterrows():
                st.write(f"• {row['name']} - Automation: {row['automation']}/10")

with main_tab3:
    workstream_management_interface()
    
    # Real-time data export
    st.markdown("---")
    st.subheader("📤 Export Data")
    
    df = pd.DataFrame(st.session_state.workstream_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name=f"workstreams_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="Download as JSON", 
            data=json_data,
            file_name=f"workstreams_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

with main_tab4:
    st.markdown("### 💰 Capital Project Portfolio Dashboard")
    st.markdown("This section provides an interactive overview of your capital projects, allowing you to track financials, monitor trends, and identify variances.")
    
    uploaded_file = st.file_uploader("Upload your Capital Project CSV or Excel file", type=["csv", "xlsx"], key="capital_project_upload")
    
    if uploaded_file is not None:
        st.session_state.reports_ready = False
        df_capital = load_capital_project_data(uploaded_file)
        if not df_capital.empty:
            st.sidebar.header("Filter Projects")
            filter_columns = { 
                "PORTFOLIO_OBS_LEVEL1": "Select Portfolio Level", 
                "SUB_PORTFOLIO_OBS_LEVEL2": "Select Sub-Portfolio Level", 
                "PROJECT_MANAGER": "Select Project Manager", 
                "BRS_CLASSIFICATION": "Select BRS Classification", 
                "FUND_DECISION": "Select Fund Decision" 
            }
            selected_filters = {}
            for col_name, display_name in filter_columns.items():
                if col_name in df_capital.columns:
                    options = ['All'] + sorted(df_capital[col_name].dropna().unique())
                    selected_filters[col_name] = st.sidebar.selectbox(display_name, options, 
                                                                    on_change=lambda: st.session_state.update(reports_ready=False),
                                                                    key=f"filter_{col_name}")
                else:
                    if col_name == "FUND_DECISION": 
                        st.sidebar.info(f"Column '{col_name}' not found.")
                    selected_filters[col_name] = 'All'
            
            filtered_df_capital = df_capital.copy()
            for col_name, selected_value in selected_filters.items():
                if selected_value != 'All' and col_name in filtered_df_capital.columns:
                    filtered_df_capital = filtered_df_capital[filtered_df_capital[col_name] == selected_value]

            if filtered_df_capital.empty:
                st.warning("No projects match the selected filters.")
                st.stop()

            # Calculate metrics
            total_projects = len(filtered_df_capital)
            sum_actual_spend_ytd = filtered_df_capital['SUM_ACTUAL_SPEND_YTD'].sum()
            sum_of_forecasted_numbers_sum = filtered_df_capital['SUM_OF_FORECASTED_NUMBERS'].sum()
            run_rate_per_month = filtered_df_capital['RUN_RATE_PER_MONTH'].mean()
            capital_underspend = filtered_df_capital['CAPITAL_UNDERSPEND'].sum()
            capital_overspend = filtered_df_capital['CAPITAL_OVERSPEND'].sum()
            net_reallocation_amount = filtered_df_capital['NET_REALLOCATION_AMOUNT'].sum()

            st.subheader("Key Metrics Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Number of Projects", total_projects)
            col2.metric("Sum Actual Spend (YTD)", f"${sum_actual_spend_ytd:,.2f}")
            col3.metric("Sum Of Forecasted Numbers", f"${sum_of_forecasted_numbers_sum:,.2f}")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Average Run Rate / Month", f"${run_rate_per_month:,.2f}")
            m2.metric("Total Potential Underspend", f"${capital_underspend:,.2f}")
            m3.metric("Total Potential Overspend", f"${capital_overspend:,.2f}")
            m4.metric("Net Reallocation Amount", f"${net_reallocation_amount:,.2f}")
            st.markdown("---")

            # Project Details Table
            st.subheader("Project Details")
            current_year = datetime.now().year
            project_table_cols = [ 
                'PORTFOLIO_OBS_LEVEL1', 'SUB_PORTFOLIO_OBS_LEVEL2', 'PROJECT_NAME', 'PROJECT_MANAGER', 
                'BRS_CLASSIFICATION', 'FUND_DECISION', 'BUSINESS_ALLOCATION', 'CURRENT_EAC', 
                'ALL_PRIOR_YEARS_ACTUALS', f'TOTAL_{current_year}_ACTUALS', f'TOTAL_{current_year}_FORECASTS', 
                f'TOTAL_{current_year}_CAPITAL_PLAN', 'CAPITAL_UNDERSPEND', 'CAPITAL_OVERSPEND', 'AVERAGE_MONTHLY_SPREAD_SCORE' 
            ]
            project_table_cols_present = [col for col in project_table_cols if col in filtered_df_capital.columns]
            financial_format_map = { col: "${:,.2f}" for col in project_table_cols_present if any(keyword in col for keyword in ['ACTUALS', 'FORECASTS', 'PLAN', 'ALLOCATION', 'EAC', 'SPEND', 'AMOUNT', 'SCORE'])}
            st.dataframe(filtered_df_capital[project_table_cols_present].style.format(financial_format_map), use_container_width=True, hide_index=True)
            st.markdown("---")

            # Generate and download reports
            st.subheader("Generate Professional Reports")
            st.markdown("Add your comments in the sections above, then click the button below to prepare your downloadable reports.")

            if st.button("Prepare Reports for Download", key="prepare_capital_reports"):
                st.session_state.reports_ready = True

            if st.session_state.get('reports_ready', False):
                metrics_data = {
                    "Number of Projects": total_projects,
                    "Sum Actual Spend (YTD)": f"${sum_actual_spend_ytd:,.2f}",
                    "Sum Of Forecasted Numbers": f"${sum_of_forecasted_numbers_sum:,.2f}",
                    "Avg Run Rate / Month": f"${run_rate_per_month:,.2f}",
                    "Total Potential Underspend": f"${capital_underspend:,.2f}",
                    "Total Potential Overspend": f"${capital_overspend:,.2f}",
                    "Net Reallocation": f"${net_reallocation_amount:,.2f}"
                }
                
                # Create HTML report
                html_report_content = generate_capital_html_report(metrics_data, filtered_df_capital)
                
                # Create Excel report
                excel_report_content = generate_capital_excel_report(metrics_data, filtered_df_capital)
                
                st.info("Your reports are ready to download below.")
                dl1, dl2 = st.columns(2)
                dl1.download_button("⬇️ Download Report as HTML", html_report_content, "capital_project_report.html", "text/html")
                dl2.download_button("⬇️ Download Report as Excel", excel_report_content, "capital_project_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Upload your Capital Project CSV or Excel file to get started!")

with main_tab5:
    st.markdown("### 📄 Application Source Code")
    st.markdown("*View the complete source code of this Streamlit application.*")
    
    st.markdown("---")
    with st.expander("View Application Source Code", expanded=False):
        try:
            # Read the current file's source code
            with open(__file__, 'r', encoding='utf-8') as file:
                source_code = file.read()
            st.code(source_code, language='python')
        except Exception as e:
            st.error(f"Error reading source code: {e}")
            # Fallback using inspect
            try:
                import inspect
                source_code = inspect.getsource(inspect.getmodule(inspect.currentframe()))
                st.code(source_code, language='python')
            except Exception as e2:
                st.error(f"Fallback method also failed: {e2}")
    
    # Additional information about the application
    st.markdown("---")
    st.markdown("### 📊 Application Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            with open(__file__, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            st.metric("Total Lines of Code", len(lines))
        except:
            st.metric("Total Lines of Code", "N/A")
    
    with col2:
        try:
            with open(__file__, 'r', encoding='utf-8') as file:
                content = file.read()
            function_count = content.count('def ')
            st.metric("Total Functions", function_count)
        except:
            st.metric("Total Functions", "N/A")
    
    with col3:
        try:
            with open(__file__, 'r', encoding='utf-8') as file:
                content = file.read()
            import_count = content.count('import ')
            st.metric("Import Statements", import_count)
        except:
            st.metric("Import Statements", "N/A")
    
    st.markdown("---")
    st.markdown("### 🔧 Technical Dependencies")
    st.markdown("""
    **Core Libraries:**
    - `streamlit` - Web application framework
    - `pandas` - Data manipulation and analysis
    - `plotly` - Interactive visualizations and 3D charts
    - `numpy` - Numerical computing
    
    **Standard Libraries:**
    - `datetime` - Date and time handling
    - `json` - JSON data processing
    - `io` - Input/output operations
    - `re` - Regular expressions
    - `inspect` - Runtime inspection utilities
    """)
    
    st.markdown("---")
    st.markdown("### 📋 Application Features")
    st.markdown("""
    **🧪 Workstream Views:**
    - Periodic Table Layout
    - Strategic Matrix Analysis  
    - Analytics Dashboard
    - Timeline Roadmap
    - Hierarchy Visualization
    
    **📊 3D Analysis:**
    - Enhanced 3D Complexity Analysis
    - Strategic Priority Mapping
    - Investment Performance Analysis
    - Surface Plot Analysis
    - Network Relationship Analysis
    
    **⚙️ Workstream Management:**
    - Add/Edit/Delete Operations
    - Excel/CSV Data Upload
    - Data Export Functionality
    - Session State Management
    
    **💰 Capital Projects:**
    - Financial Data Processing
    - Project Portfolio Analysis
    - Variance Analysis
    - Professional Report Generation
    - HTML/Excel Export
    """)

with main_tab6:
    st.markdown("### 💼 Fund Administration P&L Analysis")
    st.markdown("*Comprehensive Profit & Loss analysis for Fund Administration and Accounting Products using revenue attribution and cost allocation methodologies.*")
    
    st.markdown("---")
    
    # P&L Analysis Methodology Section
    with st.expander("📋 P&L Analysis Methodology", expanded=False):
        st.markdown("""
        ### Core Methodology: Revenue Attribution & Cost Allocation
        
        **Revenue Attribution:**
        - Uses client rate cards to break down total revenue into specific service lines
        - Fund Accounting, Fund Administration, Transfer Agency, Regulatory Reporting
        - Fixed fees allocated proportionally based on service notional values
        
        **Direct Cost Allocation:**
        - **Labor Costs**: Fund Accountants per client/fund × average fully-burdened cost
        - **Technology Costs**: Software licenses, data providers, cloud infrastructure
        - **Manager Oversight**: Senior management time allocation based on complexity
        
        **Overhead Allocation:**
        - Indirect costs allocated as percentage of direct costs or revenue
        - Management salaries, office rent, compliance, risk management
        - Proportional allocation based on headcount or revenue drivers
        
        **Key Metrics:**
        - Revenue per AUM (basis points)
        - Cost per Fund
        - Gross Margin by Service Line
        - Client Profitability Ranking
        """)
    
    # Data Upload Section
    st.subheader("📂 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 Upload P&L Data")
        uploaded_pl_file = st.file_uploader(
            "Upload P&L Data (Excel/CSV)", 
            type=['xlsx', 'csv'], 
            help="Upload your fund administration P&L data file",
            key="pl_upload"
        )
        
        if uploaded_pl_file:
            with st.spinner("Loading P&L data..."):
                pl_data = load_pl_data(uploaded_pl_file)
                if not pl_data.empty:
                    st.session_state.pl_data = pl_data
                    st.success(f"✅ Loaded {len(pl_data)} records successfully!")
    
    with col2:
        st.markdown("#### 📋 Download Template")
        st.markdown("*Download the standardized P&L template with sample data*")
        
        template_data = create_pl_template()
        template_excel = io.BytesIO()
        
        with pd.ExcelWriter(template_excel, engine='xlsxwriter') as writer:
            template_data.to_excel(writer, sheet_name='PL_Template', index=False)
            
            # Add methodology sheet
            methodology_df = pd.DataFrame({
                'Field_Name': [
                    'Client_Name', 'Fund_Name', 'Fund_AUM_USD_Millions', 'Total_Annual_Revenue_USD',
                    'Fund_Accountants_Required', 'Average_Accountant_Salary_USD', 'Fully_Burdened_Cost_Multiplier',
                    'Software_License_Cost_USD', 'Data_Provider_Costs_USD', 'Number_of_Funds'
                ],
                'Description': [
                    'Client organization name',
                    'Specific fund name',
                    'Assets under management in millions USD',
                    'Total annual revenue from client',
                    'Number of fund accountants required',
                    'Average accountant salary',
                    'Multiplier for benefits/overhead (typically 1.3-1.5)',
                    'Annual software licensing costs',
                    'Annual data provider costs',
                    'Number of funds managed for client'
                ],
                'Data_Type': [
                    'Text', 'Text', 'Number', 'Number',
                    'Number', 'Number', 'Number',
                    'Number', 'Number', 'Integer'
                ]
            })
            methodology_df.to_excel(writer, sheet_name='Data_Dictionary', index=False)
        
        template_excel.seek(0)
        
        st.download_button(
            label="📋 Download P&L Template",
            data=template_excel.getvalue(),
            file_name=f"Fund_Admin_PL_Template_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.markdown("---")
    
    # Analysis Section
    if not st.session_state.pl_data.empty:
        st.subheader("📊 P&L Analysis Dashboard")
        
        # Calculate comprehensive metrics
        with st.spinner("Calculating P&L metrics..."):
            pl_analysis = calculate_pl_metrics(st.session_state.pl_data)
        
        if not pl_analysis.empty:
            # Executive Summary Metrics
            st.markdown("#### 📈 Executive Summary")
            
            total_revenue = pl_analysis['Total_Annual_Revenue_USD'].sum()
            total_costs = pl_analysis['Total_Costs'].sum()
            total_profit = pl_analysis['Gross_Profit'].sum()
            avg_margin = pl_analysis['Gross_Margin_Percent'].mean()
            total_aum = pl_analysis['Fund_AUM_USD_Millions'].sum()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Revenue", f"${total_revenue:,.0f}")
            with col2:
                st.metric("Total Costs", f"${total_costs:,.0f}")
            with col3:
                st.metric("Total Profit", f"${total_profit:,.0f}")
            with col4:
                st.metric("Average Margin", f"{avg_margin:.1f}%")
            with col5:
                st.metric("Total AUM", f"${total_aum:,.0f}M")
            
            st.markdown("---")
            
            # Create visualization charts
            revenue_chart, cost_chart, profit_chart, aum_chart = create_pl_summary_charts(pl_analysis)
            
            # Display charts in tabs
            chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
                "📊 Revenue Breakdown", 
                "💰 Cost Allocation", 
                "📈 Profitability", 
                "🎯 AUM Efficiency"
            ])
            
            with chart_tab1:
                st.plotly_chart(revenue_chart, use_container_width=True)
                
                # Service line summary
                st.markdown("#### Service Line Performance")
                service_summary = pd.DataFrame({
                    'Service_Line': ['Fund Accounting', 'Fund Administration', 'Transfer Agency', 'Regulatory Reporting'],
                    'Total_Revenue': [
                        pl_analysis['Fund_Accounting_Revenue_USD'].sum(),
                        pl_analysis['Fund_Administration_Revenue_USD'].sum(),
                        pl_analysis['Transfer_Agency_Revenue_USD'].sum(),
                        pl_analysis['Regulatory_Reporting_Revenue_USD'].sum()
                    ]
                })
                service_summary['Percentage'] = (service_summary['Total_Revenue'] / service_summary['Total_Revenue'].sum()) * 100
                st.dataframe(service_summary.style.format({
                    'Total_Revenue': '${:,.0f}',
                    'Percentage': '{:.1f}%'
                }), use_container_width=True, hide_index=True)
            
            with chart_tab2:
                st.plotly_chart(cost_chart, use_container_width=True)
                
                # Cost breakdown summary
                st.markdown("#### Cost Category Analysis")
                cost_summary = pd.DataFrame({
                    'Cost_Category': ['Direct Labor', 'Manager Oversight', 'Technology', 'Overhead'],
                    'Total_Cost': [
                        pl_analysis['Total_Direct_Labor_Cost'].sum(),
                        pl_analysis['Manager_Oversight_Cost'].sum(),
                        pl_analysis['Total_Technology_Cost'].sum(),
                        pl_analysis['Overhead_Allocation'].sum()
                    ]
                })
                cost_summary['Percentage'] = (cost_summary['Total_Cost'] / cost_summary['Total_Cost'].sum()) * 100
                st.dataframe(cost_summary.style.format({
                    'Total_Cost': '${:,.0f}',
                    'Percentage': '{:.1f}%'
                }), use_container_width=True, hide_index=True)
            
            with chart_tab3:
                st.plotly_chart(profit_chart, use_container_width=True)
                
                # Top and bottom performers
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🏆 Top Performers")
                    top_performers = pl_analysis.nlargest(3, 'Gross_Margin_Percent')[
                        ['Client_Name', 'Fund_Name', 'Gross_Margin_Percent', 'Gross_Profit']
                    ]
                    st.dataframe(top_performers.style.format({
                        'Gross_Margin_Percent': '{:.1f}%',
                        'Gross_Profit': '${:,.0f}'
                    }), use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("#### 📉 Improvement Opportunities")
                    bottom_performers = pl_analysis.nsmallest(3, 'Gross_Margin_Percent')[
                        ['Client_Name', 'Fund_Name', 'Gross_Margin_Percent', 'Gross_Profit']
                    ]
                    st.dataframe(bottom_performers.style.format({
                        'Gross_Margin_Percent': '{:.1f}%',
                        'Gross_Profit': '${:,.0f}'
                    }), use_container_width=True, hide_index=True)
            
            with chart_tab4:
                st.plotly_chart(aum_chart, use_container_width=True)
                
                # AUM efficiency metrics
                st.markdown("#### AUM-Based Efficiency Metrics")
                efficiency_metrics = pl_analysis[
                    ['Client_Name', 'Fund_AUM_USD_Millions', 'Revenue_Per_AUM_BPS', 'Cost_Per_AUM_BPS']
                ].sort_values('Revenue_Per_AUM_BPS', ascending=False)
                
                st.dataframe(efficiency_metrics.style.format({
                    'Fund_AUM_USD_Millions': '${:,.0f}M',
                    'Revenue_Per_AUM_BPS': '{:.1f} bps',
                    'Cost_Per_AUM_BPS': '{:.1f} bps'
                }), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Detailed Data Table
            st.subheader("📋 Detailed P&L Analysis")
            
            # Key columns for display
            display_columns = [
                'Client_Name', 'Fund_Name', 'Fund_AUM_USD_Millions', 'Number_of_Funds',
                'Total_Annual_Revenue_USD', 'Total_Costs', 'Gross_Profit', 'Gross_Margin_Percent',
                'Revenue_Per_Fund', 'Cost_Per_Fund', 'Revenue_Per_AUM_BPS'
            ]
            
            display_df = pl_analysis[display_columns]
            
            st.dataframe(display_df.style.format({
                'Fund_AUM_USD_Millions': '${:,.0f}M',
                'Total_Annual_Revenue_USD': '${:,.0f}',
                'Total_Costs': '${:,.0f}',
                'Gross_Profit': '${:,.0f}',
                'Gross_Margin_Percent': '{:.1f}%',
                'Revenue_Per_Fund': '${:,.0f}',
                'Cost_Per_Fund': '${:,.0f}',
                'Revenue_Per_AUM_BPS': '{:.1f} bps'
            }), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Export Section
            st.subheader("📤 Export Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Summary statistics for export
                summary_stats = {
                    'Total_Revenue': total_revenue,
                    'Total_Costs': total_costs,
                    'Total_Profit': total_profit,
                    'Average_Margin_Percent': avg_margin,
                    'Total_AUM_Millions': total_aum,
                    'Number_of_Clients': len(pl_analysis),
                    'Analysis_Date': datetime.now().strftime('%Y-%m-%d')
                }
                
                # Generate Excel report
                excel_report = generate_pl_excel_report(pl_analysis, summary_stats)
                
                st.download_button(
                    label="📊 Download Complete P&L Analysis",
                    data=excel_report,
                    file_name=f"Fund_Admin_PL_Analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                # Export filtered data
                csv_data = pl_analysis.to_csv(index=False)
                st.download_button(
                    label="📋 Download Raw Data (CSV)",
                    data=csv_data,
                    file_name=f"PL_Raw_Data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    else:
        # Show template data as example
        st.subheader("📋 Template Preview")
        st.markdown("*Preview of the P&L analysis template with sample data. Upload your data to see full analysis.*")
        
        template_preview = create_pl_template()
        preview_analysis = calculate_pl_metrics(template_preview)
        
        if not preview_analysis.empty:
            # Show sample charts with template data
            revenue_chart, cost_chart, profit_chart, aum_chart = create_pl_summary_charts(preview_analysis)
            
            st.markdown("#### Sample Analysis Preview")
            
            # Sample metrics
            sample_revenue = preview_analysis['Total_Annual_Revenue_USD'].sum()
            sample_costs = preview_analysis['Total_Costs'].sum()
            sample_profit = preview_analysis['Gross_Profit'].sum()
            sample_margin = preview_analysis['Gross_Margin_Percent'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sample Revenue", f"${sample_revenue:,.0f}")
            with col2:
                st.metric("Sample Costs", f"${sample_costs:,.0f}")
            with col3:
                st.metric("Sample Profit", f"${sample_profit:,.0f}")
            with col4:
                st.metric("Sample Margin", f"{sample_margin:.1f}%")
            
            # Sample chart
            st.plotly_chart(profit_chart, use_container_width=True)
            
            # Sample data preview
            st.markdown("#### Template Data Structure")
            st.dataframe(template_preview.head(), use_container_width=True, hide_index=True)

with main_tab7:
    st.markdown("### 🏆 Fund Administration Competitors Analysis")
    st.markdown("*Strategic competitive intelligence platform for analyzing major players in the Fund Administration and Custody services market.*")
    
    st.markdown("---")
    
    # Competitive Analysis Methodology
    with st.expander("📋 Competitive Analysis Framework", expanded=False):
        st.markdown("""
        ### Strategic Competitive Intelligence Framework
        
        **Market Positioning Analysis:**
        - Assets Under Administration vs Market Share positioning
        - Technology investment correlation with client satisfaction
        - Geographic presence and target client segment analysis
        
        **Technology Capability Assessment:**
        - AI/ML capabilities maturity evaluation
        - Cloud-native platform adoption analysis
        - API integration and digital transformation readiness
        - Blockchain and emerging technology implementation
        
        **Operational Excellence Benchmarking:**
        - Client satisfaction and Net Promoter Score tracking
        - Technology investment as percentage of revenue
        - Employee count and operational efficiency ratios
        - ESG focus and sustainability initiatives scoring
        
        **Strategic Intelligence Insights:**
        - Market concentration and competitive dynamics
        - Recent acquisitions and consolidation trends
        - Technology initiatives and innovation investments
        - Competitive strengths and vulnerability analysis
        """)
    
    # Data Management Section
    st.subheader("📂 Competitor Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 Upload Competitors Data")
        uploaded_competitors_file = st.file_uploader(
            "Upload Competitors Data (Excel/CSV)", 
            type=['xlsx', 'csv'], 
            help="Upload your competitors analysis data file",
            key="competitors_upload"
        )
        
        if uploaded_competitors_file:
            with st.spinner("Loading competitors data..."):
                competitors_data = load_competitors_data(uploaded_competitors_file)
                if not competitors_data.empty:
                    st.session_state.competitors_data = competitors_data
                    st.success(f"✅ Loaded {len(competitors_data)} competitors successfully!")
    
    with col2:
        st.markdown("#### 📋 Download Template")
        st.markdown("*Download the comprehensive competitors analysis template with sample data*")
        
        template_data = create_competitors_template()
        template_excel = io.BytesIO()
        
        with pd.ExcelWriter(template_excel, engine='xlsxwriter') as writer:
            template_data.to_excel(writer, sheet_name='Competitors_Template', index=False)
            
            # Add data dictionary
            data_dict = pd.DataFrame({
                'Field_Category': [
                    'Basic Information', 'Basic Information', 'Fund Administration', 'Fund Administration', 
                    'Technology', 'Technology', 'Market Position', 'Operational', 'Strategic'
                ],
                'Field_Name': [
                    'Competitor_Name', 'Competitor_Type', 'Assets_Under_Administration_USD_Trillions', 
                    'Number_of_Funds_Administered', 'AI_ML_Capabilities', 'API_Integration_Score',
                    'Market_Share_Percent', 'Client_Satisfaction_Score', 'Key_Strengths'
                ],
                'Description': [
                    'Official competitor name',
                    'Bank category (Custody Bank, Universal Bank, etc.)',
                    'Total assets under administration in trillions USD',
                    'Total number of funds administered',
                    'AI/ML maturity level (Advanced/Intermediate/Basic)',
                    'API integration capability score (1-10)',
                    'Market share percentage in fund administration',
                    'Client satisfaction score (1-10)',
                    'Key competitive strengths'
                ],
                'Data_Type': [
                    'Text', 'Text', 'Number', 'Integer', 'Text', 'Integer', 'Number', 'Number', 'Text'
                ]
            })
            data_dict.to_excel(writer, sheet_name='Data_Dictionary', index=False)
        
        template_excel.seek(0)
        
        st.download_button(
            label="📋 Download Competitors Template",
            data=template_excel.getvalue(),
            file_name=f"Competitors_Analysis_Template_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.markdown("---")
    
    # Analysis Dashboard
    if not st.session_state.competitors_data.empty:
        st.subheader("📊 Competitive Intelligence Dashboard")
        
        # Generate insights
        with st.spinner("Analyzing competitive landscape..."):
            competitive_insights = generate_competitive_insights(st.session_state.competitors_data)
        
        # Executive Summary
        st.markdown("#### 🎯 Executive Summary")
        
        df_comp = st.session_state.competitors_data
        total_competitors = len(df_comp)
        total_aum = df_comp['Assets_Under_Administration_USD_Trillions'].sum()
        avg_market_share = df_comp['Market_Share_Percent'].mean()
        tech_leaders = len(df_comp[df_comp['AI_ML_Capabilities'] == 'Advanced'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Competitors", total_competitors)
        with col2:
            st.metric("Combined AUM", f"${total_aum:.1f}T")
        with col3:
            st.metric("Avg Market Share", f"{avg_market_share:.1f}%")
        with col4:
            st.metric("Tech Leaders", f"{tech_leaders} competitors")
        
        st.markdown("---")
        
        # Visualization Charts
        chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
            "🎯 Market Positioning", 
            "💻 Technology Analysis", 
            "📈 Market Evolution",
            "🔍 Strategic Insights"
        ])
        
        with chart_tab1:
            st.markdown("#### Competitive Positioning Map")
            positioning_chart = create_competitive_positioning_chart(df_comp)
            if positioning_chart:
                st.plotly_chart(positioning_chart, use_container_width=True)
                
                # Market leaders analysis
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🏆 Market Leaders (by AUM)")
                    top_aum = df_comp.nlargest(5, 'Assets_Under_Administration_USD_Trillions')[
                        ['Competitor_Name', 'Assets_Under_Administration_USD_Trillions', 'Market_Share_Percent']
                    ]
                    st.dataframe(top_aum.style.format({
                        'Assets_Under_Administration_USD_Trillions': '${:.1f}T',
                        'Market_Share_Percent': '{:.1f}%'
                    }), use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("#### 📊 Client Satisfaction Leaders")
                    top_satisfaction = df_comp.nlargest(5, 'Client_Satisfaction_Score')[
                        ['Competitor_Name', 'Client_Satisfaction_Score', 'Net_Promoter_Score']
                    ]
                    st.dataframe(top_satisfaction.style.format({
                        'Client_Satisfaction_Score': '{:.1f}/10',
                        'Net_Promoter_Score': '{:.0f}'
                    }), use_container_width=True, hide_index=True)
        
        with chart_tab2:
            st.markdown("#### Technology Capabilities Comparison")
            tech_radar = create_technology_capability_radar(df_comp)
            if tech_radar:
                st.plotly_chart(tech_radar, use_container_width=True)
                
                # Technology breakdown
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🤖 AI/ML Capabilities")
                    ai_breakdown = df_comp['AI_ML_Capabilities'].value_counts()
                    for capability, count in ai_breakdown.items():
                        st.info(f"**{capability}**: {count} competitors")
                
                with col2:
                    st.markdown("#### ☁️ Cloud Adoption")
                    cloud_breakdown = df_comp['Cloud_Native_Platform'].value_counts()
                    for status, count in cloud_breakdown.items():
                        color = "success" if status == "Yes" else "info" if status == "Partial" else "warning"
                        if color == "success":
                            st.success(f"**{status}**: {count} competitors")
                        elif color == "info":
                            st.info(f"**{status}**: {count} competitors")
                        else:
                            st.warning(f"**{status}**: {count} competitors")
        
        with chart_tab3:
            st.markdown("#### Digital Transformation Maturity")
            evolution_chart = create_market_evolution_analysis(df_comp)
            if evolution_chart:
                st.plotly_chart(evolution_chart, use_container_width=True)
                
                # Transformation insights
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🚀 Digital Leaders")
                    leaders = df_comp[df_comp['Digital_Transformation_Stage'] == 'Leader']
                    if not leaders.empty:
                        for _, leader in leaders.iterrows():
                            st.success(f"**{leader['Competitor_Name']}** - {leader['Technology_Initiatives']}")
                
                with col2:
                    st.markdown("#### 📈 Investment Levels")
                    avg_tech_investment = df_comp.groupby('Digital_Transformation_Stage')['Technology_Investment_Percent'].mean()
                    for stage, investment in avg_tech_investment.items():
                        st.info(f"**{stage}**: {investment:.1f}% avg tech investment")
        
        with chart_tab4:
            st.markdown("#### Strategic Competitive Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Market Dynamics")
                st.info(competitive_insights.get('market_concentration', 'N/A'))
                st.info(competitive_insights.get('geographic_reach', 'N/A'))
                st.info(competitive_insights.get('cloud_adoption', 'N/A'))
                
                # Recent acquisitions
                st.markdown("#### 🤝 Recent Acquisitions")
                recent_acquisitions = df_comp[df_comp['Recent_Acquisitions'] != 'None (Recent)'][
                    ['Competitor_Name', 'Recent_Acquisitions']
                ].head(5)
                for _, row in recent_acquisitions.iterrows():
                    st.success(f"**{row['Competitor_Name']}**: {row['Recent_Acquisitions']}")
            
            with col2:
                st.markdown("#### 🏆 Performance Leaders")
                st.info(competitive_insights.get('tech_leaders', 'N/A'))
                
                # Top performers by multiple metrics
                st.markdown("#### 📊 Multi-Metric Leaders")
                df_comp['overall_score'] = (
                    df_comp['Client_Satisfaction_Score'] * 0.3 +
                    df_comp['Technology_Investment_Percent'] * 0.3 +
                    df_comp['API_Integration_Score'] * 0.4
                )
                top_overall = df_comp.nlargest(5, 'overall_score')[
                    ['Competitor_Name', 'overall_score']
                ]
                for _, row in top_overall.iterrows():
                    st.success(f"**{row['Competitor_Name']}**: {row['overall_score']:.1f} overall score")
        
        st.markdown("---")
        
        # Detailed Analysis Table
        st.subheader("📋 Detailed Competitors Analysis")
        
        # Key columns for display
        display_columns = [
            'Competitor_Name', 'Competitor_Type', 'Assets_Under_Administration_USD_Trillions',
            'Market_Share_Percent', 'Technology_Investment_Percent', 'Client_Satisfaction_Score',
            'AI_ML_Capabilities', 'Digital_Transformation_Stage', 'Geographic_Presence'
        ]
        
        display_df = df_comp[display_columns]
        
        st.dataframe(display_df.style.format({
            'Assets_Under_Administration_USD_Trillions': '${:.1f}T',
            'Market_Share_Percent': '{:.1f}%',
            'Technology_Investment_Percent': '{:.1f}%',
            'Client_Satisfaction_Score': '{:.1f}/10'
        }), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Export Analysis
        st.subheader("📤 Export Competitive Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate comprehensive Excel report
            excel_report = generate_competitors_excel_report(df_comp, competitive_insights)
            
            st.download_button(
                label="📊 Download Complete Analysis",
                data=excel_report,
                file_name=f"Competitors_Analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            # Export raw data
            csv_data = df_comp.to_csv(index=False)
            st.download_button(
                label="📋 Download Raw Data (CSV)",
                data=csv_data,
                file_name=f"Competitors_Data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    else:
        # Show template preview
        st.subheader("📋 Template Preview")
        st.markdown("*Preview of the competitors analysis template with sample data. Upload your data to see full competitive intelligence.*")
        
        template_preview = create_competitors_template()
        
        if not template_preview.empty:
            # Show sample visualizations with template data
            st.session_state.competitors_data = template_preview  # Temporarily set for preview
            positioning_chart = create_competitive_positioning_chart(template_preview)
            tech_radar = create_technology_capability_radar(template_preview)
            
            st.markdown("#### Sample Competitive Positioning")
            if positioning_chart:
                st.plotly_chart(positioning_chart, use_container_width=True)
            
            # Sample metrics
            sample_competitors = len(template_preview)
            sample_aum = template_preview['Assets_Under_Administration_USD_Trillions'].sum()
            sample_leaders = len(template_preview[template_preview['AI_ML_Capabilities'] == 'Advanced'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sample Competitors", sample_competitors)
            with col2:
                st.metric("Sample AUM", f"${sample_aum:.1f}T")
            with col3:
                st.metric("Tech Leaders", sample_leaders)
            
            # Sample data structure
            st.markdown("#### Template Data Structure")
            st.dataframe(template_preview[['Competitor_Name', 'Assets_Under_Administration_USD_Trillions', 
                                        'Market_Share_Percent', 'AI_ML_Capabilities', 'Client_Satisfaction_Score']].head(), 
                        use_container_width=True, hide_index=True)
            
            st.session_state.competitors_data = pd.DataFrame()  # Reset after preview

with main_tab8:
    st.markdown("### 📋 Business Case Development & Management")
    st.markdown("*Comprehensive business case creation system with scoring, gap analysis, and workflow management for capital funds and offering enhancements.*")
    
    st.markdown("---")
    
    # Business Case Development Framework
    with st.expander("🏗️ Business Case Development Framework", expanded=False):
        st.markdown("""
        ### Strategic Business Case Development Process
        
        **Business Case Creation:**
        - Comprehensive template with financial metrics, strategic alignment, and feasibility assessment
        - Integration with existing workstream, P&L, and competitive data
        - Qualitative assessment with region and workstream targeting
        
        **Scoring & Gap Analysis Engine:**
        - Weighted scoring across 5 categories: Financial (30%), Strategic (25%), Feasibility (20%), Impact (15%), Resource (10%)
        - Current vs Target state gap analysis with detailed recommendations
        - Automated threshold scoring for workflow progression
        
        **Workflow Management System:**
        - **Parking Lot**: Cases scoring above threshold (70+) for initial assessment
        - **Backlog**: Approved cases ready for capital fund allocation
        - **Roadmap**: Prioritized cases with timeline for offering enhancement
        
        **Document Generation:**
        - Professional Word document generation with comprehensive business case formatting
        - Integration of supporting data from all platform modules
        - Executive summary with recommendations and next steps
        """)
    
    # Create main interface tabs
    bc_tab1, bc_tab2, bc_tab3, bc_tab4 = st.tabs([
        "📋 Data Management",
        "📊 Scoring & Analysis", 
        "🗂️ Management Pipeline",
        "📤 Export & Reports"
    ])
    
    with bc_tab1:
        st.markdown("#### Business Case Data Management")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### 📋 Download Template")
            
            # Download business case template
            template_data = create_business_case_template()
            template_buffer = io.BytesIO()
            with pd.ExcelWriter(template_buffer, engine='xlsxwriter') as writer:
                template_data.to_excel(writer, sheet_name='Business_Case_Template', index=False)
            
            st.download_button(
                label="📋 Download Business Case Template",
                data=template_buffer.getvalue(),
                file_name="Business_Case_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.info("💡 **Template includes:** Financial metrics, strategic alignment scores, implementation details, current vs target state analysis fields, plus detailed example with score calculations.")
            
            # Template contents explanation
            with st.expander("📋 What's in the Template", expanded=False):
                st.markdown("""
                ### 📊 **Template Contents**
                
                **5 Sample Business Cases** - Pre-filled examples optimized to score ≥70 for parking lot qualification
                
                **1 Detailed Example Case** - Step-by-step scoring calculation showing:
                - How each field contributes to the final score
                - Detailed comments explaining the scoring formulas
                - Example scoring: **84.4/100** ✅ **Qualifies for Parking Lot**
                
                ### 🧮 **Scoring Breakdown Example:**
                
                **Financial Score (30% weight):**
                - ROI: 60% → 10/10 points → (10 × 0.6) = 6.0
                - Payback: 20 months → 6.7/10 points → (6.7 × 0.4) = 2.7
                - **Total Financial: 8.7/10 → Weighted: 8.7 × 30% = 2.61 points**
                
                **Strategic Score (25% weight):**
                - Strategic Alignment: 9.5 → (9.5 × 0.7) = 6.65
                - Client Impact: 9.0 → (9.0 × 0.3) = 2.7  
                - **Total Strategic: 9.35/10 → Weighted: 9.35 × 25% = 2.34 points**
                
                **Feasibility Score (20% weight):**
                - Low Complexity (3) + Low Risk (2) = High Feasibility
                - **Total Feasibility: 7.5/10 → Weighted: 7.5 × 20% = 1.5 points**
                
                **Impact Score (15% weight):**
                - Process Efficiency Gap: 6 points improvement
                - Error Rate Reduction: 7.5% improvement
                - **Total Impact: 6.6/10 → Weighted: 6.6 × 15% = 0.99 points**
                
                **Resource Score (10% weight):**
                - FTE Reduction: 9 staff reduction
                - **Total Resource: 10/10 → Weighted: 10 × 10% = 1.0 points**
                
                ### 🎯 **Final Score Calculation:**
                **2.61 + 2.34 + 1.5 + 0.99 + 1.0 = 8.44/10 = 84.4/100**
                
                ✅ **Result: Qualifies for Parking Lot** (≥70 threshold)
                """)
        
        with col2:
            st.markdown("##### 📤 Upload Business Case Data")
            
            # Upload business case data
            uploaded_bc_file = st.file_uploader("Upload Business Case Data", type=['xlsx', 'csv'], key="bc_upload")
            
            if uploaded_bc_file:
                try:
                    if uploaded_bc_file.name.endswith('.csv'):
                        bc_data = pd.read_csv(uploaded_bc_file)
                    else:
                        bc_data = pd.read_excel(uploaded_bc_file)
                    
                    st.session_state.business_case_data = bc_data
                    st.success(f"✅ Loaded {len(bc_data)} business case records")
                    
                    # Display preview of loaded data
                    st.markdown("**Data Preview:**")
                    preview_cols = ['Case_Title', 'Estimated_Investment_USD', 'Expected_Annual_Savings_USD', 'ROI_Percentage']
                    available_cols = [col for col in preview_cols if col in bc_data.columns]
                    if available_cols:
                        st.dataframe(bc_data[available_cols].head(), use_container_width=True, hide_index=True)
                    else:
                        st.dataframe(bc_data.head(), use_container_width=True, hide_index=True)
                    
                except Exception as e:
                    st.error(f"Error loading business case data: {e}")
            
            else:
                st.info("📁 Upload your completed business case template to begin analysis.")
        
        # Template information section
        st.markdown("---")
        st.markdown("#### 📊 Template Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📈 Financial Data**")
            st.write("• Investment amounts")
            st.write("• Expected savings") 
            st.write("• ROI calculations")
            st.write("• Payback periods")
        
        with col2:
            st.markdown("**🎯 Strategic Metrics**")
            st.write("• Strategic alignment scores")
            st.write("• Technology complexity")
            st.write("• Implementation risk")
            st.write("• Client impact assessment")
        
        with col3:
            st.markdown("**🔄 Gap Analysis**")
            st.write("• Current state metrics")
            st.write("• Target state goals")
            st.write("• Process efficiency gaps")
            st.write("• Performance improvements")
    
    with bc_tab2:
        st.markdown("#### Scoring & Gap Analysis Dashboard")
        
        # Explanation of Scoring & Gap Analysis
        with st.expander("📊 How Scoring & Gap Analysis Works", expanded=False):
            st.markdown("""
            ### 🎯 **Business Case Scoring Methodology**
            
            Each business case is evaluated across **5 weighted categories** to generate a comprehensive score out of 100:
            
            #### **Scoring Categories:**
            
            **💰 Financial Score (30% weight)**
            - **ROI Analysis**: Return on Investment percentage (normalized to 10-point scale)
            - **Payback Period**: Shorter payback periods score higher
            - **Formula**: `(ROI Score × 0.6) + (Payback Score × 0.4)`
            
            **🎯 Strategic Alignment Score (25% weight)** 
            - **Strategic Fit**: Alignment with organizational objectives
            - **Client Impact**: Expected improvement in client satisfaction/outcomes
            - **Formula**: `(Strategic Alignment × 0.7) + (Client Impact × 0.3)`
            
            **⚙️ Implementation Feasibility Score (20% weight)**
            - **Technology Complexity**: Lower complexity scores higher
            - **Implementation Risk**: Lower risk scores higher  
            - **Formula**: `(Complexity Penalty × 0.5) + (Risk Penalty × 0.5)`
            
            **📈 Business Impact Score (15% weight)**
            - **Process Efficiency Gains**: Current vs Target efficiency improvement
            - **Error Rate Reduction**: Reduction in operational errors
            - **Formula**: `(Efficiency Gain × 0.6) + (Error Reduction × 0.4)`
            
            **👥 Resource Efficiency Score (10% weight)**
            - **FTE Optimization**: Reduction in full-time equivalent staff needed
            - **Resource Utilization**: More efficient use of existing resources
            
            ---
            
            ### 📊 **Gap Analysis Process**
            
            **Current vs Target State Analysis:**
            - **Process Efficiency Gap**: Target efficiency - Current efficiency  
            - **Error Rate Gap**: Current error rate - Target error rate
            - **Client Satisfaction Gap**: Target satisfaction - Current satisfaction
            - **FTE Efficiency Gap**: Current FTE count - Target FTE count
            
            **Gap Scoring:**
            - Larger positive gaps indicate greater improvement potential
            - Each gap includes percentage improvement calculations
            - Recommendations generated based on gap severity
            
            ---
            
            ### 🚀 **Pipeline Qualification**
            
            **Automatic Promotion Criteria:**
            - **Threshold Score**: ≥70 points qualifies for Parking Lot
            - **Strategic Threshold**: ≥70 Strategic Score recommended  
            - **Financial Threshold**: ≥70 Financial Score recommended
            
            **Pipeline Stages:**
            1. **🅿️ Parking Lot**: Qualified cases awaiting assessment
            2. **📋 Backlog**: Approved cases ready for funding
            3. **🗺️ Roadmap**: Funded cases with implementation timeline
            """)
        
        # Debug information
        with st.expander("🔍 Data Status (Debug Info)", expanded=False):
            st.write(f"Business case data empty: {st.session_state.business_case_data.empty}")
            if not st.session_state.business_case_data.empty:
                st.write(f"Number of rows: {len(st.session_state.business_case_data)}")
                st.write(f"Columns: {list(st.session_state.business_case_data.columns)}")
                st.dataframe(st.session_state.business_case_data.head(2), use_container_width=True, hide_index=True)
            else:
                st.write("No business case data found. Please upload data in the Data Management tab.")
        
        if not st.session_state.business_case_data.empty:
            # Process uploaded business case data
            all_cases = []
            
            # Add uploaded cases
            for _, row in st.session_state.business_case_data.iterrows():
                case_dict = row.to_dict()
                all_cases.append(case_dict)
            
            if all_cases:
                st.markdown(f"##### Analysis of {len(all_cases)} Business Cases")
                
                # Score all cases
                scored_cases = []
                for case in all_cases:
                    # Integrate supporting data (simplified for error prevention)
                    supporting_data = {}
                    
                    # Calculate score
                    overall_score, score_breakdown = calculate_business_case_score(case)
                    case_with_score = {
                        **case, 
                        'Total_Score': overall_score * 10,  # Convert to 100-point scale
                        'Financial_Score': score_breakdown.get('Financial', 0) * 10,
                        'Strategic_Score': score_breakdown.get('Strategic', 0) * 10,
                        'Feasibility_Score': score_breakdown.get('Feasibility', 0) * 10,
                        'Impact_Score': score_breakdown.get('Impact', 0) * 10,
                        'Resource_Score': score_breakdown.get('Resource', 0) * 10
                    }
                    scored_cases.append(case_with_score)
                
                # Create scoring dashboard
                scores_df = pd.DataFrame(scored_cases)
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_score = scores_df['Total_Score'].mean()
                    st.metric("Average Score", f"{avg_score:.1f}/100")
                
                with col2:
                    high_score = len(scores_df[scores_df['Total_Score'] >= 70])
                    st.metric("High Score Cases", f"{high_score}/{len(scores_df)}")
                
                with col3:
                    # Handle different investment column names
                    investment_col = None
                    for col_name in ['Investment_Required_M', 'investment', 'Estimated_Investment_USD', 'Investment_Required_USD']:
                        if col_name in scores_df.columns:
                            investment_col = col_name
                            break
                    
                    if investment_col:
                        total_investment = scores_df[investment_col].sum()
                        # Convert to millions if needed
                        if 'USD' in investment_col:
                            total_investment = total_investment / 1000000
                        st.metric("Total Investment", f"${total_investment:.1f}M")
                    else:
                        st.metric("Total Investment", "N/A")
                
                with col4:
                    pipeline_ready = len(scores_df[scores_df['Total_Score'] >= 70])
                    st.metric("Pipeline Ready", pipeline_ready)
                
                # Scoring visualization
                st.markdown("##### Scoring Analysis")
                
                # Create investment size column for scatter plot
                if investment_col and investment_col in scores_df.columns:
                    size_data = scores_df[investment_col]
                    if 'USD' in investment_col:
                        size_data = size_data / 1000000  # Convert to millions for sizing
                else:
                    size_data = [1] * len(scores_df)  # Default size
                
                fig_scores = px.scatter(
                    scores_df,
                    x='Financial_Score',
                    y='Strategic_Score',
                    size=size_data,
                    color='Total_Score',
                    hover_name='Case_Name' if 'Case_Name' in scores_df.columns else None,
                    hover_data=['Feasibility_Score', 'Impact_Score', 'Resource_Score'],
                    title="Business Case Scoring Matrix",
                    labels={
                        'Financial_Score': 'Financial Score',
                        'Strategic_Score': 'Strategic Score',
                        'Total_Score': 'Total Score'
                    },
                    color_continuous_scale='RdYlGn'
                )
                
                fig_scores.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Strategic Threshold")
                fig_scores.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="Financial Threshold")
                
                st.plotly_chart(fig_scores, use_container_width=True)
                
                # Business Case Promotion System
                st.markdown("---")
                st.markdown("##### 🚀 Promote Business Cases to Pipeline")
                
                # Filter cases that qualify for parking lot (score >= 70)
                qualified_cases = scores_df[scores_df['Total_Score'] >= 70]
                
                if len(qualified_cases) > 0:
                    st.success(f"🎯 {len(qualified_cases)} business cases qualify for the pipeline (score ≥ 70)")
                    
                    # Check which cases are not already in pipeline stages
                    existing_parking_ids = [case.get('Case_ID', case.get('Case_Name', '')) for case in st.session_state.parking_lot]
                    existing_backlog_ids = [case.get('Case_ID', case.get('Case_Name', '')) for case in st.session_state.backlog]  
                    existing_roadmap_ids = [case.get('Case_ID', case.get('Case_Name', '')) for case in st.session_state.roadmap]
                    
                    new_qualified_cases = []
                    for _, case in qualified_cases.iterrows():
                        case_id = case.get('Case_ID', case.get('Case_Title', case.get('Case_Name', 'Unknown')))
                        if (case_id not in existing_parking_ids and 
                            case_id not in existing_backlog_ids and 
                            case_id not in existing_roadmap_ids):
                            new_qualified_cases.append(case)
                    
                    if len(new_qualified_cases) > 0:
                        st.info(f"📋 {len(new_qualified_cases)} new cases ready for promotion to Parking Lot")
                        
                        promote_col1, promote_col2 = st.columns([2, 1])
                        
                        with promote_col1:
                            st.markdown("**Cases Ready for Promotion:**")
                            for case in new_qualified_cases:
                                case_name = case.get('Case_Title', case.get('Case_Name', 'Unknown Case'))
                                st.write(f"• **{case_name}** - Score: {case.get('Total_Score', 0):.1f}/100")
                        
                        with promote_col2:
                            if st.button("🚀 Promote All to Parking Lot", type="primary"):
                                for case in new_qualified_cases:
                                    # Create parking lot item
                                    parking_item = {
                                        'Case_ID': case.get('Case_ID', case.get('Case_Title', 'Unknown')),
                                        'Case_Name': case.get('Case_Title', case.get('Case_Name', 'Unknown Case')),
                                        'Total_Score': case.get('Total_Score', 0),
                                        'Investment_Required_M': case.get('Investment_Required_M', 
                                                                        case.get('investment', 
                                                                               case.get('Estimated_Investment_USD', 0))),
                                        'Primary_Workstream': case.get('Primary_Workstream', 'N/A'),
                                        'Target_Region': case.get('Target_Region', case.get('Region', 'Global')),
                                        'ROI_Percentage': case.get('ROI_Percentage', 0),
                                        'Implementation_Timeline': case.get('Implementation_Duration_Months', 'TBD'),
                                        'Status': 'Parking Lot',
                                        'Date_Added': datetime.now().strftime('%Y-%m-%d %H:%M')
                                    }
                                    
                                    st.session_state.parking_lot.append(parking_item)
                                
                                st.success(f"✅ Promoted {len(new_qualified_cases)} cases to Parking Lot!")
                                st.rerun()
                    else:
                        st.info("✅ All qualified cases are already in the pipeline stages.")
                else:
                    st.warning("⚠️ No business cases currently qualify for the pipeline (need score ≥ 70)")
                
                # Gap analysis for top cases
                st.markdown("##### Gap Analysis - Top Performing Cases")
                top_cases = scores_df.nlargest(5, 'Total_Score')
                
                for _, case in top_cases.iterrows():
                    # Handle different case name field names
                    case_name = case.get('Case_Name', case.get('Case_Title', case.get('name', 'Unnamed Case')))
                    with st.expander(f"📊 {case_name} - Score: {case['Total_Score']:.1f}/100"):
                        gap_analysis = create_gap_analysis(case.to_dict())
                        
                        # Score breakdown
                        score_col1, score_col2 = st.columns(2)
                        with score_col1:
                            st.markdown("**Score Breakdown:**")
                            st.write(f"• Financial: {case['Financial_Score']:.1f}/100")
                            st.write(f"• Strategic: {case['Strategic_Score']:.1f}/100") 
                            st.write(f"• Feasibility: {case['Feasibility_Score']:.1f}/100")
                            st.write(f"• Impact: {case['Impact_Score']:.1f}/100")
                            st.write(f"• Resource: {case['Resource_Score']:.1f}/100")
                        
                        with score_col2:
                            st.markdown("**Gap Analysis:**")
                            if gap_analysis:
                                for gap_type, gap_data in gap_analysis.items():
                                    if isinstance(gap_data, dict) and 'gap' in gap_data:
                                        st.write(f"⚠️ {gap_type}: {gap_data['gap']:.1f} improvement needed")
                            
                            st.markdown("**Recommendations:**")
                            st.write("💡 Focus on highest-impact gaps first")
                            st.write("💡 Consider phased implementation approach")
                            st.write("💡 Monitor progress with defined KPIs")
        else:
            st.info("📁 Upload business case data in the 'Data Management' tab to see comprehensive scoring analysis.")
    
    with bc_tab3:
        st.markdown("#### Business Case Management Pipeline")
        
        # Initialize pipeline states
        parking_lot_cases = [case for case in st.session_state.parking_lot if case.get('Total_Score', 0) >= 70]
        backlog_cases = st.session_state.backlog
        roadmap_cases = st.session_state.roadmap
        
        # Pipeline overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 🅿️ Parking Lot")
            st.info(f"{len(parking_lot_cases)} cases awaiting assessment")
            
            if parking_lot_cases:
                for case in parking_lot_cases:
                    with st.expander(f"{case.get('Case_Name', 'Unknown Case')} - {case.get('Total_Score', 0):.1f}/100"):
                        # Handle different investment field names
                        investment = case.get('Investment_Required_M', case.get('investment', case.get('Estimated_Investment_USD', 0)))
                        if isinstance(investment, (int, float)) and investment > 1000000:
                            investment = investment / 1000000  # Convert to millions
                        st.write(f"**Investment:** ${investment:.1f}M")
                        st.write(f"**Workstream:** {case.get('Primary_Workstream', 'N/A')}")
                        st.write(f"**Region:** {case.get('Target_Region', 'N/A')}")
                        
                        if st.button(f"Move to Backlog", key=f"move_backlog_{case.get('Case_Name', '')}"): 
                            st.session_state.backlog.append(case)
                            st.session_state.parking_lot.remove(case)
                            st.rerun()
        
        with col2:
            st.markdown("##### 📋 Backlog")
            st.warning(f"{len(backlog_cases)} cases ready for capital allocation")
            
            if backlog_cases:
                for case in backlog_cases:
                    with st.expander(f"{case.get('Case_Name', 'Unknown Case')}"):
                        # Handle different investment field names
                        investment = case.get('Investment_Required_M', case.get('investment', case.get('Estimated_Investment_USD', 0)))
                        if isinstance(investment, (int, float)) and investment > 1000000:
                            investment = investment / 1000000  # Convert to millions
                        st.write(f"**Investment:** ${investment:.1f}M")
                        st.write(f"**Score:** {case.get('Total_Score', 0):.1f}/100")
                        
                        if st.button(f"Add to Roadmap", key=f"move_roadmap_{case.get('Case_Name', '')}"):
                            st.session_state.roadmap.append(case)
                            st.session_state.backlog.remove(case)
                            st.rerun()
        
        with col3:
            st.markdown("##### 🗺️ Roadmap")
            st.success(f"{len(roadmap_cases)} cases in delivery pipeline")
            
            if roadmap_cases:
                for case in roadmap_cases:
                    with st.expander(f"{case.get('Case_Name', 'Unknown Case')}"):
                        st.write(f"**Timeline:** {case.get('Implementation_Timeline', 'TBD')}")
                        # Handle different investment field names
                        investment = case.get('Investment_Required_M', case.get('investment', case.get('Estimated_Investment_USD', 0)))
                        if isinstance(investment, (int, float)) and investment > 1000000:
                            investment = investment / 1000000  # Convert to millions
                        st.write(f"**Investment:** ${investment:.1f}M")
                        st.write(f"**Score:** {case.get('Total_Score', 0):.1f}/100")
        
        # Pipeline analytics
        st.markdown("---")
        st.markdown("##### 📈 Pipeline Analytics")
        
        # Calculate total pipeline investment with flexible field names
        total_pipeline_investment = 0
        for case in parking_lot_cases + backlog_cases + roadmap_cases:
            investment = case.get('Investment_Required_M', case.get('investment', case.get('Estimated_Investment_USD', 0)))
            if isinstance(investment, (int, float)):
                if investment > 1000000:  # Convert USD to millions
                    investment = investment / 1000000
                total_pipeline_investment += investment
        
        pipeline_col1, pipeline_col2, pipeline_col3 = st.columns(3)
        with pipeline_col1:
            st.metric("Total Pipeline Value", f"${total_pipeline_investment:.1f}M")
        with pipeline_col2:
            total_cases = len(parking_lot_cases) + len(backlog_cases) + len(roadmap_cases)
            st.metric("Total Pipeline Cases", total_cases)
        with pipeline_col3:
            if total_cases > 0:
                avg_investment = total_pipeline_investment / total_cases
                st.metric("Avg Case Investment", f"${avg_investment:.1f}M")
    
    with bc_tab4:
        st.markdown("#### Export & Document Generation")
        
        if not st.session_state.business_case_data.empty:
            st.markdown("##### Generate Professional Documents")
            
            # Select business case for document generation
            all_case_names = []
            all_cases_dict = {}
            
            for _, row in st.session_state.business_case_data.iterrows():
                name = row.get('Case_Title', row.get('Case_Name', f"Case_{len(all_case_names)+1}"))
                all_case_names.append(name)
                all_cases_dict[name] = row.to_dict()
            
            selected_case = st.selectbox("Select Business Case for Document Generation", all_case_names)
            
            if selected_case and selected_case in all_cases_dict:
                case_data = all_cases_dict[selected_case]
                
                # Add scoring if not present
                if 'Total_Score' not in case_data:
                    supporting_data = {}  # Simplified to prevent errors
                    overall_score, score_breakdown = calculate_business_case_score(case_data)
                    case_data.update({
                        'Total_Score': overall_score * 10,  # Convert to 100-point scale
                        'Financial_Score': score_breakdown.get('Financial', 0) * 10,
                        'Strategic_Score': score_breakdown.get('Strategic', 0) * 10,
                        'Feasibility_Score': score_breakdown.get('Feasibility', 0) * 10,
                        'Impact_Score': score_breakdown.get('Impact', 0) * 10,
                        'Resource_Score': score_breakdown.get('Resource', 0) * 10
                    })
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Generate Word document
                    if st.button("📄 Generate Word Document", type="primary"):
                        try:
                            # Create a simple text version for now
                            # Get case title with fallbacks
                            doc_title = case_data.get('Case_Name', case_data.get('Case_Title', case_data.get('name', 'N/A')))
                            
                            # Get investment with unit conversion
                            doc_investment = case_data.get('Investment_Required_M', case_data.get('investment', case_data.get('Estimated_Investment_USD', 0)))
                            if isinstance(doc_investment, (int, float)) and doc_investment > 1000000:
                                doc_investment = doc_investment / 1000000
                            
                            word_content = f"""
BUSINESS CASE DOCUMENT

Title: {doc_title}
Investment Required: ${doc_investment:.1f}M
Implementation Timeline: {case_data.get('Implementation_Timeline', 'TBD')}
Primary Workstream: {case_data.get('Primary_Workstream', 'N/A')}
Target Region: {case_data.get('Target_Region', 'N/A')}

DESCRIPTION:
{case_data.get('Description', 'No description provided')}

STRATEGIC RATIONALE:
{case_data.get('Strategic_Rationale', 'No rationale provided')}

SCORING SUMMARY:
Total Score: {case_data.get('Total_Score', 0):.1f}/100
- Financial Score: {case_data.get('Financial_Score', 0):.1f}/100
- Strategic Score: {case_data.get('Strategic_Score', 0):.1f}/100
- Feasibility Score: {case_data.get('Feasibility_Score', 0):.1f}/100
- Impact Score: {case_data.get('Impact_Score', 0):.1f}/100
- Resource Score: {case_data.get('Resource_Score', 0):.1f}/100

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: Iluvalcar 2.0 Business Case Development System
"""
                            
                            st.download_button(
                                label="📥 Download Business Case Document (Text)",
                                data=word_content,
                                file_name=f"Business_Case_{selected_case.replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                            
                        except Exception as e:
                            st.error(f"Error generating document: {e}")
                            st.info("Word document generation will be implemented in a future update. Text format available above.")
                
                with col2:
                    # Export pipeline summary
                    if st.button("📊 Export Pipeline Report"):
                        all_pipeline_cases = st.session_state.parking_lot + st.session_state.backlog + st.session_state.roadmap
                        
                        if all_pipeline_cases:
                            pipeline_df = pd.DataFrame(all_pipeline_cases)
                            
                            pipeline_buffer = io.BytesIO()
                            with pd.ExcelWriter(pipeline_buffer, engine='xlsxwriter') as writer:
                                pipeline_df.to_excel(writer, sheet_name='Pipeline_Summary', index=False)
                            
                            st.download_button(
                                label="📥 Download Pipeline Report",
                                data=pipeline_buffer.getvalue(),
                                file_name=f"Business_Case_Pipeline_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                
                # Case preview
                st.markdown("##### Selected Business Case Preview")
                st.json(case_data)
        
        else:
            st.info("📁 Upload business case data to generate professional documents and reports.")

# Footer
st.markdown("---")
st.markdown("**🚀 Iluvalcar 2.0** - Fund Administration Workstream Management Platform")