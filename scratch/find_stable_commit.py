import subprocess
import os

erp_modules = ['Retail', 'CRM', 'HRM', 'FMS', 'backend', 'core', 'common']
excluded_terms = ['frontend/public', '.html', 'static/', 'explorer.html', 'index.html', 'styles/']

repo_path = r'D:\viji\erp-v23\erp-master'

def get_git_log():
    # Get commits on main between the dates
    cmd = ['git', '-C', repo_path, 'log', 'origin/main', '--since=2026-04-15', '--until=2026-04-21', '--oneline', '--name-only']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

log_output = get_git_log()

commits = []
current_commit = None

for line in log_output.splitlines():
    if not line.strip():
        continue
    
    # Check if it's a commit line (starts with hex string)
    parts = line.split()
    if parts and all(c in '0123456789abcdef' for c in parts[0]):
        current_commit = {'header': line, 'files': []}
        commits.append(current_commit)
    elif current_commit:
        current_commit['files'].append(line)

stable_commit = None

for commit in commits:
    header = commit['header']
    files = commit['files']
    
    # Condition: ONLY ERP modules, NO excluded files
    only_erp = True
    no_excluded = True
    
    if not files:
        continue
        
    for file in files:
        # Check if file is part of erp modules
        is_erp = any(file.lower().startswith(m.lower() + '/') or ('/' + m.lower() + '/') in file.lower() for m in erp_modules)
        
        if not is_erp:
            only_erp = False
            break
            
        # Check for excluded terms
        if any(term in file.lower() for term in excluded_terms):
            no_excluded = False
            break
            
    if only_erp and no_excluded:
        stable_commit = header
        break

if stable_commit:
    print(f"LAST_STABLE_COMMIT: {stable_commit}")
else:
    print("No stable commit found matching criteria.")
