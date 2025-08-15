"""
Data validation utilities
"""

import pandas as pd
import streamlit as st
from typing import List, Optional, Dict, Any
from config.constants import ERROR_MESSAGES


class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_required_columns(df: pd.DataFrame, required_columns: List[str], 
                                dataset_name: str = "dataset") -> bool:
        """Validate that required columns exist in dataframe"""
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns in {dataset_name}: {', '.join(missing_columns)}")
            return False
            
        return True

    @staticmethod
    def validate_numeric_columns(df: pd.DataFrame, numeric_columns: List[str]) -> bool:
        """Validate that specified columns contain numeric data"""
        errors = []
        
        for col in numeric_columns:
            if col in df.columns:
                non_numeric = df[col].apply(lambda x: pd.isna(pd.to_numeric(x, errors='coerce'))).sum()
                if non_numeric > 0:
                    errors.append(f"Column '{col}' contains {non_numeric} non-numeric values")
        
        if errors:
            for error in errors:
                st.warning(error)
            return False
            
        return True

    @staticmethod
    def validate_date_columns(df: pd.DataFrame, date_columns: List[str]) -> bool:
        """Validate that specified columns contain valid dates"""
        errors = []
        
        for col in date_columns:
            if col in df.columns:
                try:
                    pd.to_datetime(df[col], errors='coerce')
                except:
                    errors.append(f"Column '{col}' contains invalid date values")
        
        if errors:
            for error in errors:
                st.error(error)
            return False
            
        return True

    @staticmethod
    def validate_data_completeness(df: pd.DataFrame, min_rows: int = 1) -> bool:
        """Validate minimum data completeness"""
        if len(df) < min_rows:
            st.error(f"Dataset contains {len(df)} rows, minimum required: {min_rows}")
            return False
            
        return True

    @staticmethod
    def validate_business_case_data(case_data: Dict[str, Any]) -> List[str]:
        """Validate business case data structure"""
        errors = []
        
        required_fields = ['Case_Name', 'Description', 'Investment_Required_M']
        for field in required_fields:
            if not case_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate investment amount
        investment = case_data.get('Investment_Required_M', 0)
        if not isinstance(investment, (int, float)) or investment <= 0:
            errors.append("Investment amount must be a positive number")
        
        # Validate scores
        score_fields = ['Financial_Score', 'Strategic_Score', 'Feasibility_Score', 
                       'Impact_Score', 'Resource_Score']
        for field in score_fields:
            score = case_data.get(field, 0)
            if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                errors.append(f"{field} must be between 0 and 100")
        
        return errors


class InputSanitizer:
    """Input sanitization utilities"""
    
    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 255) -> str:
        """Sanitize string input"""
        if not isinstance(input_str, str):
            return str(input_str)
            
        # Remove potentially harmful characters
        sanitized = input_str.strip()[:max_length]
        
        # Remove HTML tags and potential script injections
        import re
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        import re
        
        # Remove or replace unsafe characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        
        # Limit length
        if len(sanitized) > 255:
            name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
            sanitized = f"{name[:251]}.{ext}" if ext else sanitized[:255]
        
        return sanitized

    @staticmethod
    def validate_numeric_range(value: float, min_val: float = None, 
                             max_val: float = None, field_name: str = "Value") -> bool:
        """Validate numeric value is within acceptable range"""
        if min_val is not None and value < min_val:
            st.error(f"{field_name} must be at least {min_val}")
            return False
            
        if max_val is not None and value > max_val:
            st.error(f"{field_name} must be at most {max_val}")
            return False
            
        return True