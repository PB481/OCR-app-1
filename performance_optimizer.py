"""
Performance optimization utilities for the Fund Administration Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from functools import lru_cache
import time
import gc

class PerformanceMonitor:
    """Monitor and optimize application performance"""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = None
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_time = time.time()
        self.metrics[operation] = {'start': self.start_time}
    
    def end_timer(self, operation: str):
        """End timing an operation and log duration"""
        if self.start_time and operation in self.metrics:
            duration = time.time() - self.start_time
            self.metrics[operation]['duration'] = duration
            self.metrics[operation]['end'] = time.time()
            
            if duration > 5.0:  # Log slow operations
                st.warning(f"⚠️ Slow operation detected: {operation} took {duration:.2f}s")
    
    def get_performance_summary(self) -> Dict[str, float]:
        """Get summary of performance metrics"""
        return {op: data.get('duration', 0) for op, data in self.metrics.items()}

# Global performance monitor
perf_monitor = PerformanceMonitor()

@st.cache_data(ttl=600)  # Cache for 10 minutes
def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage and performance"""
    try:
        # Convert object columns to appropriate types
        for col in df.select_dtypes(include=['object']):
            if df[col].nunique() / len(df) < 0.5:  # Low cardinality
                df[col] = df[col].astype('category')
        
        # Convert numeric columns to appropriate types
        for col in df.select_dtypes(include=['int64']):
            if df[col].min() >= 0:
                if df[col].max() < 255:
                    df[col] = df[col].astype('uint8')
                elif df[col].max() < 65535:
                    df[col] = df[col].astype('uint16')
                else:
                    df[col] = df[col].astype('uint32')
        
        # Convert float columns
        for col in df.select_dtypes(include=['float64']):
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        return df
    except Exception as e:
        st.warning(f"DataFrame optimization failed: {str(e)}")
        return df

@lru_cache(maxsize=128)
def cached_calculation(func_name: str, *args) -> Any:
    """Cache expensive calculations"""
    # This is a placeholder for actual calculation caching
    # In practice, you would implement specific calculation caching here
    pass

def batch_process_data(data_list: List[pd.DataFrame], 
                      process_func: callable,
                      batch_size: int = 10) -> List[Any]:
    """Process data in batches to avoid memory issues"""
    results = []
    
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i + batch_size]
        batch_results = [process_func(df) for df in batch]
        results.extend(batch_results)
        
        # Force garbage collection after each batch
        gc.collect()
    
    return results

def optimize_chart_rendering(fig, max_points: int = 1000):
    """Optimize chart rendering for large datasets"""
    try:
        # Reduce data points for large datasets
        if hasattr(fig, 'data') and len(fig.data) > 0:
            for trace in fig.data:
                if hasattr(trace, 'x') and len(trace.x) > max_points:
                    # Sample data points
                    indices = np.linspace(0, len(trace.x) - 1, max_points, dtype=int)
                    trace.x = [trace.x[i] for i in indices]
                    trace.y = [trace.y[i] for i in indices]
        
        return fig
    except Exception as e:
        st.warning(f"Chart optimization failed: {str(e)}")
        return fig

def memory_usage_optimization():
    """Monitor and optimize memory usage"""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        if memory_mb > 500:  # Warning at 500MB
            st.warning(f"⚠️ High memory usage: {memory_mb:.1f}MB")
            
            # Force garbage collection
            gc.collect()
            
            # Clear Streamlit cache if needed
            if memory_mb > 1000:  # Critical at 1GB
                st.cache_data.clear()
                st.cache_resource.clear()
        
        return memory_mb
    except ImportError:
        return None

def async_data_loading(func: callable):
    """Decorator for asynchronous data loading"""
    def wrapper(*args, **kwargs):
        with st.spinner("Loading data..."):
            return func(*args, **kwargs)
    return wrapper

# Performance monitoring decorator
def monitor_performance(operation_name: str):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            perf_monitor.start_timer(operation_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                perf_monitor.end_timer(operation_name)
        return wrapper
    return decorator 