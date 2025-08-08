#!/usr/bin/env python3
"""
Heroku Deployment Helper Script
This script helps prepare and validate your app for Heroku deployment
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_file_exists(filename):
    """Check if a required file exists"""
    if os.path.exists(filename):
        print(f"✅ {filename} - Found")
        return True
    else:
        print(f"❌ {filename} - Missing")
        return False

def validate_requirements():
    """Validate that all required files exist"""
    print("🔍 Checking required files for Heroku deployment...")
    
    required_files = [
        'streamlit_app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.streamlit/config.toml'
    ]
    
    all_good = True
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    return all_good

def check_requirements_content():
    """Check requirements.txt content"""
    print("\n📦 Checking requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required_packages = [
            'streamlit',
            'pandas',
            'plotly',
            'gunicorn'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"⚠️ Missing packages in requirements.txt: {missing_packages}")
            return False
        else:
            print("✅ All required packages found in requirements.txt")
            return True
            
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def check_procfile():
    """Check Procfile content"""
    print("\n📄 Checking Procfile...")
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
            
        if 'streamlit run streamlit_app.py' in content and '$PORT' in content:
            print("✅ Procfile looks correct")
            return True
        else:
            print("❌ Procfile may be incorrect")
            print(f"Current content: {content}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading Procfile: {e}")
        return False

def create_deployment_summary():
    """Create a deployment summary"""
    print("\n📋 Deployment Summary")
    print("=" * 50)
    
    # App information
    app_name = input("Enter your desired Heroku app name (or press Enter for auto-generated): ").strip()
    
    summary = {
        "app_name": app_name or "your-fund-admin-app",
        "deployment_method": "Heroku Dashboard",
        "repository": "OCR-app-1",
        "main_file": "streamlit_app.py",
        "port": 8501
    }
    
    print(f"\n🎯 Deployment Configuration:")
    print(f"   App Name: {summary['app_name']}")
    print(f"   Method: {summary['deployment_method']}")
    print(f"   Repository: {summary['repository']}")
    print(f"   Main File: {summary['main_file']}")
    
    # Save summary
    with open('deployment_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Deployment summary saved to deployment_summary.json")
    
    return summary

def generate_heroku_commands():
    """Generate Heroku CLI commands for reference"""
    print("\n🔧 Heroku CLI Commands (if you install CLI later):")
    print("=" * 50)
    
    commands = [
        "heroku login",
        "heroku create your-fund-admin-app",
        "git push heroku main",
        "heroku open",
        "heroku logs --tail"
    ]
    
    for cmd in commands:
        print(f"$ {cmd}")
    
    print("\n📝 Note: You can also deploy via Heroku Dashboard (recommended for now)")

def main():
    """Main deployment validation function"""
    print("🚀 Heroku Deployment Validator")
    print("=" * 50)
    
    # Check files
    files_ok = validate_requirements()
    
    # Check requirements
    requirements_ok = check_requirements_content()
    
    # Check Procfile
    procfile_ok = check_procfile()
    
    print("\n" + "=" * 50)
    
    if files_ok and requirements_ok and procfile_ok:
        print("✅ All checks passed! Your app is ready for Heroku deployment.")
        
        # Create deployment summary
        summary = create_deployment_summary()
        
        # Generate commands
        generate_heroku_commands()
        
        print("\n🎉 Next Steps:")
        print("1. Push your code to GitHub (if not already done)")
        print("2. Go to https://dashboard.heroku.com")
        print("3. Create a new app")
        print("4. Connect your GitHub repository")
        print("5. Deploy!")
        
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        print("\n💡 Common fixes:")
        print("- Ensure all required files exist")
        print("- Check requirements.txt has all dependencies")
        print("- Verify Procfile format is correct")

if __name__ == "__main__":
    main() 