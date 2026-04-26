import os

start_path = r'd:\viji\viji-olivine'
for root, dirs, files in os.walk(start_path):
    if 'workflows' in dirs:
        print(os.path.join(root, 'workflows'))
