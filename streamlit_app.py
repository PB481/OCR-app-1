import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import json
from datetime import datetime, timedelta

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
        
        # Download template
        st.markdown("#### 📥 Download Excel Template")
        template_data = pd.DataFrame([
            {
                'id': 'template_001',
                'name': 'Example Workstream Name',
                'category': 'NAV Calculation',
                'complexity': 5,
                'automation': 5,
                'risk': 5,
                'investment': 2.0,
                'completion': 50,
                'priority': 'Medium',
                'description': 'Enter your workstream description here'
            }
        ])
        
        # Create Excel file in memory
        from io import BytesIO
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            template_data.to_excel(writer, sheet_name='Workstreams', index=False)
        
        st.download_button(
            label="📥 Download Excel Template",
            data=excel_buffer.getvalue(),
            file_name="workstream_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_template"
        )
        
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

# Main App Layout
st.title("🏗️ Operational Workstreams - Fund Administration Periodic Table")

st.markdown("""
### Interactive Workstream Management & 3D Analysis Platform

This application provides a comprehensive view of fund administration operational workstreams with interactive management capabilities and real-time 3D analysis.
""")

# Create tabs for different sections
main_tab1, main_tab2, main_tab3 = st.tabs([
    "🧪 Periodic Table View",
    "📊 3D Analysis", 
    "⚙️ Manage Workstreams"
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
    
    # 3D Analysis selector
    analysis_type = st.selectbox(
        "Select 3D Analysis Type:",
        [
            "🎯 Strategic Analysis (Complexity × Automation × Risk)",
            "💰 Investment Performance (Investment × Performance × Timeline)", 
            "📊 ROI Analysis (Investment × Completion × ROI)",
            "🔮 Scenario Planning (Current vs Future Projections)",
            "🌐 Network Dependencies (Workstream Interdependencies)"
        ],
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

# Footer
st.markdown("---")
st.markdown("**🚀 Iluvalcar 2.0** - Fund Administration Workstream Management Platform")