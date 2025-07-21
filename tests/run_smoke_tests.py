#!/usr/bin/env python3
"""
Simple test runner for Synth Riders Discord RPC Smoke Tests

This script runs the smoke tests with proper environment setup.
"""

import os
import sys
import subprocess

def main():
    """Run the smoke tests"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Add project root to Python path
    sys.path.insert(0, project_root)
    
    print("🚀 Starting Synth Riders Discord RPC Smoke Tests")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.executable}")
    print("-" * 60)
    
    try:
        # Import and run the smoke tests
        from test_smoke import run_smoke_tests
        
        success = run_smoke_tests()
        
        if success:
            print("\n🎉 All smoke tests completed successfully!")
            return 0
        else:
            print("\n💥 Some smoke tests failed!")
            return 1
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 