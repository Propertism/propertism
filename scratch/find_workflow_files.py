import os

start_path = r'd:\viji\viji-olivine\00current\00mindra\olivine-platform'
for root, dirs, files in os.walk(start_path):
    for file in files:
        if 'workflow' in file.lower() and file.endswith('.md'):
            print(os.path.join(root, file))
