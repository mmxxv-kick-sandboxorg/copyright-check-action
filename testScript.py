#!/usr/bin/env python3
"""
Simplified Copyright Infringement Detection Script for Testing
"""
import os
import sys
import json

def main():
    print("=== Simplified Copyright Check Test ===")
    
    # Debug all environment variables
    print("\n=== ALL Environment Variables ===")
    for key, value in sorted(os.environ.items()):
        if any(keyword in key.upper() for keyword in ['PR', 'GITHUB', 'AACS', 'TOKEN']):
            if any(secret in key.upper() for secret in ['TOKEN', 'KEY', 'SECRET']):
                print(f"{key}: ***")
            else:
                print(f"{key}: {value}")
    
    print(f"\n=== Searching for PR Number ===")
    # Try multiple possible environment variable names
    pr_sources = [
        ('PR_NUMBER', os.getenv('PR_NUMBER')),
        ('GITHUB_PR_NUMBER', os.getenv('GITHUB_PR_NUMBER')),
        ('INPUT_PR_NUMBER', os.getenv('INPUT_PR_NUMBER')),
        ('EVENT_PR_NUMBER', os.getenv('EVENT_PR_NUMBER'))
    ]
    
    pr_number = None
    for source_name, source_value in pr_sources:
        print(f"Checking {source_name}: {source_value}")
        if source_value and source_value.strip() and source_value != 'null':
            try:
                pr_number = int(source_value)
                print(f"✅ Found valid PR number from {source_name}: {pr_number}")
                break
            except ValueError:
                print(f"❌ Invalid PR number format in {source_name}: {source_value}")
    
    if pr_number is None:
        print("\n❌ ERROR: No valid PR number found in any environment variable")
        print("Command line arguments:", sys.argv)
        
        # Try to get from command line as fallback
        if len(sys.argv) > 1:
            try:
                pr_number = int(sys.argv[1])
                print(f"✅ Using PR number from command line: {pr_number}")
            except ValueError:
                print(f"❌ Invalid command line PR number: {sys.argv[1]}")
        
        if pr_number is None:
            print("❌ No PR number available from any source")
            return 1
    
    print(f"\n✅ Processing PR #{pr_number}")
    
    # Print all relevant environment variables
    print("\n=== Environment Variables ===")
    for key, value in sorted(os.environ.items()):
        if any(keyword in key for keyword in ['PR_NUMBER', 'GITHUB_', 'AACS']):
            if any(secret in key for secret in ['TOKEN', 'KEY']):
                print(f"{key}: ***")
            else:
                print(f"{key}: {value}")
    
    # Simple analysis simulation
    print(f"\n=== Analysis Results for PR #{pr_number} ===")
    result = {
        "pr_number": pr_number,
        "violations_found": False,
        "violation_count": 0,
        "status": "completed",
        "message": "Test analysis completed successfully"
    }
    
    print(json.dumps(result, indent=2))
    
    # Set GitHub Actions output if available
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"result={json.dumps(result)}\n")
            f.write(f"violations-found=false\n")
    
    print("\n✅ Test completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())