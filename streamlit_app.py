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

def create_workstream_periodic_table():
    """Create a periodic table style visualization of workstreams using Plotly"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Create grid positions based on category and complexity
    category_rows = {
        'NAV Calculation': 7,
        'Portfolio Valuation': 6, 
        'Trade Capture': 5,
        'Reconciliation': 4,
        'Corporate Actions': 3,
        'Expense Management': 2,
        'Reporting': 1
    }
    
    # Prepare data for plotting
    x_positions = []
    y_positions = []
    colors = []
    sizes = []
    text_labels = []
    hover_texts = []
    
    for _, row in df.iterrows():
        y_pos = category_rows.get(row['category'], 1)
        x_pos = int(row['complexity'])
        
        x_positions.append(x_pos)
        y_positions.append(y_pos)
        colors.append(get_category_color(row['category']))
        
        # Size based on investment amount
        sizes.append(max(20, min(80, row['investment'] * 15)))
        
        # Text labels for elements
        text_labels.append(f"<b>{row['name'][:15]}{'...' if len(row['name']) > 15 else ''}</b><br>Auto: {row['automation']}/10<br>{row['completion']}%")
        
        # Hover text with full details
        priority_symbol = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(row['priority'], '⚪')
        hover_texts.append(f"""<b>{row['name']}</b><br>
Category: {row['category']}<br>
Complexity: {row['complexity']}/10<br>
Automation: {row['automation']}/10<br>
Risk: {row['risk']}/10<br>
Investment: ${row['investment']:.1f}M<br>
Completion: {row['completion']}%<br>
Priority: {priority_symbol} {row['priority']}<br><br>
{row['description'][:100]}{'...' if len(row['description']) > 100 else ''}""")
    
    # Create the scatter plot
    fig = go.Figure()
    
    # Add workstream elements
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=3, color='white'),
            opacity=0.8
        ),
        text=text_labels,
        textposition="middle center",
        textfont=dict(size=10, color='white'),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_texts,
        showlegend=False
    ))
    
    # Customize layout to look like periodic table
    fig.update_layout(
        title="Fund Administration Workstreams - Periodic Table Layout",
        title_x=0.5,
        xaxis=dict(
            title="Complexity Level →",
            range=[0.5, 10.5],
            tickmode='linear',
            tick0=1,
            dtick=1,
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title="Categories",
            range=[0.5, 7.5],
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7],
            ticktext=['Reporting', 'Expense Mgmt', 'Corp Actions', 'Reconciliation', 'Trade Capture', 'Portfolio Val', 'NAV Calc'],
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1
        ),
        plot_bgcolor='rgba(240, 248, 255, 0.8)',
        paper_bgcolor='white',
        width=900,
        height=600,
        margin=dict(l=100, r=50, t=80, b=80)
    )
    
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

def create_3d_analysis():
    """Create 3D analysis visualization"""
    df = pd.DataFrame(st.session_state.workstream_data)
    
    # Create 3D scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=df['complexity'],
        y=df['automation'],
        z=df['risk'],
        mode='markers+text',
        marker=dict(
            size=df['investment'] * 3,
            color=[get_category_color(cat) for cat in df['category']],
            opacity=0.8,
            line=dict(width=2, color='DarkSlateGray')
        ),
        text=df['name'],
        textposition="top center",
        hovertemplate='<b>%{text}</b><br>' +
                      'Complexity: %{x}<br>' +
                      'Automation: %{y}<br>' +
                      'Risk: %{z}<br>' +
                      'Investment: $%{marker.size:.1f}M<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="3D Workstream Analysis: Complexity vs Automation vs Risk",
        scene=dict(
            xaxis_title="Complexity Level (1-10)",
            yaxis_title="Automation Level (1-10)", 
            zaxis_title="Risk Level (1-10)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=600,
        margin=dict(r=20, b=10, l=10, t=40)
    )
    
    return fig

def workstream_management_interface():
    """Create interface for managing workstreams"""
    st.subheader("🛠️ Manage Workstreams - Add/Edit/Delete")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add New", "✏️ Edit Existing", "🗑️ Delete"])
    
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
    st.markdown("### Fund Administration Workstreams - Periodic Table Layout")
    st.markdown("*Interactive visualization showing workstreams positioned by complexity and category. Hover over elements for detailed information.*")
    
    # Display the periodic table using Plotly
    periodic_table_fig = create_workstream_periodic_table()
    st.plotly_chart(periodic_table_fig, use_container_width=True)
    
    # Display legend and guide
    legend_info = create_legend_info()
    st.markdown(legend_info)
    
    # Category color guide
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🔴 **NAV Calculation**")
        st.markdown("🟦 **Portfolio Valuation**")
    with col2:
        st.markdown("🔵 **Trade Capture**")
        st.markdown("🟢 **Reconciliation**")
    with col3:
        st.markdown("🟡 **Corporate Actions**")
        st.markdown("🟣 **Expense Management**")
    with col4:
        st.markdown("🟫 **Reporting**")
    
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
    st.markdown("### 3D Workstream Analysis")
    st.markdown("*Interactive 3D visualization showing the relationship between complexity, automation level, and risk. Marker size represents investment amount.*")
    
    # Create and display 3D plot
    fig_3d = create_3d_analysis()
    st.plotly_chart(fig_3d, use_container_width=True)
    
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