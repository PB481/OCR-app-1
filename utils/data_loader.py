"""
Utility functions for data loading and processing
"""

import streamlit as st
import pandas as pd
import json
import io
import re
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

from config.constants import CURRENT_YEAR, CURRENT_MONTH, ERROR_MESSAGES, SUCCESS_MESSAGES
from config.settings import DATA_CONFIG, UPLOAD_CONFIG


class DataLoader:
    """Centralized data loading and processing class"""
    
    @staticmethod
    @st.cache_data(ttl=DATA_CONFIG["cache_timeout"])
    def load_json_data(file_path: str) -> List[Dict[str, Any]]:
        """Load data from JSON file with caching"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error(f"Data file not found: {file_path}")
            return []
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format in {file_path}: {e}")
            return []
        except Exception as e:
            st.error(f"Error loading data from {file_path}: {e}")
            return []

    @staticmethod
    def validate_upload(uploaded_file) -> bool:
        """Validate uploaded file"""
        if uploaded_file is None:
            return False
            
        file_extension = Path(uploaded_file.name).suffix.lower()
        if file_extension not in UPLOAD_CONFIG["allowed_extensions"]:
            st.error(f"Invalid file type. Allowed: {', '.join(UPLOAD_CONFIG['allowed_extensions'])}")
            return False
            
        if uploaded_file.size > UPLOAD_CONFIG["max_file_size"] * 1024 * 1024:
            st.error(f"File too large. Maximum size: {UPLOAD_CONFIG['max_file_size']}MB")
            return False
            
        return True

    @staticmethod
    @st.cache_data(ttl=DATA_CONFIG["cache_timeout"])
    def load_uploaded_file(uploaded_file: io.BytesIO) -> pd.DataFrame:
        """Load data from uploaded file with caching and validation"""
        if not DataLoader.validate_upload(uploaded_file):
            return pd.DataFrame()
            
        try:
            file_extension = Path(uploaded_file.name).suffix.lower()
            
            if file_extension == '.csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(uploaded_file)
            else:
                st.error(ERROR_MESSAGES["invalid_format"])
                return pd.DataFrame()
                
            st.success(SUCCESS_MESSAGES["file_uploaded"])
            return df
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def clean_column_name(col_name: str) -> str:
        """Clean and standardize column names"""
        col_name = str(col_name).strip()
        col_name = col_name.replace(' ', '_').replace('+', '_')
        col_name = col_name.replace('.', '_').replace('-', '_')
        col_name = '_'.join(filter(None, col_name.split('_')))
        col_name = col_name.upper()
        
        # Common corrections
        corrections = {
            'PROJEC_TID': 'PROJECT_ID',
            'INI_MATIVE_PROGRAM': 'INITIATIVE_PROGRAM',
            'ALL_PRIOR_YEARS_A': 'ALL_PRIOR_YEARS_ACTUALS',
            'C_URRENT_EAC': 'CURRENT_EAC',
            'QE_RUN_RATE': 'QE_RUN_RATE',
            'RATE_1': 'RATE_SUPPLEMENTARY'
        }
        
        return corrections.get(col_name, col_name)

    @staticmethod
    def handle_duplicate_columns(columns: List[str]) -> List[str]:
        """Handle duplicate column names by adding suffixes"""
        seen = {}
        result = []
        
        for col in columns:
            original_col = col
            count = seen.get(col, 0)
            if count > 0:
                col = f"{col}_{count}"
            result.append(col)
            seen[original_col] = count + 1
            
        return result

    @staticmethod
    def convert_financial_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Convert financial columns to numeric format"""
        try:
            financial_pattern = DATA_CONFIG["numeric_columns_pattern"]
            financial_cols = [col for col in df.columns 
                            if pd.Series([col]).str.contains(financial_pattern, regex=True).any()]
            
            for col in financial_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace(',', '').str.strip()
                    df[col] = df[col].replace('', '0')
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    
            return df
            
        except Exception as e:
            st.error(f"Error converting financial columns: {str(e)}")
            return df

    @staticmethod
    def get_monthly_columns(df: pd.DataFrame, year: int = CURRENT_YEAR) -> Dict[str, List[str]]:
        """Extract monthly columns by type (Actuals, Forecasts, Capital Plan)"""
        monthly_pattern = re.compile(rf'^{year}_\d{{2}}_([AF]|CP)$')
        
        columns = {
            'actuals': [],
            'forecasts': [],
            'capital_plan': []
        }
        
        for col in df.columns:
            match = monthly_pattern.match(col)
            if match:
                col_type = match.group(1)
                if col_type == 'A':
                    columns['actuals'].append(col)
                elif col_type == 'F':
                    columns['forecasts'].append(col)
                elif col_type == 'CP':
                    columns['capital_plan'].append(col)
                    
        return columns


class SessionStateManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables"""
        from config.settings import SESSION_KEYS
        
        # Initialize data containers
        for key in SESSION_KEYS.values():
            if isinstance(key, dict):
                for subkey in key.values():
                    if subkey not in st.session_state:
                        st.session_state[subkey] = ""
            else:
                if key not in st.session_state:
                    if 'data' in key:
                        st.session_state[key] = pd.DataFrame()
                    elif 'cases' in key:
                        st.session_state[key] = []
                    else:
                        st.session_state[key] = None
        
        # Initialize flags
        flag_keys = ['pl_template_downloaded', 'competitors_template_downloaded', 'reports_ready']
        for key in flag_keys:
            if key not in st.session_state:
                st.session_state[key] = False

    @staticmethod
    def load_workstream_data():
        """Load workstream data into session state"""
        if 'workstream_data' not in st.session_state:
            workstream_data = DataLoader.load_json_data('data/workstream_data.json')
            st.session_state.workstream_data = workstream_data