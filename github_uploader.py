#!/usr/bin/env python3
import os
import json
import base64
import urllib.request
import urllib.error
import glob
import fnmatch
from pathlib import Path

# Configuration
GITHUB_API_URL = "https://api.github.com"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def load_gitignore(root_dir):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    # Add default ignores
    patterns.extend(['.git', '.github', '*.pyc', '__pycache__', '.DS_Store'])
    return patterns

def is_ignored(path, root_dir, patterns):
    rel_path = os.path.relpath(path, root_dir)
    name = os.path.basename(path)
    
    for pattern in patterns:
        # Normalize pattern
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/')
            
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
        
        # Check directory matches
        if os.path.isdir(path) and (fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(name + '/', pattern)):
            return True
            
        # Check path segments
        parts = rel_path.split(os.sep)
        for part in parts:
             if fnmatch.fnmatch(part, pattern):
                 return True
                 
    return False

def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

import ssl

def upload_file(token, repo, file_path, remote_path):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{remote_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    content = get_file_content(file_path)
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    # Create unverified SSL context to avoid certificate errors on some macOS Python installs
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Check if file exists to get SHA (for update)
    sha = None
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                sha = data.get('sha')
                print(f"  Existing file found: {remote_path} (updating)")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"  Error checking file {remote_path}: {e}")
            return False

    # Prepare payload
    data = {
        "message": f"Upload {remote_path} via photonic_uploader",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha
        
    # Upload
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='PUT')
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status in [200, 201]:
                print(f"✅ Uploaded: {remote_path}")
                return True
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to upload {remote_path}: {e}")
        try:
             print(e.read().decode('utf-8'))
        except:
            pass
        return False
    except Exception as e:
        print(f"❌ Error uploading {remote_path}: {e}")
        return False
    return False

def create_repo(token, repo_name):
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = {"name": repo_name, "private": False, "description": "Photonic Computing Platform"}
    
    # Create unverified SSL context
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status == 201:
                print(f"✅ Created repository: {repo_name}")
                return True
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to create repository: {e}")
        try:
            print(e.read().decode('utf-8'))
        except:
            pass
        return False
    return False

def check_repo_exists(token, full_repo):
    url = f"{GITHUB_API_URL}/repos/{full_repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Create unverified SSL context
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            return response.status == 200
    except urllib.error.HTTPError:
        return False

def main():
    print("="*60)
    print("   Photonic Computing GitHub Uploader (No Git Required)")
    print("="*60)
    
    # Get user input
    token = input("Enter your GitHub Personal Access Token: ").strip()
    if not token:
        print("Error: Token is required.")
        return
        
    username = input("Enter your GitHub Username: ").strip()
    repo_name = input("Enter the Repository Name (e.g., photonic_computing): ").strip()
    
    full_repo = f"{username}/{repo_name}"
    
    print(f"\nChecking repository {full_repo}...")
    if not check_repo_exists(token, full_repo):
        print(f"Repository {full_repo} does not exist.")
        create = input(f"Do you want to create it now? (y/n): ").lower()
        if create == 'y':
            if not create_repo(token, repo_name):
                print("Aborting.")
                return
        else:
            print("Aborting.")
            return
    
    print(f"\nPreparing to upload to {full_repo}...")
    
    ignore_patterns = load_gitignore(PROJECT_ROOT)
    
    files_to_upload = []
    
    # Walk directory
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter directories in place
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), PROJECT_ROOT, ignore_patterns)]
        
        for file in files:
            file_path = os.path.join(root, file)
            if not is_ignored(file_path, PROJECT_ROOT, ignore_patterns):
                # Don't upload this script itself if you want, but usually it's fine
                # Don't upload .git directory if it exists
                if '.git' in file_path.split(os.sep):
                    continue
                files_to_upload.append(file_path)
    
    print(f"Found {len(files_to_upload)} files to upload.")
    confirm = input("Proceed? (y/n): ").lower()
    if confirm != 'y':
        print("Aborted.")
        return
        
    success_count = 0
    for file_path in files_to_upload:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        if upload_file(token, full_repo, file_path, rel_path):
            success_count += 1
            
    print("\n" + "="*60)
    print(f"Upload Complete. {success_count}/{len(files_to_upload)} files uploaded.")
    print(f"View your repository at: https://github.com/{full_repo}")
    print("="*60)

if __name__ == "__main__":
    main()
