import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import configuration and utilities
from config.settings import PAGE_CONFIG, SESSION_KEYS
from config.constants import CURRENT_YEAR
from utils.data_loader import SessionStateManager

# Import modules
from modules.capital_projects import CapitalProjects
from modules.workstream_management import WorkstreamManagement
from modules.pl_analysis import PLAnalysis  
from modules.competitors import CompetitorsAnalysis
from modules.business_cases import BusinessCases


class FundAdministrationApp:
    """Main application class"""
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
        self.modules = self.setup_modules()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(**PAGE_CONFIG)
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        SessionStateManager.initialize_session_state()
        SessionStateManager.load_workstream_data()
    
    def setup_modules(self):
        """Initialize feature modules"""
        return {
            "🏗️ Workstream Management": WorkstreamManagement(),
            "💰 Capital Projects": CapitalProjects(),
            "📊 P&L Analysis": PLAnalysis(),
            "🏆 Competitors Analysis": CompetitorsAnalysis(), 
            "💼 Business Cases": BusinessCases()
        }
    
    def render_sidebar_navigation(self):
        """Render sidebar navigation"""
        st.sidebar.title("🏗️ Fund Administration Platform")
        st.sidebar.markdown(f"**Analysis Year:** {CURRENT_YEAR}")
        st.sidebar.markdown("---")
        
        # Module selection
        selected_module = st.sidebar.selectbox(
            "Select Analysis Module:",
            list(self.modules.keys()),
            help="Choose the analysis module you want to use"
        )
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 Module Overview")
        
        module_descriptions = {
            "🏗️ Workstream Management": "Operational workstream analysis and portfolio management",
            "💰 Capital Projects": "Capital project portfolio tracking and variance analysis", 
            "📊 P&L Analysis": "Profit & Loss analysis with comparative metrics",
            "🏆 Competitors Analysis": "Competitive positioning and market analysis",
            "💼 Business Cases": "Business case development and scoring system"
        }
        
        for module, description in module_descriptions.items():
            if module == selected_module:
                st.sidebar.info(f"**{module}**\n\n{description}")
            else:
                st.sidebar.markdown(f"**{module}**\n{description}")
        
        return selected_module
    
    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🔧 System Info")
            st.markdown(f"- **Analysis Year:** {CURRENT_YEAR}")
            st.markdown(f"- **Modules:** {len(self.modules)}")
            st.markdown("- **Status:** Active")
        
        with col2:
            st.markdown("### 📈 Quick Stats")
            total_projects = len(st.session_state.get('capital_project_data', []))
            total_workstreams = len(st.session_state.get('workstream_data', []))
            
            st.markdown(f"- **Workstreams:** {total_workstreams}")
            st.markdown(f"- **Projects:** {total_projects}")
            st.markdown("- **Reports:** Generated on-demand")
        
        with col3:
            st.markdown("### 🎯 Features")
            st.markdown("- ✅ Multi-module analysis")
            st.markdown("- ✅ Interactive dashboards") 
            st.markdown("- ✅ Export capabilities")
            st.markdown("- ✅ Real-time calculations")
        
        # Copyright and version info
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
                <p>Fund Administration Platform v2.0 | Built with Streamlit | 
                <a href='#' style='color: #666;'>Documentation</a> | 
                <a href='#' style='color: #666;'>Support</a></p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    def run(self):
        """Run the main application"""
        try:
            # Render navigation
            selected_module = self.render_sidebar_navigation()
            
            # Render selected module
            if selected_module in self.modules:
                self.modules[selected_module].render()
            else:
                st.error(f"Module '{selected_module}' not found")
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            st.markdown("---")
            st.markdown("**Error Details:**")
            st.code(str(e))
            
            # Show fallback content
            st.markdown("### 🔄 Fallback Mode")
            st.info("The application encountered an error. Please refresh the page or contact support.")


def main():
    """Application entry point"""
    try:
        app = FundAdministrationApp()
        app.run()
    except Exception as e:
        st.error(f"Critical application error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()