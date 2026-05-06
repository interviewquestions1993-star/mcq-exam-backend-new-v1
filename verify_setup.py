#!/usr/bin/env python
"""
Setup verification script
Checks that all dependencies are installed and configured correctly
"""
import sys
import importlib


def check_import(package_name, display_name=None):
    """Check if a package is installed"""
    if display_name is None:
        display_name = package_name
    
    try:
        importlib.import_module(package_name)
        print(f"✓ {display_name}")
        return True
    except ImportError:
        print(f"✗ {display_name} - NOT INSTALLED")
        return False


def check_env():
    """Check environment variables"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    token = os.getenv("HF_TOKEN", "")
    if token:
        print(f"✓ HF_TOKEN configured")
        return True
    else:
        print(f"✗ HF_TOKEN - NOT CONFIGURED")
        return False


def main():
    print("\n" + "="*60)
    print("HUGGING FACE BACKEND - SETUP VERIFICATION")
    print("="*60 + "\n")
    
    print("Checking Python dependencies...\n")
    
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("requests", "Requests"),
        ("dotenv", "python-dotenv"),
    ]
    
    results = []
    for package, name in dependencies:
        results.append(check_import(package, name))
    
    print("\nChecking configuration...\n")
    results.append(check_env())
    
    print("\n" + "="*60)
    if all(results):
        print("✓ ALL CHECKS PASSED - Ready to go!")
        print("="*60)
        print("\nRun the backend with:")
        print("  python main.py")
        print("\nTest with:")
        print("  python test_api.py")
        print("\nOr visit:")
        print("  http://localhost:8000/docs")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - See above for details")
        print("="*60)
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
