"""
Error handling utilities for the Fund Administration Platform
"""

import streamlit as st
import logging
import traceback
from typing import Any, Callable, Optional
from functools import wraps
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AppError(Exception):
    """Custom exception for application-specific errors"""
    def __init__(self, message: str, error_type: str = "general"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

def handle_streamlit_error(func: Callable) -> Callable:
    """Decorator to handle errors in Streamlit functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:
            st.error(f"Application Error ({e.error_type}): {e.message}")
            logger.error(f"AppError in {func.__name__}: {e.message}")
        except ValueError as e:
            st.error(f"Data validation error: {str(e)}")
            logger.error(f"ValueError in {func.__name__}: {str(e)}")
        except FileNotFoundError as e:
            st.error(f"File not found: {str(e)}")
            logger.error(f"FileNotFoundError in {func.__name__}: {str(e)}")
        except PermissionError as e:
            st.error(f"Permission denied: {str(e)}")
            logger.error(f"PermissionError in {func.__name__}: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
        return None
    return wrapper

def validate_data_quality(df, required_columns: list = None) -> bool:
    """Validate data quality and return True if valid"""
    try:
        if df.empty:
            raise AppError("DataFrame is empty", "data_quality")
        
        if required_columns:
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise AppError(f"Missing required columns: {missing_cols}", "data_quality")
        
        # Check for null values in critical columns
        null_counts = df.isnull().sum()
        if null_counts.sum() > len(df) * 0.1:  # More than 10% null values
            st.warning(f"High number of null values detected: {null_counts.sum()}")
        
        return True
    except Exception as e:
        logger.error(f"Data validation error: {str(e)}")
        return False

def safe_numeric_conversion(value: Any, default: float = 0.0) -> float:
    """Safely convert value to numeric with error handling"""
    try:
        if pd.isna(value) or value == '':
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def log_user_action(action: str, details: dict = None):
    """Log user actions for audit purposes"""
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details or {}
        }
        logger.info(f"User action: {action} - {details}")
    except Exception as e:
        logger.error(f"Failed to log user action: {str(e)}")

def display_error_summary(errors: list):
    """Display a summary of errors in a user-friendly format"""
    if not errors:
        return
    
    st.error("⚠️ Data Quality Issues Detected:")
    for i, error in enumerate(errors, 1):
        st.write(f"{i}. {error}")
    
    st.info("💡 Tip: Please review and correct the data before proceeding.") 