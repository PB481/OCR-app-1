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

# Conditional imports for optional features
try:
    import altair as alt
    ALTAIR_AVAILABLE = True
except ImportError:
    ALTAIR_AVAILABLE = False

try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    from scipy.optimize import minimize
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Fund Administration Platform - Complete Edition",
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

# Initialize other session state variables
if 'capital_project_data' not in st.session_state:
    st.session_state.capital_project_data = pd.DataFrame()
if 'pl_data' not in st.session_state:
    st.session_state.pl_data = pd.DataFrame()
if 'competitors_data' not in st.session_state:
    st.session_state.competitors_data = pd.DataFrame()
if 'business_cases' not in st.session_state:
    st.session_state.business_cases = []

def get_category_color(category):
    """Get color for category"""
    colors = {
        'NAV Calculation': '#1f77b4',
        'Portfolio Valuation': '#ff7f0e',
        'Trade Capture': '#2ca02c',
        'Reconciliation': '#d62728',
        'Corporate Actions': '#9467bd',
        'Expense Management': '#8c564b',
        'Reporting': '#e377c2'
    }
    return colors.get(category, '#7f7f7f')

def create_workstream_matrix():
    """Create workstream matrix visualization"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    fig = px.scatter(
        df, 
        x='risk', 
        y='automation', 
        size='investment',
        color='category',
        hover_data=['name', 'completion', 'priority'],
        title='Workstream Risk vs Automation Matrix',
        labels={'risk': 'Risk Level', 'automation': 'Automation Level', 'investment': 'Investment (M)'}
    )
    
    fig.update_layout(
        width=800,
        height=600,
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10])
    )
    
    return fig

def create_3d_visualization():
    """Create 3D visualization if scipy is available"""
    if not SCIPY_AVAILABLE:
        st.warning("3D visualization requires scipy. Using 2D alternative.")
        return create_workstream_matrix()
    
    df = pd.DataFrame(st.session_state.workstream_data)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df['risk'],
        y=df['automation'],
        z=df['complexity'],
        mode='markers',
        marker=dict(
            size=df['investment'] * 2,
            color=df['completion'],
            colorscale='Viridis',
            opacity=0.8
        ),
        text=df['name'],
        hovertemplate='<b>%{text}</b><br>' +
                      'Risk: %{x}<br>' +
                      'Automation: %{y}<br>' +
                      'Complexity: %{z}<br>' +
                      '<extra></extra>'
    )])
    
    fig.update_layout(
        title='3D Workstream Analysis (Risk vs Automation vs Complexity)',
        scene=dict(
            xaxis_title='Risk Level',
            yaxis_title='Automation Level',
            zaxis_title='Complexity Level'
        ),
        width=800,
        height=600
    )
    
    return fig

def create_network_analysis():
    """Create network analysis if networkx is available"""
    if not NETWORKX_AVAILABLE:
        st.warning("Network analysis requires networkx. Skipping this feature.")
        return None
    
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Create network graph
    G = nx.Graph()
    
    # Add nodes
    for _, row in df.iterrows():
        G.add_node(row['name'], 
                  category=row['category'],
                  risk=row['risk'],
                  automation=row['automation'],
                  investment=row['investment'])
    
    # Add edges based on category relationships
    categories = df['category'].unique()
    for category in categories:
        category_nodes = df[df['category'] == category]['name'].tolist()
        for i in range(len(category_nodes)):
            for j in range(i+1, len(category_nodes)):
                G.add_edge(category_nodes[i], category_nodes[j])
    
    # Create network visualization
    pos = nx.spring_layout(G)
    
    fig = go.Figure()
    
    # Add edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'))
    
    # Add nodes
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        
        # Get node attributes
        node_data = G.nodes[node]
        node_size.append(node_data.get('investment', 1) * 10)
        node_color.append(node_data.get('risk', 5))
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            size=node_size,
            color=node_color,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Risk Level")
        )))
    
    fig.update_layout(
        title='Workstream Network Analysis',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def create_advanced_analytics():
    """Create advanced analytics dashboard"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    st.subheader("📊 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category analysis
        st.write("**Investment by Category**")
        category_investment = df.groupby('category')['investment'].sum().sort_values(ascending=False)
        fig_cat = px.bar(
            x=category_investment.index,
            y=category_investment.values,
            title="Total Investment by Category",
            labels={'x': 'Category', 'y': 'Investment (M)'}
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Risk distribution
        st.write("**Risk Distribution**")
        fig_risk = px.histogram(
            df, x='risk', nbins=10,
            title="Risk Level Distribution",
            labels={'risk': 'Risk Level', 'count': 'Number of Workstreams'}
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Correlation analysis
    st.write("**Correlation Analysis**")
    numeric_cols = ['complexity', 'automation', 'risk', 'investment', 'completion']
    correlation_matrix = df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        title="Feature Correlation Matrix",
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

def create_management_interface():
    """Create comprehensive workstream management interface"""
    st.subheader("⚙️ Workstream Management")
    
    # Add new workstream
    with st.expander("➕ Add New Workstream"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Workstream Name")
            category = st.selectbox("Category", ['NAV Calculation', 'Portfolio Valuation', 'Trade Capture', 'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting'])
            priority = st.selectbox("Priority", ['Low', 'Medium', 'High', 'Critical'])
            description = st.text_area("Description")
        
        with col2:
            complexity = st.slider("Complexity", 1, 10, 5)
            automation = st.slider("Automation", 1, 10, 5)
            risk = st.slider("Risk", 1, 10, 5)
            investment = st.number_input("Investment (M)", min_value=0.0, value=1.0, step=0.1)
            completion = st.slider("Completion %", 0, 100, 50)
        
        if st.button("Add Workstream"):
            new_workstream = {
                'id': f'ws_{len(st.session_state.workstream_data) + 1:03d}',
                'name': name,
                'category': category,
                'complexity': complexity,
                'automation': automation,
                'risk': risk,
                'investment': investment,
                'completion': completion,
                'priority': priority,
                'description': description or f'Added on {datetime.now().strftime("%Y-%m-%d")}'
            }
            st.session_state.workstream_data.append(new_workstream)
            st.success("Workstream added successfully!")
    
    # Edit existing workstreams
    with st.expander("✏️ Edit Workstreams"):
        df = pd.DataFrame(st.session_state.workstream_data)
        if not df.empty:
            selected_workstream = st.selectbox("Select workstream to edit", df['name'].tolist())
            
            if selected_workstream:
                workstream = df[df['name'] == selected_workstream].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Name", value=workstream['name'])
                    new_category = st.selectbox("Category", ['NAV Calculation', 'Portfolio Valuation', 'Trade Capture', 'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting'], index=['NAV Calculation', 'Portfolio Valuation', 'Trade Capture', 'Reconciliation', 'Corporate Actions', 'Expense Management', 'Reporting'].index(workstream['category']))
                    new_priority = st.selectbox("Priority", ['Low', 'Medium', 'High', 'Critical'], index=['Low', 'Medium', 'High', 'Critical'].index(workstream['priority']))
                
                with col2:
                    new_completion = st.slider("Completion %", 0, 100, int(workstream['completion']))
                    new_investment = st.number_input("Investment (M)", min_value=0.0, value=float(workstream['investment']), step=0.1)
                
                if st.button("Update Workstream"):
                    # Update the workstream in session state
                    for i, ws in enumerate(st.session_state.workstream_data):
                        if ws['name'] == selected_workstream:
                            st.session_state.workstream_data[i].update({
                                'name': new_name,
                                'category': new_category,
                                'priority': new_priority,
                                'completion': new_completion,
                                'investment': new_investment
                            })
                            break
                    st.success("Workstream updated successfully!")

def create_dashboard():
    """Create comprehensive dashboard"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Investment", f"${df['investment'].sum():.1f}M")
    with col2:
        st.metric("Average Completion", f"{df['completion'].mean():.1f}%")
    with col3:
        st.metric("High Risk Items", len(df[df['risk'] >= 7]))
    with col4:
        st.metric("Low Automation", len(df[df['automation'] <= 4]))
    
    # Matrix visualization
    st.subheader("🎯 Workstream Analysis")
    fig = create_workstream_matrix()
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.subheader("📋 Workstream Summary")
    display_df = df[['name', 'category', 'risk', 'automation', 'investment', 'completion', 'priority']].copy()
    st.dataframe(display_df, use_container_width=True)

def main():
    """Main application"""
    st.title("🏗️ Fund Administration Platform - Complete Edition")
    st.markdown("### Comprehensive Operational Workstreams Management")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "🎯 Advanced Analytics", 
        "🌐 3D Analysis",
        "🕸️ Network Analysis",
        "⚙️ Management"
    ])
    
    with tab1:
        create_dashboard()
    
    with tab2:
        create_advanced_analytics()
    
    with tab3:
        st.subheader("🌐 3D Workstream Analysis")
        fig_3d = create_3d_visualization()
        st.plotly_chart(fig_3d, use_container_width=True)
    
    with tab4:
        st.subheader("🕸️ Network Analysis")
        fig_network = create_network_analysis()
        if fig_network:
            st.plotly_chart(fig_network, use_container_width=True)
    
    with tab5:
        create_management_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("**Fund Administration Platform - Complete Edition** - All features included")
    
    # Feature availability info
    with st.expander("ℹ️ Feature Availability"):
        st.write("**Available Features:**")
        st.write("✅ Basic Dashboard")
        st.write("✅ Workstream Management")
        st.write("✅ Matrix Visualization")
        st.write("✅ Advanced Analytics")
        
        if SCIPY_AVAILABLE:
            st.write("✅ 3D Visualizations")
        else:
            st.write("❌ 3D Visualizations (scipy not available)")
        
        if NETWORKX_AVAILABLE:
            st.write("✅ Network Analysis")
        else:
            st.write("❌ Network Analysis (networkx not available)")
        
        if SEABORN_AVAILABLE:
            st.write("✅ Advanced Plotting")
        else:
            st.write("❌ Advanced Plotting (seaborn not available)")

if __name__ == "__main__":
    main() 