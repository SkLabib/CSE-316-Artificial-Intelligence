#!/usr/bin/env python
"""
This script makes it easier to run the Path Finder application.
Instead of using 'streamlit run main.py', you can just run this script.
"""

import os
import subprocess
import sys

def create_exports_dir(base_dir):
    """Create the exports directory if it doesn't exist."""
    exports_dir = os.path.join(base_dir, "exports")
    
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        print(f"Created exports directory: {exports_dir}")
    
    return exports_dir

def main():
    """Run the Path Finder Streamlit application."""
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create exports directory
    create_exports_dir(current_dir)
    
    # The main application file
    main_app = os.path.join(current_dir, "main_standalone.py")
    
    # Check if the main file exists
    if not os.path.exists(main_app):
        print(f"Error: Could not find {main_app}")
        return 1
    
    # Run the Streamlit application
    cmd = [sys.executable, "-m", "streamlit", "run", main_app, "--server.headless", "true"]
    
    try:
        process = subprocess.run(cmd)
        return process.returncode
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
        return 0
    except Exception as e:
        print(f"Error running application: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 