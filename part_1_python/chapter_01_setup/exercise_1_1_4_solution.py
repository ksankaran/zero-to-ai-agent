# Save as: exercise_1_1_4_solution.py
"""
Exercise 1.4.1 Solution: Package Explorer

This script explores your Python environment and checks which
packages are installed and working.
"""

import sys
import subprocess


def check_package(package_name, import_name=None):
    """
    Check if a package is installed and can be imported.
    
    Args:
        package_name: Name as shown in pip (e.g., 'beautifulsoup4')
        import_name: Name used for import (e.g., 'bs4'), defaults to package_name
    
    Returns:
        tuple: (is_installed, version_or_error)
    """
    if import_name is None:
        import_name = package_name
    
    try:
        # Try to import the package
        module = __import__(import_name)
        
        # Try to get version
        version = getattr(module, '__version__', 'unknown')
        
        return True, version
    except ImportError as e:
        return False, str(e)


def get_pip_info(package_name):
    """Get detailed info about a package using pip show."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            info = {}
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            return info
    except Exception:
        pass
    return None


def main():
    """Main function to explore installed packages."""
    
    print("=" * 60)
    print("🔍 PYTHON PACKAGE EXPLORER")
    print("=" * 60)
    
    # List of packages to check
    # Format: (pip_name, import_name, description)
    packages_to_check = [
        ('requests', 'requests', 'HTTP library for API calls'),
        ('colorama', 'colorama', 'Cross-platform colored terminal text'),
        ('rich', 'rich', 'Beautiful terminal formatting'),
        ('numpy', 'numpy', 'Numerical computing'),
        ('pandas', 'pandas', 'Data manipulation'),
        ('openai', 'openai', 'OpenAI API client'),
        ('python-dotenv', 'dotenv', 'Environment variable management'),
        ('beautifulsoup4', 'bs4', 'HTML/XML parsing'),
        ('pillow', 'PIL', 'Image processing'),
        ('matplotlib', 'matplotlib', 'Data visualization'),
    ]
    
    print("\n📦 Checking Common Packages:")
    print("-" * 60)
    
    installed_count = 0
    missing_count = 0
    
    for pip_name, import_name, description in packages_to_check:
        is_installed, version = check_package(pip_name, import_name)
        
        if is_installed:
            installed_count += 1
            print(f"✅ {pip_name:20} v{version:15} - {description}")
        else:
            missing_count += 1
            print(f"❌ {pip_name:20} {'NOT INSTALLED':15} - {description}")
    
    # Summary
    print("\n" + "-" * 60)
    print(f"📊 Summary: {installed_count} installed, {missing_count} missing")
    
    # Show details for installed packages
    print("\n" + "=" * 60)
    print("📋 DETAILED PACKAGE INFO")
    print("=" * 60)
    
    for pip_name, import_name, description in packages_to_check:
        is_installed, _ = check_package(pip_name, import_name)
        
        if is_installed:
            info = get_pip_info(pip_name)
            if info:
                print(f"\n🔹 {pip_name}")
                print(f"   Version: {info.get('Version', 'unknown')}")
                print(f"   Location: {info.get('Location', 'unknown')}")
                requires = info.get('Requires', '')
                if requires:
                    print(f"   Requires: {requires}")
    
    # Installation suggestions
    if missing_count > 0:
        print("\n" + "=" * 60)
        print("💡 INSTALLATION SUGGESTIONS")
        print("=" * 60)
        print("\nTo install missing packages, run:")
        print()
        for pip_name, import_name, description in packages_to_check:
            is_installed, _ = check_package(pip_name, import_name)
            if not is_installed:
                print(f"   pip install {pip_name}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
