import sys
import os

repo_root = r'D:\viji\erp-v23\erp-main'
sys.path.insert(0, repo_root)

print(f"Directory exists: {os.path.isdir(os.path.join(repo_root, 'Common'))}")
print(f"Contents of repo_root: {os.listdir(repo_root)}")

try:
    import Common
    print("SUCCESS: Imported Common")
except ImportError as e:
    print(f"FAILED Common: {e}")

try:
    import common
    print("SUCCESS: Imported common")
except ImportError as e:
    print(f"FAILED common: {e}")
