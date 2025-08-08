# 🏗️ Iluvalcar 2.0 - Fund Administration Workstream Management Platform

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

A comprehensive, interactive Streamlit application for Fund Administration workstream management, capital project analysis, business case development, and competitive intelligence. This enterprise-grade platform provides 3D analytics, automated reporting, and data-driven insights for fund administration operations.

## 🎯 Overview

**Iluvalcar 2.0** is a multi-tab application that transforms fund administration operations through:
- **Interactive 3D Analytics**: Advanced visualizations for workstream analysis
- **Capital Project Management**: Comprehensive portfolio tracking with variance analysis
- **Business Case Development**: Scoring engine with workflow management
- **Competitive Intelligence**: Market positioning and strategic analysis
- **P&L Analysis**: Revenue attribution and cost allocation methodologies
- **Automated Reporting**: Professional HTML/Excel report generation

## 🚀 Features

### 🧪 Tab 1: Workstream Views
- **Periodic Table Visualization**: Interactive workstream mapping with hover tooltips
- **Network Diagrams**: Relationship analysis between workstreams
- **Heat Maps**: Risk, complexity, and automation level analysis
- **Bubble Charts**: Investment vs completion analysis
- **Professional Dashboard**: Metrics and performance indicators

### 📊 Tab 2: 3D Analysis
- **3D Scatter Plots**: Multi-dimensional workstream analysis
- **P&L Integration**: Revenue and cost analysis overlays
- **Dynamic Filtering**: Category-based analysis
- **Investment Visualization**: Bubble size represents investment amounts
- **Interactive Controls**: Rotation, zoom, and selection capabilities

### ⚙️ Tab 3: Manage Workstreams
- **CRUD Operations**: Add, edit, delete workstream data
- **Data Import/Export**: CSV and JSON format support
- **Template Management**: Pre-configured workstream templates
- **Real-time Updates**: Instant visualization updates
- **Data Validation**: Input validation and error handling

### 💰 Tab 4: Capital Projects
- **Portfolio Dashboard**: Comprehensive project tracking
- **Financial Analytics**: Budget variance and reallocation analysis
- **Monthly Trends**: Actuals vs forecasts visualization
- **Performance Ranking**: Project success metrics
- **Template System**: Excel templates with examples
- **Professional Reports**: HTML and Excel export

**Key Metrics:**
- Sum Actual Spend (YTD)
- Total Potential Underspend/Overspend
- Net Reallocation Amount
- Average Monthly Spread Score
- Project Performance Rankings

### 📄 Tab 5: Source Code
- **Code Inspection**: Complete application source code
- **Technical Documentation**: Function explanations
- **Architecture Overview**: Component relationships

### 💼 Tab 6: P&L Analysis
- **Revenue Attribution**: Service line and client segment analysis
- **Cost Allocation**: Direct and indirect cost mapping
- **Profitability Analysis**: Margin and efficiency metrics
- **Template System**: Comprehensive P&L data collection
- **AUM Efficiency**: Assets under management analysis

**Analysis Components:**
- Revenue Breakdown Charts
- Cost Allocation Visualization
- Profitability Trends
- AUM Efficiency Metrics

### 🏆 Tab 7: Competitors Analysis
- **Market Positioning**: Competitive landscape mapping
- **Technology Analysis**: Feature comparison matrix
- **Strategic Intelligence**: Market evolution tracking
- **Template System**: Competitor data collection
- **Visualization**: Interactive charts and heatmaps

**Competitor Categories:**
- Global Custodians (State Street, JPM, BNY, HSBC, Citi)
- Technology Providers
- Service Specialists
- Emerging Players

### 📋 Tab 8: Business Cases
- **Scoring Engine**: Weighted criteria analysis (Financial 30%, Strategic 25%, Feasibility 20%, Impact 15%, Resource 10%)
- **Pipeline Management**: Parking Lot → Backlog → Roadmap workflow
- **Gap Analysis**: Performance benchmarking
- **Template System**: Business case data collection
- **Automated Promotion**: Threshold-based advancement (70+ score)

