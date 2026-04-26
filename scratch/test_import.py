import sys
import os

repo_root = r'D:\viji\erp-v23\erp-main'
sys.path.insert(0, repo_root)

try:
    import Common
    print("SUCCESS: Imported Common")
    import Common.domain
    print("SUCCESS: Imported Common.domain")
except ImportError as e:
    print(f"FAILED: {e}")

print("Path entries:")
for p in sys.path:
    print(f"  {p}")
