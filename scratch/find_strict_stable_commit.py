import subprocess
import os

erp_modules = ['Retail', 'CRM', 'HRM', 'FMS', 'backend', 'core', 'common']
excluded_folders = ['frontend/public', 'static/', 'explore-assets/', '.agent/', '.github/']
excluded_extensions = ['.html', '.css', '.jpg', '.png', '.svg', '.json', '.bat', '.ps1']

repo_path = r'D:\viji\erp-v23\erp-master'

def get_git_log():
    # Get all commits in the range or near it
    cmd = ['git', '-C', repo_path, 'log', '--all', '--since=2026-04-01', '--oneline', '--name-only']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

log_output = get_git_log()

commits = []
current_commit = None

for line in log_output.splitlines():
    if not line.strip():
        continue
    
    parts = line.split()
    if parts and all(c in '0123456789abcdef' for c in parts[0]):
        current_commit = {'header': line, 'files': []}
        commits.append(current_commit)
    elif current_commit:
        current_commit['files'].append(line)

matches = []

for commit in commits:
    header = commit['header']
    files = commit['files']
    
    if not files:
        continue
        
    is_erp_only = True
    for file in files:
        # Check if file is in an ERP module
        is_erp = any(file.lower().startswith(m.lower() + '/') for m in erp_modules)
        
        # Check if it's in an excluded folder
        is_excluded_folder = any(term in file.lower() for term in excluded_folders)
        
        # Check if it has an excluded extension
        is_excluded_ext = any(file.lower().endswith(ext) for ext in excluded_extensions)
        
        if not is_erp or is_excluded_folder or is_excluded_ext:
            # Check if it's a python file or something that could be ERP core but not in a module folder
            if file.lower().endswith('.py') and not is_excluded_folder:
                # Might be okay, but let's be strict
                is_erp_only = False
                break
            else:
                is_erp_only = False
                break
                
    if is_erp_only:
        matches.append(header)

for m in matches:
    print(m)
