import subprocess
import os

erp_modules = ['Retail', 'CRM', 'HRM', 'FMS', 'backend', 'core', 'common']
excluded_terms = ['frontend/public', '.html', 'static/', 'explorer.html', 'index.html', 'styles/']

repo_path = r'D:\viji\erp-v23\erp-master'

def get_git_log():
    # Get last 1000 commits
    cmd = ['git', '-C', repo_path, 'log', '--all', '--oneline', '--name-only', '-n', '1000']
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
        is_erp = any(file.lower().startswith(m.lower() + '/') for m in erp_modules)
        is_excluded = any(term in file.lower() for term in excluded_terms)
        
        if not is_erp or is_excluded:
            is_erp_only = False
            break
            
    if is_erp_only:
        matches.append(header)

for m in matches[:10]:
    print(m)
