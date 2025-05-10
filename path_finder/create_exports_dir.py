#!/usr/bin/env python
"""
This script creates the exports directory for the Path Finder application.
Run this before starting the application to ensure the exports directory exists.
"""

import os

def main():
    """Create the exports directory if it doesn't exist."""
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the exports directory path
    exports_dir = os.path.join(current_dir, "exports")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
        print(f"Created exports directory: {exports_dir}")
    else:
        print(f"Exports directory already exists: {exports_dir}")

if __name__ == "__main__":
    main() 