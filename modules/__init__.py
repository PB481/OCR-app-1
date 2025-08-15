"""
Feature modules for the Fund Administration Platform
"""

from .workstream_management import WorkstreamManagement
from .capital_projects import CapitalProjects
from .pl_analysis import PLAnalysis
from .competitors import CompetitorsAnalysis
from .business_cases import BusinessCases

__all__ = [
    'WorkstreamManagement',
    'CapitalProjects', 
    'PLAnalysis',
    'CompetitorsAnalysis',
    'BusinessCases'
]