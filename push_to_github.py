"""
Script to push simulation results to GitHub repository.
"""

import os
import subprocess
from datetime import datetime

def push_to_github(output_dir: str):
    """Push simulation results to GitHub repository."""
    print("Pushing results to GitHub...")
    
    # Initialize git repository if not already done
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'remote', 'add', 'origin', 
                       'https://github.com/deluair/Integrated-Coastal-Resilience-and-Blue-Economy-Development-for-Bangladesh.git'])
    
    # Add all files
    subprocess.run(['git', 'add', '.'])
    
    # Create commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Simulation results: {timestamp}"
    
    # Commit changes
    subprocess.run(['git', 'commit', '-m', commit_message])
    
    # Push to GitHub
    subprocess.run(['git', 'push', '-u', 'origin', 'master'])
    
    print("Results pushed to GitHub successfully!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python push_to_github.py <output_directory>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    push_to_github(output_dir) 