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