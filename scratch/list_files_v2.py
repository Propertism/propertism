import os

root_dir = r'D:\viji\erp-v23\erp-master'
output_file = r'd:\viji\viji-olivine\03rolledout\01propertism\all_erp_filenames.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for root, dirs, files in os.walk(root_dir):
        # Exclude .git folder
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), root_dir)
            f.write(rel_path + '\n')
