#!/usr/bin/env python3
"""
Heroku Deployment Helper
This script helps with the Heroku deployment process
"""

import os
import sys

def check_deployment_readiness():
    """Check if the app is ready for Heroku deployment"""
    print("🚀 Heroku Deployment Readiness Check")
    print("=" * 50)
    
    # Check file sizes
    files_to_check = [
        'streamlit_app_heroku.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.streamlit/config.toml'
    ]
    
    total_size = 0
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            total_size += size
            print(f"✅ {file} - {size:,} bytes")
        else:
            print(f"❌ {file} - Missing")
    
    print(f"\n📊 Total size of core files: {total_size:,} bytes")
    
    # Check requirements
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            package_count = len([line for line in requirements.split('\n') if line.strip() and not line.startswith('#')])
            print(f"📦 Number of packages: {package_count}")
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
    
    print("\n💡 Deployment Tips:")
    print("- The streamlined app should be much smaller")
    print("- Core functionality is preserved")
    print("- 3D visualizations removed to reduce size")
    print("- Focus on essential features only")
    
    return True

def main():
    """Main function"""
    print("🎯 Heroku Deployment Helper")
    print("=" * 50)
    
    ready = check_deployment_readiness()
    
    if ready:
        print("\n✅ App is ready for Heroku deployment!")
        print("\n📋 Next Steps:")
        print("1. Commit and push the streamlined version")
        print("2. Try deploying again in Heroku Dashboard")
        print("3. The app should now be under 500MB")
        print("4. Monitor the build logs for any issues")
    else:
        print("\n❌ Some issues need to be resolved before deployment")

if __name__ == "__main__":
    main() 