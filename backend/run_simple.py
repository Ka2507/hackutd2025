"""
Simple test to verify backend structure.
"""
import sys
from pathlib import Path

# Check all required modules exist
required_dirs = [
    "agents",
    "orchestrator",
    "integrations",
    "db",
    "utils"
]

print("Checking ProdPlex backend structure...")
print("-" * 50)

all_good = True
for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists() and dir_path.is_dir():
        print(f"[OK] {dir_name}/ directory exists")
        
        # Check for __init__.py
        init_file = dir_path / "__init__.py"
        if init_file.exists():
            print(f"  -> Has __init__.py")
        else:
            print(f"  -> Missing __init__.py")
            all_good = False
    else:
        print(f"[FAIL] {dir_name}/ directory missing")
        all_good = False

print("-" * 50)
if all_good:
    print("Backend structure looks good!")
else:
    print("Some issues found, but structure is mostly there")

# Try importing main modules
print("\nTrying to import main modules...")
try:
    from utils import config, logger
    print("[OK] utils module imported successfully")
except Exception as e:
    print(f"[FAIL] utils import failed: {e}")

try:
    from db import context_store
    print("[OK] db module imported successfully")
except Exception as e:
    print(f"[FAIL] db import failed: {e}")

print("\nBackend check complete!")
