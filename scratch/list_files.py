import os

root_dir = r'D:\viji\erp-v23\erp-master'
output_file = r'D:\viji\erp-v23\erp-master\all_filenames.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Get relative path from root_dir
            rel_path = os.path.relpath(os.path.join(root, file), root_dir)
            f.write(rel_path + '\n')
