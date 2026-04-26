import subprocess
import os

erp_modules = ['Retail', 'CRM', 'HRM', 'FMS', 'backend', 'core', 'common']
excluded_terms = ['frontend/public', '.html', 'static/', 'explorer.html', 'index.html', 'styles/']

repo_path = r'D:\viji\erp-v23\erp-master'

def get_git_log():
    # Get all commits
    cmd = ['git', '-C', repo_path, 'log', '--all', '--oneline', '--name-only', '-n', '500']
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

matches = []

for commit in commits:
    header = commit['header']
    files = commit['files']
    
    only_erp = True
    no_excluded = True
    
    if not files:
        continue
        
    for file in files:
        is_erp = any(file.lower().startswith(m.lower() + '/') or ('/' + m.lower() + '/') in file.lower() for m in erp_modules)
        
        if not is_erp:
            # Check if it's a documentation file or something safe
            if any(term in file.lower() for term in ['.md', '.txt', '.py', 'scripts/']):
                # If it's a script or md, we might allow it if it's erp related, but the user said "only contains ERP modules"
                # Let's be strict first.
                only_erp = False
                break
            else:
                only_erp = False
                break
            
        if any(term in file.lower() for term in excluded_terms):
            no_excluded = False
            break
            
    if only_erp and no_excluded:
        matches.append(header)

for m in matches[:10]:
    print(m)
