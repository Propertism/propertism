import os

start_path = r'd:\viji\viji-olivine'
for root, dirs, files in os.walk(start_path):
    if 'workflows' in dirs:
        full_path = os.path.join(root, 'workflows')
        if '.github' not in full_path:
            print(full_path)
