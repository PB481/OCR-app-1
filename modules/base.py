"""
Base module with common functionality for all feature modules
"""

import streamlit as st
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

from utils.data_loader import DataLoader, SessionStateManager
from utils.validators import DataValidator, InputSanitizer
from utils.report_generator import ReportGenerator
from config.settings import PAGE_CONFIG
from config.constants import ERROR_MESSAGES, SUCCESS_MESSAGES


class BaseModule(ABC):
    """Base class for all feature modules"""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.data_loader = DataLoader()
        self.validator = DataValidator()
        self.sanitizer = InputSanitizer()
        self.report_generator = ReportGenerator()
        
    @abstractmethod
    def render(self):
        """Render the module UI - must be implemented by subclasses"""
        pass
    
    def show_header(self, title: str, description: str = ""):
        """Display module header"""
        st.title(title)
        if description:
            st.markdown(description)
        st.markdown("---")
    
    def show_error(self, message: str):
        """Display error message"""
        st.error(f"🚨 {message}")
    
    def show_success(self, message: str):
        """Display success message"""
        st.success(f"✅ {message}")
    
    def show_warning(self, message: str):
        """Display warning message"""
        st.warning(f"⚠️ {message}")
    
    def show_info(self, message: str):
        """Display info message"""
        st.info(f"ℹ️ {message}")
    
    def create_file_uploader(self, label: str, file_types: List[str] = None, 
                           help_text: str = None) -> Optional[Any]:
        """Create standardized file uploader"""
        if file_types is None:
            file_types = ["csv", "xlsx"]
            
        return st.file_uploader(
            label=label,
            type=file_types,
            help=help_text
        )
    
    def create_download_section(self, reports: Dict[str, bytes], 
                              section_title: str = "📥 Download Reports"):
        """Create standardized download section"""
        if not reports:
            return
            
        st.subheader(section_title)
        
        cols = st.columns(len(reports))
        for i, (name, data) in enumerate(reports.items()):
            with cols[i]:
                file_ext = "xlsx" if "excel" in name.lower() else "html"
                mime_type = ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
                           if file_ext == "xlsx" else "text/html")
                
                filename = f"{self.sanitizer.sanitize_filename(name)}.{file_ext}"
                
                st.download_button(
                    label=f"Download {name}",
                    data=data,
                    file_name=filename,
                    mime=mime_type
                )
    
    def process_uploaded_data(self, uploaded_file, required_columns: List[str] = None) -> pd.DataFrame:
        """Process uploaded file with validation"""
        if uploaded_file is None:
            return pd.DataFrame()
        
        # Load data
        df = self.data_loader.load_uploaded_file(uploaded_file)
        
        if df.empty:
            return df
        
        # Clean column names
        df.columns = [self.data_loader.clean_column_name(col) for col in df.columns]
        df.columns = self.data_loader.handle_duplicate_columns(df.columns.tolist())
        
        # Validate required columns
        if required_columns:
            if not self.validator.validate_required_columns(df, required_columns, self.module_name):
                return pd.DataFrame()
        
        # Convert financial columns
        df = self.data_loader.convert_financial_columns(df)
        
        self.show_success(SUCCESS_MESSAGES["data_processed"])
        return df
    
    def create_metrics_display(self, metrics: Dict[str, Any], columns: int = 3):
        """Create standardized metrics display"""
        if not metrics:
            return
            
        # Split metrics into rows
        metric_items = list(metrics.items())
        
        for i in range(0, len(metric_items), columns):
            cols = st.columns(columns)
            
            for j, (label, value) in enumerate(metric_items[i:i+columns]):
                if j < len(cols):
                    with cols[j]:
                        st.metric(label=label, value=value)
    
    def create_sidebar_filters(self, df: pd.DataFrame, filter_columns: Dict[str, str]) -> Dict[str, Any]:
        """Create standardized sidebar filters"""
        if df.empty:
            return {}
            
        st.sidebar.header(f"Filter {self.module_name}")
        filters = {}
        
        for col_name, display_name in filter_columns.items():
            if col_name in df.columns:
                unique_values = ['All'] + sorted(df[col_name].dropna().unique().tolist())
                filters[col_name] = st.sidebar.selectbox(display_name, unique_values)
            else:
                st.sidebar.warning(f"Column '{col_name}' not found")
                filters[col_name] = 'All'
        
        return filters
    
    def apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to dataframe"""
        if df.empty or not filters:
            return df
            
        filtered_df = df.copy()
        
        for col_name, selected_value in filters.items():
            if selected_value != 'All' and col_name in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col_name] == selected_value]
        
        return filtered_df
    
    def handle_empty_data(self, df: pd.DataFrame, message: str = None) -> bool:
        """Handle empty dataframe case"""
        if df.empty:
            if message is None:
                message = f"No data available for {self.module_name}. Please upload a file."
            self.show_warning(message)
            return True
        return False
    
    def create_data_preview(self, df: pd.DataFrame, title: str = "Data Preview", max_rows: int = 100):
        """Create standardized data preview"""
        if self.handle_empty_data(df):
            return
            
        st.subheader(title)
        
        # Show data info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            memory_usage = df.memory_usage(deep=True).sum() / 1024**2
            st.metric("Memory Usage", f"{memory_usage:.1f} MB")
        
        # Show data
        display_df = df.head(max_rows) if len(df) > max_rows else df
        st.dataframe(display_df, use_container_width=True)
        
        if len(df) > max_rows:
            st.info(f"Showing first {max_rows} rows of {len(df)} total rows")