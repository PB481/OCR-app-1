#!/usr/bin/env python3

import sys
import traceback

print("Testing imports for the integrated app...")

try:
    import streamlit as st
    print("✅ streamlit imported successfully")
except ImportError as e:
    print(f"❌ Failed to import streamlit: {e}")

try:
    import pandas as pd
    print("✅ pandas imported successfully")
except ImportError as e:
    print(f"❌ Failed to import pandas: {e}")

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    print("✅ plotly imported successfully")
except ImportError as e:
    print(f"❌ Failed to import plotly: {e}")

try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError as e:
    print(f"❌ Failed to import numpy: {e}")

try:
    import io
    import re
    import inspect
    from datetime import datetime, timedelta
    import json
    print("✅ Standard library imports successful")
except ImportError as e:
    print(f"❌ Failed to import standard libraries: {e}")

print("\n🔍 Checking key functions exist in the main app...")

try:
    # Import the functions from the main app
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Test if we can load the file without executing it
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        
    if 'load_capital_project_data' in content:
        print("✅ Capital project data loading function found")
    else:
        print("❌ Capital project data loading function missing")
        
    if 'generate_capital_html_report' in content:
        print("✅ Capital project HTML report function found")
    else:
        print("❌ Capital project HTML report function missing")
        
    if 'main_tab4' in content:
        print("✅ Fourth main tab (Capital Projects) found")
    else:
        print("❌ Fourth main tab missing")
        
except Exception as e:
    print(f"❌ Error checking main app: {e}")
    traceback.print_exc()

print("\n✨ Integration test complete!")