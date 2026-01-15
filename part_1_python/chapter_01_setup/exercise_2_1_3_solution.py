# Save as: exercise_2_1_3_solution.py
"""
Exercise 2 1.3 Solution: Environment Inspector

This script reports comprehensive information about your current
Python environment, helping you understand virtual environments.
"""

import sys
import os
import subprocess


def check_virtual_environment():
    """Check if running inside a virtual environment."""
    # Method 1: Check if base_prefix differs from prefix
    in_venv = hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    
    # Method 2: Check for VIRTUAL_ENV environment variable
    venv_path = os.environ.get('VIRTUAL_ENV')
    
    return in_venv, venv_path


def get_python_info():
    """Get Python version and executable location."""
    return {
        'version': sys.version,
        'version_info': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'executable': sys.executable,
        'prefix': sys.prefix,
        'base_prefix': getattr(sys, 'base_prefix', sys.prefix)
    }


def get_installed_packages():
    """Get list of installed packages using pip."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=json'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            import json
            packages = json.loads(result.stdout)
            return packages
    except Exception as e:
        print(f"Error getting packages: {e}")
    return []


def get_package_sizes():
    """Estimate total size of installed packages."""
    # Get site-packages directory
    import site
    site_packages = site.getsitepackages()
    
    total_size = 0
    for sp in site_packages:
        if os.path.exists(sp):
            for dirpath, dirnames, filenames in os.walk(sp):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        pass
    
    return total_size


def format_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def main():
    """Main function to display environment information."""
    print("=" * 60)
    print("🔍 PYTHON ENVIRONMENT INSPECTOR")
    print("=" * 60)
    
    # Check virtual environment status
    in_venv, venv_path = check_virtual_environment()
    print("\n📦 Virtual Environment Status:")
    print("-" * 40)
    if in_venv:
        print("✅ Running INSIDE a virtual environment")
        if venv_path:
            print(f"   Environment path: {venv_path}")
    else:
        print("⚠️  Running in SYSTEM Python (not a virtual environment)")
        print("   Consider activating a virtual environment!")
    
    # Python information
    py_info = get_python_info()
    print("\n🐍 Python Information:")
    print("-" * 40)
    print(f"   Version: {py_info['version_info']}")
    print(f"   Full version: {py_info['version'].split()[0]}")
    print(f"   Executable: {py_info['executable']}")
    print(f"   Prefix: {py_info['prefix']}")
    if py_info['prefix'] != py_info['base_prefix']:
        print(f"   Base prefix: {py_info['base_prefix']}")
    
    # Installed packages
    packages = get_installed_packages()
    print("\n📚 Installed Packages:")
    print("-" * 40)
    print(f"   Total packages: {len(packages)}")
    
    if packages:
        print("\n   Package List:")
        # Sort by name and display
        for pkg in sorted(packages, key=lambda x: x['name'].lower()):
            print(f"   • {pkg['name']} ({pkg['version']})")
    
    # Package sizes
    print("\n💾 Storage Information:")
    print("-" * 40)
    total_size = get_package_sizes()
    print(f"   Total size of installed packages: {format_size(total_size)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"   Environment: {'Virtual' if in_venv else 'System'}")
    print(f"   Python: {py_info['version_info']}")
    print(f"   Packages: {len(packages)}")
    print(f"   Size: {format_size(total_size)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
