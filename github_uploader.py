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
import urllib.parse

def upload_file(token, repo, file_path, remote_path):
    quoted_remote_path = urllib.parse.quote(remote_path)
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{quoted_remote_path}"
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

import argparse
import sys

import time
import random

def upload_project(token, repo, root_dir, progress_callback=None, simulation=False):
    ignore_patterns = load_gitignore(root_dir)
    files_to_upload = []
    
    # Discovery phase
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), root_dir, ignore_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not is_ignored(file_path, root_dir, ignore_patterns):
                if '.git' in file_path.split(os.sep): continue
                files_to_upload.append(file_path)

    total_files = len(files_to_upload)
    if progress_callback:
        progress_callback({'status': 'discovered', 'total': total_files})

    # Creation phase
    if not simulation:
        if not check_repo_exists(token, repo):
            # Determine strict name
            repo_name = repo.split('/')[-1]
            if create_repo(token, repo_name):
                if progress_callback: progress_callback({'status': 'created_repo', 'repo': repo})
            else:
                 return {'success': False, 'message': f"Could not access or create repo {repo}"}
    else:
        # Simulate Creation
        time.sleep(1.0)
        if progress_callback: progress_callback({'status': 'created_repo', 'repo': repo})

    # Upload phase
    success_count = 0
    errors = []
    
    for i, file_path in enumerate(files_to_upload):
        rel_path = os.path.relpath(file_path, root_dir)
        
        if simulation:
            # Simulate network delay/upload
            time.sleep(random.uniform(0.05, 0.2))
            success = True
        else:
            success = upload_file(token, repo, file_path, rel_path)

        if success:
            success_count += 1
        else:
            errors.append(rel_path)
        
        if progress_callback:
            progress_callback({
                'status': 'uploading',
                'current': i + 1,
                'total': total_files,
                'file': rel_path,
                'success_count': success_count
            })
            
    return {
        'success': True,
        'total': total_files,
        'uploaded': success_count,
        'errors': errors
    }


def main():
    parser = argparse.ArgumentParser(description="Upload project to GitHub without Git client")
    parser.add_argument("--token", help="GitHub Personal Access Token")
    parser.add_argument("--repo", default="AI-lightOS/Photonic_stacking", help="Target repository (user/repo)")
    parser.add_argument("--root", default=PROJECT_ROOT, help="Project root directory")
    parser.add_argument("--simulation", action="store_true", help="Run in simulation mode (offline)")
    
    args = parser.parse_args()
    
    token = args.token
    if not args.simulation and not token:
        token = input("Enter GitHub Personal Access Token: ").strip()
        if not token:
            print("Token is required!")
            sys.exit(1)
    elif args.simulation:
        token = "dummy_token"

    print(f"🚀 Starting upload to {args.repo}...")
    if args.simulation:
        print("   (Simulation Mode Active)")

    def console_progress(data):
        if data['status'] == 'discovered':
            print(f"📁 Found {data['total']} files to upload")
        elif data['status'] == 'created_repo':
            print(f"🎉 Checked/Created repository: {data['repo']}")
        elif data['status'] == 'uploading':
            percent = (data['current'] / data['total']) * 100
            bar_len = 30
            filled_len = int(bar_len * data['current'] // data['total'])
            bar = '█' * filled_len + '-' * (bar_len - filled_len)
            sys.stdout.write(f"\r[{bar}] {percent:.1f}% | Uploading {data['file']}")
            sys.stdout.flush()

    start_time = time.time()
    result = upload_project(token, args.repo, args.root, progress_callback=console_progress, simulation=args.simulation)
    end_time = time.time()

    print("\n")
    if result['success']:
        print(f"✅ Success! Uploaded {result['uploaded']} files in {end_time - start_time:.1f}s")
        if result['errors']:
            print(f"⚠️  Errors ({len(result['errors'])}):")
            for err in result['errors']:
                print(f"  - {err}")
    else:
        print(f"❌ Failed: {result.get('message')}")

if __name__ == "__main__":
    main()
