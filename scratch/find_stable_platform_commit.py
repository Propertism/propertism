import subprocess
import os

erp_modules = ['Retail', 'CRM', 'HRM', 'FMS', 'backend', 'core', 'common']
excluded_terms = ['frontend/public', '.html', 'static/', 'explorer.html', 'index.html', 'styles/']

repo_path = r'd:\viji\viji-olivine\00current\00mindra\olivine-platform'

def get_git_log():
    # Get all commits in the range
    cmd = ['git', '-C', repo_path, 'log', 'main', '--since=2026-04-15', '--until=2026-04-21', '--oneline', '--name-only']
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
        is_erp = any(file.lower().startswith(m.lower() + '/') or ('/' + m.lower() + '/') in file.lower() for m in erp_modules)
        is_excluded = any(term in file.lower() for term in excluded_terms)
        
        if not is_erp or is_excluded:
            # Check if it's a python file or something that could be ERP core
            if file.lower().endswith('.py') and not is_excluded:
                # Might be okay
                pass
            else:
                is_erp_only = False
                break
                
    if is_erp_only:
        matches.append(header)

for m in matches:
    print(m)
