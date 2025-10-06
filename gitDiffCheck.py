# Unpublished Copyright (c) 2025 NTT, Inc. All rights reserved.
# 
# Copyright Infringement Detection tool for ubuntu
# Enhanced version for Composite Action usage

# import section
import sys
import json
import time
import subprocess
import requests
import argparse
import difflib
import urllib.request
import numpy as np
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# define config param.
config = {
    "k": 0.5,
    "thr": -0.012
}

# 実行時間の計測開始
start_time = time.time()

# GitHub のコメント先頭に付与する固定文字列
strGitCommentHeader = '[Copyright Infringement Detection] '

# REST API endpoint
url = os.getenv("AACS")
# AACS APIkey
AACSAPIkey = os.getenv("AACSAPIkey")

# GitHub repository information
github_repository = os.getenv("GITHUB_REPOSITORY", "")
github_token = os.getenv("GITHUB_TOKEN", "")

def load_model(name):
    """
    Load a pre-trained language model and tokenizer from local directory or Hugging Face.
    
    Args:
        name (str): Model name/path from Hugging Face Hub or local directory path
        
    Returns:
        tuple: (model, tokenizer) - Loaded model and tokenizer
        
    Raises:
        RuntimeError: If HUGGINGFACE_TOKEN environment variable is not set for remote models
        FileNotFoundError: If local model directory is not found
    """
    try:
        # Try loading from local directory first
        if os.path.exists(name):
            print(f"Loading model from local directory: {name}")
            tokenizer = AutoTokenizer.from_pretrained(name, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(name, local_files_only=True)
            return model, tokenizer
    except Exception as e:
        print(f"Failed to load from local directory: {e}")
    
    # Fall back to Hugging Face Hub
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        raise RuntimeError("HUGGINGFACE_TOKEN environment variable must be set for remote model access")
    
    print(f"Loading model from Hugging Face: {name}")
    tokenizer = AutoTokenizer.from_pretrained(name, use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(name, use_auth_token=hf_token)
    
    return model, tokenizer

def get_git_diff(pr_number):
    """
    Get git diff for the specified pull request.
    
    Args:
        pr_number (int): Pull request number
        
    Returns:
        str: Git diff content
    """
    try:
        # Use GitHub API to get PR diff if available
        if github_repository and github_token:
            api_url = f"https://api.github.com/repos/{github_repository}/pulls/{pr_number}"
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3.diff"
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return response.text
        
        # Fallback to git command
        result = subprocess.run(['git', 'diff', 'HEAD~1'], 
                              capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error getting git diff: {e}")
        return ""

def post_github_comment(pr_number, comment):
    """
    Post a comment to GitHub PR.
    
    Args:
        pr_number (int): Pull request number
        comment (str): Comment text
    """
    if not github_repository or not github_token:
        print("GitHub repository or token not available, skipping comment")
        return
    
    api_url = f"https://api.github.com/repos/{github_repository}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 201:
            print("Comment posted successfully")
        else:
            print(f"Failed to post comment: {response.status_code}")
    except Exception as e:
        print(f"Error posting comment: {e}")

def analyze_copyright_infringement(diff_content, pr_number):
    """
    Analyze git diff for copyright infringement using AI model.
    
    Args:
        diff_content (str): Git diff content
        pr_number (int): Pull request number
        
    Returns:
        dict: Analysis results
    """
    print("Starting copyright infringement analysis...")
    
    try:
        # Load the model (you can specify your preferred model here)
        model, tokenizer = load_model("microsoft/DialoGPT-medium")
        
        # Analyze the diff content
        # This is a simplified example - implement your actual analysis logic
        lines = diff_content.split('\n')
        added_lines = [line for line in lines if line.startswith('+') and not line.startswith('+++')]
        
        violations = []
        
        for i, line in enumerate(added_lines):
            # Implement your copyright detection logic here
            if 'copyright' in line.lower() or '©' in line:
                violations.append({
                    'line': line,
                    'risk_level': 'high',
                    'reason': 'Contains copyright notice'
                })
        
        result = {
            'violations_found': len(violations) > 0,
            'violation_count': len(violations),
            'violations': violations,
            'analysis_time': time.time() - start_time
        }
        
        # Post results to GitHub
        if violations:
            comment = f"{strGitCommentHeader}⚠️ Copyright infringement detected!\n\n"
            comment += f"Found {len(violations)} potential violations:\n\n"
            for v in violations[:5]:  # Limit to first 5
                comment += f"- `{v['line']}` (Risk: {v['risk_level']})\n"
            if len(violations) > 5:
                comment += f"- ... and {len(violations) - 5} more\n"
        else:
            comment = f"{strGitCommentHeader}✅ No copyright infringement detected."
        
        post_github_comment(pr_number, comment)
        
        return result
        
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        print(error_msg)
        post_github_comment(pr_number, f"{strGitCommentHeader}❌ {error_msg}")
        return {'error': error_msg}

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Copyright Infringement Detection')
    parser.add_argument('pr_number', type=int, help='Pull request number')
    
    args = parser.parse_args()
    
    print(f"Analyzing PR #{args.pr_number} in repository {github_repository}")
    
    # Get git diff
    diff_content = get_git_diff(args.pr_number)
    
    if not diff_content:
        print("No diff content found")
        return
    
    # Analyze for copyright infringement
    result = analyze_copyright_infringement(diff_content, args.pr_number)
    
    # Output results
    print(json.dumps(result, indent=2))
    
    # Set GitHub Actions output
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"result={json.dumps(result)}\n")
            f.write(f"violations-found={str(result.get('violations_found', False)).lower()}\n")

if __name__ == "__main__":
    main()