**Business Case Components:**
- ROI and Payback Period Analysis
- Strategic Alignment Scoring
- Feasibility Assessment
- Resource Requirements
- Impact Analysis

## 🛠️ Technical Architecture

### Core Dependencies
```
streamlit>=1.28.0      # Web application framework
pandas>=1.5.0          # Data manipulation and analysis
plotly>=5.0.0          # Interactive visualizations
numpy>=1.21.0          # Numerical computing
openpyxl>=3.0.0        # Excel file handling
xlsxwriter>=3.0.0      # Excel template generation
```

### Application Structure
```
streamlit_app.py           # Main application (5000+ lines)
├── Session State Management
├── Data Loading Functions
├── Visualization Functions
├── Template Generation
├── Report Generation
└── 8 Main Tabs
```

### Key Functions

#### Data Management
- `load_capital_project_data()`: CSV/Excel data processing
- `load_pl_data()`: P&L data validation and cleaning
- `load_competitors_data()`: Competitive intelligence data handling

#### Template Generation
- `create_capital_projects_template()`: Capital project Excel templates
- `create_pl_template()`: P&L analysis templates
- `create_competitors_template()`: Competitor analysis templates
- `create_business_case_template()`: Business case templates

#### Visualization
- `create_workstream_periodic_table()`: Interactive periodic table
- `create_3d_analysis()`: Multi-dimensional scatter plots
- `create_competitive_positioning_chart()`: Market positioning
- `create_pl_analysis_charts()`: Financial analysis visualizations

#### Reporting
- `generate_capital_html_report()`: Professional HTML reports
- `generate_capital_excel_report()`: Multi-sheet Excel reports
- `generate_business_case_report()`: Business case documentation

### Data Models

#### Workstream Data Structure
```python
{
    'id': 'nav_001',
    'name': 'NAV Calculation & Publication',
    'category': 'NAV Calculation',
    'complexity': 8,        # 1-10 scale
    'automation': 7,        # 1-10 scale
    'risk': 8,              # 1-10 scale
    'investment': 4.2,      # Millions USD
    'completion': 80,       # Percentage
    'priority': 'High',     # High/Medium/Low
    'description': 'Core NAV calculation engine...'
}
```

#### Capital Project Structure
```python
{
    'PROJECT_ID': 'PROJ_001',
    'PROJECT_NAME': 'Digital Trade Processing Platform',
    'PORTFOLIO_OBS_LEVEL1': 'Technology Infrastructure',
    'BUSINESS_ALLOCATION': 5000000.0,
    'CURRENT_EAC': 4800000.0,
    '2025_01_A': 200000.0,  # Monthly actuals
    '2025_01_F': 180000.0,  # Monthly forecasts
    # ... additional monthly columns
}
```

#### Business Case Structure
```python
{
    'Case_ID': 'BC_001',
    'Case_Title': 'Digital Enhancement Initiative',
    'ROI_Percentage': 60.0,
    'Payback_Period_Months': 20,
    'Strategic_Alignment_Score': 8.5,
    'Total_Score': 84.4,    # 0-100 scale
    # ... additional scoring criteria
}
```

## 📊 Analytics & Reporting

### 3D Analysis Capabilities
- **Complexity vs Automation vs Risk**: Multi-dimensional workstream analysis
- **Investment Visualization**: Marker size represents investment amounts
- **Category Color Coding**: Visual differentiation by workstream type
- **Interactive Controls**: Zoom, rotate, and filter capabilities

### Professional Reporting
- **HTML Reports**: Styled, responsive reports with embedded charts
- **Excel Exports**: Multi-sheet workbooks with professional formatting
- **Template Downloads**: Pre-configured data collection templates
- **Real-time Updates**: Dynamic report generation

