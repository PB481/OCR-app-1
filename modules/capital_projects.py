"""
Capital Projects Analysis Module
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import re
from datetime import datetime
from typing import Dict, Any, Optional, List

from .base import BaseModule
from config.constants import CURRENT_YEAR, CURRENT_MONTH, CURRENT_YEAR_STR, CAPITAL_PROJECT_HEADERS
from config.settings import CHART_CONFIG, REPORT_CONFIG


class CapitalProjects(BaseModule):
    """Capital Projects Analysis and Management"""
    
    def __init__(self):
        super().__init__("Capital Projects")
        
    def render(self):
        """Render the Capital Projects module"""
        self.show_header(
            "💰 Capital Project Portfolio Dashboard",
            "Interactive overview of capital projects with financial tracking, trend monitoring, and variance analysis."
        )
        
        # File upload section
        uploaded_file = self.create_file_uploader(
            "Upload your Capital Project CSV or Excel file",
            file_types=["csv", "xlsx"],
            help_text="File should contain project data with financial columns"
        )
        
        if uploaded_file is not None:
            # Reset reports flag
            st.session_state.reports_ready = False
            
            # Process data
            df = self.process_capital_project_data(uploaded_file)
            
            if not self.handle_empty_data(df):
                self.render_dashboard(df)
        else:
            self.show_info("Upload your Capital Project CSV or Excel file to get started!")
    
    @st.cache_data(ttl=3600)
    def process_capital_project_data(_self, uploaded_file) -> pd.DataFrame:
        """Process capital project data with caching"""
        try:
            df = _self.process_uploaded_data(uploaded_file)
            
            if df.empty:
                return df
                
            # Add calculated columns
            df = _self._calculate_derived_metrics(df)
            
            return df
            
        except Exception as e:
            _self.show_error(f"Error processing capital project data: {str(e)}")
            return pd.DataFrame()
    
    def _calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for capital projects"""
        try:
            # Get monthly columns
            monthly_cols = self.data_loader.get_monthly_columns(df, CURRENT_YEAR)
            
            # Calculate totals
            df[f'TOTAL_{CURRENT_YEAR}_ACTUALS'] = df[monthly_cols['actuals']].sum(axis=1) if monthly_cols['actuals'] else 0
            df[f'TOTAL_{CURRENT_YEAR}_FORECASTS'] = df[monthly_cols['forecasts']].sum(axis=1) if monthly_cols['forecasts'] else 0
            df[f'TOTAL_{CURRENT_YEAR}_CAPITAL_PLAN'] = df[monthly_cols['capital_plan']].sum(axis=1) if monthly_cols['capital_plan'] else 0
            
            # Calculate YTD actuals
            ytd_actual_cols = [col for col in monthly_cols['actuals'] 
                             if int(col.split('_')[1]) <= CURRENT_MONTH]
            df['SUM_ACTUAL_SPEND_YTD'] = df[ytd_actual_cols].sum(axis=1) if ytd_actual_cols else 0
            
            # Calculate total actuals to date
            if 'ALL_PRIOR_YEARS_ACTUALS' in df.columns:
                df['TOTAL_ACTUALS_TO_DATE'] = df['ALL_PRIOR_YEARS_ACTUALS'] + df[f'TOTAL_{CURRENT_YEAR}_ACTUALS']
            else:
                df['TOTAL_ACTUALS_TO_DATE'] = df[f'TOTAL_{CURRENT_YEAR}_ACTUALS']
                self.show_warning("Column 'ALL_PRIOR_YEARS_ACTUALS' not found.")
            
            # Calculate run rates and averages
            df['RUN_RATE_PER_MONTH'] = (df[f'TOTAL_{CURRENT_YEAR}_ACTUALS'] + df[f'TOTAL_{CURRENT_YEAR}_FORECASTS']) / 12
            
            num_actual_months = len(ytd_actual_cols) if ytd_actual_cols else 1
            num_forecast_months = len(monthly_cols['forecasts']) if monthly_cols['forecasts'] else 1
            
            df['AVG_ACTUAL_SPEND'] = df['SUM_ACTUAL_SPEND_YTD'] / num_actual_months
            df['AVG_FORECAST_SPEND'] = df[f'TOTAL_{CURRENT_YEAR}_FORECASTS'] / num_forecast_months
            
            # Calculate variances
            if 'BUSINESS_ALLOCATION' in df.columns:
                df['CAPITAL_VARIANCE'] = df['BUSINESS_ALLOCATION'] - df[f'TOTAL_{CURRENT_YEAR}_FORECASTS']
                df['CAPITAL_UNDERSPEND'] = df['CAPITAL_VARIANCE'].apply(lambda x: x if x > 0 else 0)
                df['CAPITAL_OVERSPEND'] = df['CAPITAL_VARIANCE'].apply(lambda x: abs(x) if x < 0 else 0)
            else:
                df['CAPITAL_VARIANCE'] = 0
                df['CAPITAL_UNDERSPEND'] = 0
                df['CAPITAL_OVERSPEND'] = 0
                self.show_warning("Column 'BUSINESS_ALLOCATION' not found.")
            
            df['NET_REALLOCATION_AMOUNT'] = df['CAPITAL_UNDERSPEND'] - df['CAPITAL_OVERSPEND']
            df['TOTAL_SPEND_VARIANCE'] = df[f'TOTAL_{CURRENT_YEAR}_ACTUALS'] - df[f'TOTAL_{CURRENT_YEAR}_FORECASTS']
            
            # Calculate monthly variance scores
            monthly_variance_cols = []
            for i in range(1, 13):
                actual_col = f'{CURRENT_YEAR}_{i:02d}_A'
                forecast_col = f'{CURRENT_YEAR}_{i:02d}_F'
                if actual_col in df.columns and forecast_col in df.columns:
                    variance_col = f'{CURRENT_YEAR}_{i:02d}_AF_VARIANCE'
                    df[variance_col] = df[actual_col] - df[forecast_col]
                    monthly_variance_cols.append(variance_col)
            
            df['AVERAGE_MONTHLY_SPREAD_SCORE'] = df[monthly_variance_cols].abs().mean(axis=1) if monthly_variance_cols else 0
            
            return df
            
        except Exception as e:
            self.show_error(f"Error calculating derived metrics: {str(e)}")
            return df
    
    def render_dashboard(self, df: pd.DataFrame):
        """Render the main dashboard"""
        # Sidebar filters
        filters = self.create_sidebar_filters(df, {
            "PORTFOLIO_OBS_LEVEL1": "Select Portfolio Level",
            "SUB_PORTFOLIO_OBS_LEVEL2": "Select Sub-Portfolio Level", 
            "PROJECT_MANAGER": "Select Project Manager",
            "BRS_CLASSIFICATION": "Select BRS Classification",
            "FUND_DECISION": "Select Fund Decision"
        })
        
        # Apply filters
        filtered_df = self.apply_filters(df, filters)
        
        if self.handle_empty_data(filtered_df, "No projects match the selected filters."):
            return
        
        # Key metrics
        self._render_key_metrics(filtered_df)
        
        # Project details table
        self._render_project_details(filtered_df)
        
        # Monthly trends
        self._render_monthly_trends(filtered_df)
        
        # Variance analysis
        self._render_variance_analysis(filtered_df)
        
        # Budget impact
        self._render_budget_impact(filtered_df)
        
        # Individual project view
        self._render_individual_project(filtered_df)
        
        # Project performance
        self._render_project_performance(filtered_df)
        
        # Report generation
        self._render_report_generation(filtered_df)
    
    def _render_key_metrics(self, df: pd.DataFrame):
        """Render key metrics section"""
        st.subheader("Key Metrics Overview")
        
        metrics = {
            "Number of Projects": len(df),
            "Sum Actual Spend (YTD)": f"${df['SUM_ACTUAL_SPEND_YTD'].sum():,.2f}",
            "Sum Of Forecasted Numbers": f"${df[f'TOTAL_{CURRENT_YEAR}_FORECASTS'].sum():,.2f}",
            "Average Run Rate / Month": f"${df['RUN_RATE_PER_MONTH'].mean():,.2f}",
            "Total Potential Underspend": f"${df['CAPITAL_UNDERSPEND'].sum():,.2f}",
            "Total Potential Overspend": f"${df['CAPITAL_OVERSPEND'].sum():,.2f}",
            "Net Reallocation Amount": f"${df['NET_REALLOCATION_AMOUNT'].sum():,.2f}"
        }
        
        self.create_metrics_display(metrics, columns=4)
        st.markdown("---")
    
    def _render_project_details(self, df: pd.DataFrame):
        """Render project details table"""
        st.subheader("Project Details")
        
        display_cols = [col for col in CAPITAL_PROJECT_HEADERS if col in df.columns]
        display_cols.extend([
            f'TOTAL_{CURRENT_YEAR}_ACTUALS',
            f'TOTAL_{CURRENT_YEAR}_FORECASTS', 
            f'TOTAL_{CURRENT_YEAR}_CAPITAL_PLAN',
            'CAPITAL_UNDERSPEND',
            'CAPITAL_OVERSPEND',
            'AVERAGE_MONTHLY_SPREAD_SCORE'
        ])
        
        display_cols = [col for col in display_cols if col in df.columns]
        
        # Format financial columns
        financial_format = {col: "${:,.2f}" for col in display_cols 
                          if any(keyword in col for keyword in ['ACTUALS', 'FORECASTS', 'PLAN', 'ALLOCATION', 'EAC', 'SPEND', 'AMOUNT', 'SCORE'])}
        
        st.dataframe(
            df[display_cols].style.format(financial_format),
            use_container_width=True,
            hide_index=True
        )
        st.markdown("---")
    
    def _render_monthly_trends(self, df: pd.DataFrame):
        """Render monthly trends chart"""
        st.subheader(f"{CURRENT_YEAR} Monthly Spend Trends")
        
        try:
            # Get monthly data
            monthly_cols = self.data_loader.get_monthly_columns(df, CURRENT_YEAR)
            
            # Prepare data for chart
            trend_data = []
            
            # Add actuals (up to current month)
            for col in monthly_cols['actuals']:
                month_num = int(col.split('_')[1])
                if month_num <= CURRENT_MONTH:
                    trend_data.append({
                        'Month': f'{CURRENT_YEAR}_{month_num:02d}',
                        'Amount': df[col].sum(),
                        'Type': 'Actuals'
                    })
            
            # Add forecasts (from current month + 1)
            for col in monthly_cols['forecasts']:
                month_num = int(col.split('_')[1])
                if month_num > CURRENT_MONTH:
                    trend_data.append({
                        'Month': f'{CURRENT_YEAR}_{month_num:02d}',
                        'Amount': df[col].sum(),
                        'Type': 'Forecasts'
                    })
            
            if trend_data:
                trend_df = pd.DataFrame(trend_data)
                
                # Create chart
                fig = px.line(
                    trend_df,
                    x='Month',
                    y='Amount',
                    color='Type',
                    title=f'Monthly Capital Trends for {CURRENT_YEAR}',
                    markers=True,
                    height=CHART_CONFIG["default_height"]
                )
                
                fig.update_layout(template=CHART_CONFIG["template"])
                st.plotly_chart(fig, use_container_width=True)
            else:
                self.show_warning("No monthly trend data available")
                
        except Exception as e:
            self.show_error(f"Error creating monthly trends chart: {str(e)}")
        
        st.markdown("---")
    
    def _render_variance_analysis(self, df: pd.DataFrame):
        """Render variance analysis section"""
        st.subheader("🔎 Project Spend Variance Analysis")
        st.markdown("These charts compare spend for each project, sorted by greatest variance between actual and forecasted spend.")
        
        # Project count slider
        num_projects = st.slider(
            "Select number of projects to display:",
            5, min(50, len(df)), min(15, len(df)), 5,
            key="variance_projects"
        )
        
        # Get top variance projects
        variance_df = df.nlargest(num_projects, 'TOTAL_SPEND_VARIANCE')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Total Spend: Actuals vs. Forecast**")
            self._create_variance_chart(variance_df, 
                                      [f'TOTAL_{CURRENT_YEAR}_ACTUALS', f'TOTAL_{CURRENT_YEAR}_FORECASTS'],
                                      ['Total Actuals', 'Total Forecasts'])
        
        with col2:
            st.write("**Average Monthly Spend**")  
            self._create_variance_chart(variance_df,
                                      ['AVG_ACTUAL_SPEND', 'AVG_FORECAST_SPEND'],
                                      ['Avg Actuals (YTD)', 'Avg Forecasts (Annual)'])
        
        # Comments section
        st.text_area("Add comments for the Spend Variance section:", key="comment_variance")
        st.markdown("---")
    
    def _create_variance_chart(self, df: pd.DataFrame, value_cols: List[str], labels: List[str]):
        """Create variance comparison chart"""
        try:
            if 'PROJECT_NAME' not in df.columns:
                st.warning("PROJECT_NAME column not found")
                return
                
            melted_df = df.melt(
                id_vars='PROJECT_NAME',
                value_vars=value_cols,
                var_name='Spend Type',
                value_name='Amount'
            )
            
            # Replace column names with labels
            label_map = dict(zip(value_cols, labels))
            melted_df['Spend Type'] = melted_df['Spend Type'].map(label_map)
            
            fig = px.bar(
                melted_df,
                y='PROJECT_NAME',
                x='Amount', 
                color='Spend Type',
                barmode='group',
                orientation='h',
                height=max(400, len(df) * 35)
            )
            
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                template=CHART_CONFIG["template"]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating variance chart: {str(e)}")
    
    def _render_budget_impact(self, df: pd.DataFrame):
        """Render budget impact and reallocation section"""
        st.subheader("🎯 Budget Impact and Reallocation Insights")
        
        overspend_df = df[df['CAPITAL_OVERSPEND'] > 0].nlargest(5, 'CAPITAL_OVERSPEND')
        underspend_df = df[df['CAPITAL_UNDERSPEND'] > 0].nlargest(5, 'CAPITAL_UNDERSPEND')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Projects with Largest Forecasted Overspend")
            if not overspend_df.empty:
                display_cols = ['PROJECT_NAME', 'BUSINESS_ALLOCATION', f'TOTAL_{CURRENT_YEAR}_FORECASTS', 'CAPITAL_OVERSPEND']
                display_cols = [col for col in display_cols if col in overspend_df.columns]
                
                currency_format = {col: "${:,.2f}" for col in display_cols[1:]}
                st.dataframe(
                    overspend_df[display_cols].style.format(currency_format),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                self.show_info("No projects are currently forecasting an overspend.")
        
        with col2:
            st.write("#### Projects with Largest Potential Underspend")
            if not underspend_df.empty:
                display_cols = ['PROJECT_NAME', 'BUSINESS_ALLOCATION', f'TOTAL_{CURRENT_YEAR}_FORECASTS', 'CAPITAL_UNDERSPEND']
                display_cols = [col for col in display_cols if col in underspend_df.columns]
                
                currency_format = {col: "${:,.2f}" for col in display_cols[1:]}
                st.dataframe(
                    underspend_df[display_cols].style.format(currency_format),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                self.show_info("No projects are currently forecasting an underspend.")
        
        # Reallocation suggestion
        if not overspend_df.empty and not underspend_df.empty:
            total_underspend = df['CAPITAL_UNDERSPEND'].sum()
            total_overspend = df['CAPITAL_OVERSPEND'].sum()
            st.success(f"**Reallocation Suggestion:** Total potential underspend of **${total_underspend:,.2f}** could cover total potential overspend of **${total_overspend:,.2f}**.")
        
        st.text_area("Add comments for the Budget Impact section:", key="comment_impact")
        st.markdown("---")
    
    def _render_individual_project(self, df: pd.DataFrame):
        """Render individual project detailed view"""
        st.subheader("Individual Project Financials")
        
        if 'PROJECT_NAME' not in df.columns:
            self.show_warning("PROJECT_NAME column not found")
            return
            
        project_names = ['Select a Project'] + sorted(df['PROJECT_NAME'].dropna().unique())
        selected_project = st.selectbox("Select a project for detailed monthly view:", project_names)
        
        if selected_project != 'Select a Project':
            project_data = df[df['PROJECT_NAME'] == selected_project].iloc[0]
            
            st.write(f"### Details for: {project_data['PROJECT_NAME']}")
            
            # Project metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Business Allocation", f"${project_data.get('BUSINESS_ALLOCATION', 0):,.2f}")
            with col2:
                st.metric("Current EAC", f"${project_data.get('CURRENT_EAC', 0):,.2f}")
            with col3:
                st.metric("All Prior Years Actuals", f"${project_data.get('ALL_PRIOR_YEARS_ACTUALS', 0):,.2f}")
            
            # Monthly breakdown
            self._render_project_monthly_breakdown(project_data)
        else:
            self.show_info("Select a project from the dropdown to see its detailed monthly financials.")
        
        st.markdown("---")
    
    def _render_project_monthly_breakdown(self, project_data: pd.Series):
        """Render monthly breakdown for a specific project"""
        st.write(f"#### {CURRENT_YEAR} Monthly Breakdown:")
        
        try:
            # Prepare monthly data
            monthly_data = {'Month': [f"{CURRENT_YEAR}_{i:02d}" for i in range(1, 13)]}
            
            monthly_types = {'_A': 'Actuals', '_F': 'Forecasts', '_CP': 'Capital Plan'}
            for suffix, name in monthly_types.items():
                monthly_values = []
                for i in range(1, 13):
                    col_name = f'{CURRENT_YEAR}_{i:02d}{suffix}'
                    monthly_values.append(project_data.get(col_name, 0))
                monthly_data[name] = monthly_values
            
            monthly_df = pd.DataFrame(monthly_data)
            
            # Display table
            currency_format = {col: "${:,.2f}" for col in ['Actuals', 'Forecasts', 'Capital Plan']}
            st.dataframe(
                monthly_df.style.format(currency_format),
                use_container_width=True,
                hide_index=True
            )
            
            # Create chart
            melted_df = monthly_df.melt(id_vars=['Month'], var_name='Type', value_name='Amount')
            
            fig = px.bar(
                melted_df,
                x='Month',
                y='Amount',
                color='Type',
                barmode='group',
                title=f'Monthly Financials for {project_data["PROJECT_NAME"]}',
                height=400
            )
            
            fig.update_layout(template=CHART_CONFIG["template"])
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            self.show_error(f"Error creating monthly breakdown: {str(e)}")
    
    def _render_project_performance(self, df: pd.DataFrame):
        """Render project performance ranking"""
        st.subheader("🏆 Project Performance")
        
        if 'AVERAGE_MONTHLY_SPREAD_SCORE' not in df.columns:
            self.show_warning("Performance score column not found")
            return
            
        self.show_info("**Performance Ranking:** Based on 'Average Monthly Spread Score' - the average monthly difference between actual vs. forecasted spend. **Lower scores are better**.")
        
        performance_df = df.sort_values('AVERAGE_MONTHLY_SPREAD_SCORE')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Top 5 Best Behaving Projects (Lowest Avg. Monthly Spread)")
            top_5 = performance_df.head(5)[['PROJECT_NAME', 'AVERAGE_MONTHLY_SPREAD_SCORE']]
            st.dataframe(
                top_5.style.format({'AVERAGE_MONTHLY_SPREAD_SCORE': "${:,.2f}"}),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.write("#### Bottom 5 Worst Behaving Projects (Highest Avg. Monthly Spread)")
            bottom_5 = performance_df.tail(5).sort_values('AVERAGE_MONTHLY_SPREAD_SCORE', ascending=False)
            bottom_5 = bottom_5[['PROJECT_NAME', 'AVERAGE_MONTHLY_SPREAD_SCORE']]
            st.dataframe(
                bottom_5.style.format({'AVERAGE_MONTHLY_SPREAD_SCORE': "${:,.2f}"}),
                use_container_width=True,
                hide_index=True
            )
        
        st.text_area("Add comments for the Bottom 5 Projects:", key="comment_bottom5")
        st.markdown("---")
    
    def _render_report_generation(self, df: pd.DataFrame):
        """Render report generation section"""
        st.subheader("Generate Professional Reports")
        st.markdown("Add your comments in the sections above, then click the button below to prepare your downloadable reports.")
        
        if st.button("Prepare Reports for Download"):
            st.session_state.reports_ready = True
        
        if st.session_state.get('reports_ready', False):
            try:
                # Generate reports
                reports = self._generate_reports(df)
                
                if reports:
                    self.create_download_section(reports, "📥 Download Capital Project Reports")
                    
            except Exception as e:
                self.show_error(f"Error generating reports: {str(e)}")
    
    def _generate_reports(self, df: pd.DataFrame) -> Dict[str, bytes]:
        """Generate downloadable reports"""
        reports = {}
        
        try:
            # Prepare data for reports
            metrics = {
                "Number of Projects": len(df),
                "Sum Actual Spend (YTD)": df['SUM_ACTUAL_SPEND_YTD'].sum(),
                "Sum Of Forecasted Numbers": df[f'TOTAL_{CURRENT_YEAR}_FORECASTS'].sum(),
                "Avg Run Rate / Month": df['RUN_RATE_PER_MONTH'].mean(),
                "Total Potential Underspend": df['CAPITAL_UNDERSPEND'].sum(),
                "Total Potential Overspend": df['CAPITAL_OVERSPEND'].sum(),
                "Net Reallocation": df['NET_REALLOCATION_AMOUNT'].sum()
            }
            
            # Prepare data sheets
            data_sheets = {
                'Project_Details': df,
                'Over_Spend_Projects': df[df['CAPITAL_OVERSPEND'] > 0],
                'Under_Spend_Projects': df[df['CAPITAL_UNDERSPEND'] > 0],
                'Performance_Rankings': df.sort_values('AVERAGE_MONTHLY_SPREAD_SCORE')
            }
            
            # Generate Excel report
            excel_report = self.report_generator.generate_excel_report(
                data_sheets,
                f"capital_project_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                metadata=metrics
            )
            
            if excel_report:
                reports["Capital Project Excel Report"] = excel_report
            
            # Generate HTML report (simplified version)
            html_sections = {
                "Executive Summary": self._create_html_summary(metrics),
                "Key Findings": self._create_html_findings(df)
            }
            
            html_report = self.report_generator.generate_html_report(
                "Capital Project Portfolio Report",
                html_sections
            )
            
            if html_report:
                reports["Capital Project HTML Report"] = html_report.encode('utf-8')
            
            return reports
            
        except Exception as e:
            self.show_error(f"Error generating reports: {str(e)}")
            return {}
    
    def _create_html_summary(self, metrics: Dict[str, Any]) -> str:
        """Create HTML summary section"""
        summary_html = "<h3>Portfolio Overview</h3>"
        summary_html += "<ul>"
        
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                if 'Sum' in key or 'Total' in key or 'Avg' in key or 'Net' in key:
                    formatted_value = f"${value:,.2f}"
                else:
                    formatted_value = f"{value:,}"
            else:
                formatted_value = str(value)
            
            summary_html += f"<li><strong>{key}:</strong> {formatted_value}</li>"
        
        summary_html += "</ul>"
        return summary_html
    
    def _create_html_findings(self, df: pd.DataFrame) -> str:
        """Create HTML findings section"""
        findings_html = "<h3>Key Findings</h3>"
        findings_html += "<ul>"
        
        # Top overspend project
        if not df[df['CAPITAL_OVERSPEND'] > 0].empty:
            top_overspend = df.loc[df['CAPITAL_OVERSPEND'].idxmax()]
            findings_html += f"<li>Highest overspend risk: {top_overspend['PROJECT_NAME']} (${top_overspend['CAPITAL_OVERSPEND']:,.2f})</li>"
        
        # Top underspend project
        if not df[df['CAPITAL_UNDERSPEND'] > 0].empty:
            top_underspend = df.loc[df['CAPITAL_UNDERSPEND'].idxmax()]
            findings_html += f"<li>Highest reallocation opportunity: {top_underspend['PROJECT_NAME']} (${top_underspend['CAPITAL_UNDERSPEND']:,.2f})</li>"
        
        # Performance insights
        if 'AVERAGE_MONTHLY_SPREAD_SCORE' in df.columns:
            best_performer = df.loc[df['AVERAGE_MONTHLY_SPREAD_SCORE'].idxmin()]
            worst_performer = df.loc[df['AVERAGE_MONTHLY_SPREAD_SCORE'].idxmax()]
            
            findings_html += f"<li>Best performing project: {best_performer['PROJECT_NAME']} (Score: ${best_performer['AVERAGE_MONTHLY_SPREAD_SCORE']:,.2f})</li>"
            findings_html += f"<li>Most volatile project: {worst_performer['PROJECT_NAME']} (Score: ${worst_performer['AVERAGE_MONTHLY_SPREAD_SCORE']:,.2f})</li>"
        
        findings_html += "</ul>"
        return findings_html