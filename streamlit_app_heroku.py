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

# Page Configuration
st.set_page_config(
    page_title="Fund Administration Platform",
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
        
        # Portfolio Valuation Workstreams
        {'id': 'val_001', 'name': 'Exchange Listed Securities', 'category': 'Portfolio Valuation', 'complexity': 5, 'automation': 8, 'risk': 3, 'investment': 1.5, 'completion': 90, 'priority': 'Low', 'description': 'Automated valuation of exchange-traded securities'},
        {'id': 'val_002', 'name': 'OTC Securities Valuation', 'category': 'Portfolio Valuation', 'complexity': 8, 'automation': 4, 'risk': 8, 'investment': 3.8, 'completion': 55, 'priority': 'High', 'description': 'Over-the-counter securities pricing and valuation'},
        
        # Trade Capture Workstreams
        {'id': 'trade_001', 'name': 'Cash Trade Processing', 'category': 'Trade Capture', 'complexity': 5, 'automation': 7, 'risk': 4, 'investment': 2.0, 'completion': 75, 'priority': 'Medium', 'description': 'Cash transaction capture and processing'},
        {'id': 'trade_002', 'name': 'Derivative Trade Capture', 'category': 'Trade Capture', 'complexity': 9, 'automation': 5, 'risk': 9, 'investment': 4.5, 'completion': 40, 'priority': 'High', 'description': 'Complex derivative instrument trade processing'},
        
        # Reconciliation Workstreams
        {'id': 'recon_001', 'name': 'Stock Reconciliation', 'category': 'Reconciliation', 'complexity': 6, 'automation': 5, 'risk': 6, 'investment': 2.2, 'completion': 70, 'priority': 'Medium', 'description': 'Stock position reconciliation with custodians'},
        {'id': 'recon_002', 'name': 'Cash Reconciliation', 'category': 'Reconciliation', 'complexity': 5, 'automation': 6, 'risk': 5, 'investment': 1.9, 'completion': 80, 'priority': 'Medium', 'description': 'Cash balance reconciliation across accounts'},
    ]

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

def create_dashboard():
    """Create main dashboard"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Investment", f"${df['investment'].sum():.1f}M")
        st.metric("Average Completion", f"{df['completion'].mean():.1f}%")
    
    with col2:
        st.metric("High Risk Items", len(df[df['risk'] >= 7]))
        st.metric("Low Automation", len(df[df['automation'] <= 4]))
    
    # Matrix visualization
    st.subheader("Workstream Analysis")
    fig = create_workstream_matrix()
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.subheader("Workstream Summary")
    st.dataframe(df[['name', 'category', 'risk', 'automation', 'investment', 'completion', 'priority']])

def create_management_interface():
    """Create workstream management interface"""
    st.subheader("Workstream Management")
    
    # Add new workstream
    with st.expander("Add New Workstream"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Workstream Name")
            category = st.selectbox("Category", ['NAV Calculation', 'Portfolio Valuation', 'Trade Capture', 'Reconciliation'])
            priority = st.selectbox("Priority", ['Low', 'Medium', 'High', 'Critical'])
        
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
                'description': f'Added on {datetime.now().strftime("%Y-%m-%d")}'
            }
            st.session_state.workstream_data.append(new_workstream)
            st.success("Workstream added successfully!")

def main():
    """Main application"""
    st.title("🏗️ Fund Administration Platform")
    st.markdown("### Operational Workstreams Management")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📊 Dashboard", "⚙️ Management"])
    
    with tab1:
        create_dashboard()
    
    with tab2:
        create_management_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("**Fund Administration Platform** - Streamlined for Heroku Deployment")

if __name__ == "__main__":
    main() 