### Performance Metrics
- **Workstream Analytics**: Completion rates, investment efficiency
- **Capital Project KPIs**: Variance analysis, reallocation opportunities
- **Business Case Scoring**: Weighted multi-criteria analysis
- **Competitive Intelligence**: Market positioning metrics

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+ 
- pip package manager
- Excel-compatible software (for template downloads)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OCR-app-1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:8501`

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t iluvalcar-app .
   ```

2. **Run container**
   ```bash
   docker run -p 8501:8501 iluvalcar-app
   ```

### Heroku Deployment

The application includes Heroku deployment configuration:
- `Procfile`: Web process configuration
- `runtime.txt`: Python version specification
- `setup.sh`: Streamlit configuration

## 📋 Usage Guide

### Getting Started

1. **Launch the application** and navigate through the 8 main tabs
2. **Download templates** from each relevant section to understand data requirements
3. **Upload your data** using the provided file uploaders
4. **Explore visualizations** with interactive controls
5. **Generate reports** for professional presentations

### Data Preparation

#### For Workstream Analysis
- Use the workstream management interface to add/edit data
- Categories: NAV Calculation, Portfolio Valuation, Trade Capture, Reconciliation, Corporate Actions, Expense Management, Reporting

#### For Capital Projects
- Download the Capital Projects template
- Populate with project data including monthly actuals, forecasts, and plans
- Include portfolio classification and management details

#### For P&L Analysis
- Download the P&L template with service line structure
- Include revenue attribution and cost allocation data
- Ensure AUM data for efficiency calculations

#### For Business Cases
- Download the Business Case template
- Complete ROI, payback period, and strategic alignment data
- System automatically scores and manages pipeline progression

### Advanced Features

#### 3D Analysis
- Use the 3D scatter plots to identify workstream optimization opportunities
- High complexity + low automation = automation candidates
- High risk + low investment = investment priorities

#### Pipeline Management
- Business cases automatically move through pipeline based on scores
- Parking Lot (initial assessment) → Backlog (approved) → Roadmap (prioritized)
- Threshold scoring determines progression

#### Competitive Analysis
- Upload competitor data for market positioning analysis
- Use technology comparison matrices for strategic planning
- Monitor market evolution trends

## 🔍 Troubleshooting

### Common Issues

1. **Template Download Issues**
   - Ensure pop-up blockers are disabled
   - Use modern browser (Chrome, Firefox, Safari)

2. **Data Upload Errors**
   - Check file format (CSV or Excel)
   - Verify column names match template structure
   - Ensure numerical fields contain valid numbers

3. **Visualization Performance**
   - Large datasets may impact 3D rendering performance
   - Filter data to improve responsiveness

4. **Report Generation**
   - Ensure all required data is uploaded
   - Check for missing values in key fields

### Support

For technical issues or feature requests:
1. Check the Source Code tab for implementation details
2. Review template structures for data format requirements
3. Ensure all dependencies are properly installed

## 🚀 Deployment Options

### Local Development
- Run directly with `streamlit run streamlit_app.py`
- Ideal for development and testing

### Cloud Deployment
- **Streamlit Cloud**: Deploy directly from GitHub
- **Heroku**: Use provided Heroku configuration
- **Docker**: Containerized deployment for any platform
- **AWS/Azure/GCP**: Cloud platform deployment

## 📈 Future Enhancements

### Planned Features
- Real-time data integration APIs
- Advanced ML-based workstream optimization
- Enhanced mobile responsiveness
- Role-based access control
- Audit trail and change tracking

### Extensibility
The application is designed for easy extension:
- Modular tab structure for adding new features
- Template system for new data types
- Visualization framework for new chart types
- Reporting engine for custom report formats

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Iluvalcar 2.0** - Transforming Fund Administration through Advanced Analytics and Automation

For questions or support, please refer to the application's Source Code tab for detailed implementation information.