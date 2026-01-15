# Save as: exercise_3_1_4_solution.py
"""
Exercise 3 1.4 Solution: Version Manager

This script reads requirements.txt, checks for updates, and warns
about major version changes.
"""

import subprocess
import sys
import re
from pathlib import Path


def parse_requirements(filepath='requirements.txt'):
    """
    Parse a requirements.txt file.
    
    Returns:
        list: List of tuples (package_name, current_version, version_spec)
    """
    packages = []
    path = Path(filepath)
    
    if not path.exists():
        return None
    
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse package==version format
            match = re.match(r'^([a-zA-Z0-9_-]+)\s*([<>=~!]+)?\s*([0-9.]+)?', line)
            
            if match:
                name = match.group(1)
                spec = match.group(2) or '=='
                version = match.group(3) or 'any'
                packages.append((name, version, spec))
    
    return packages


def get_installed_version(package_name):
    """Get the currently installed version of a package."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return None


def get_latest_version(package_name):
    """Get the latest available version from PyPI."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'index', 'versions', package_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Parse the output to find the latest version
            # Format: "package_name (x.y.z)"
            match = re.search(r'\(([0-9.]+)\)', result.stdout)
            if match:
                return match.group(1)
        
        # Fallback: use pip install --dry-run
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', f'{package_name}==999.999.999'],
            capture_output=True,
            text=True
        )
        
        # The error message contains available versions
        match = re.search(r'from versions: ([^)]+)\)', result.stderr)
        if match:
            versions = match.group(1).split(', ')
            # Filter and return the latest
            valid_versions = [v.strip() for v in versions if re.match(r'^[0-9.]+$', v.strip())]
            if valid_versions:
                return valid_versions[-1]
                
    except Exception as e:
        pass
    
    return None


def parse_version(version_str):
    """Parse a version string into comparable tuple."""
    if not version_str or version_str == 'any':
        return (0, 0, 0)
    
    try:
        parts = version_str.split('.')
        return tuple(int(p) for p in parts[:3])
    except (ValueError, AttributeError):
        return (0, 0, 0)


def is_major_upgrade(current, latest):
    """Check if updating would be a major version change."""
    current_parts = parse_version(current)
    latest_parts = parse_version(latest)
    
    if current_parts[0] != latest_parts[0]:
        return True
    return False


def is_minor_upgrade(current, latest):
    """Check if updating would be a minor version change."""
    current_parts = parse_version(current)
    latest_parts = parse_version(latest)
    
    if current_parts[0] == latest_parts[0] and current_parts[1] != latest_parts[1]:
        return True
    return False


def main():
    """Main function to check for package updates."""
    
    print("=" * 70)
    print("📦 VERSION MANAGER - Package Update Checker")
    print("=" * 70)
    
    # Get requirements file path
    if len(sys.argv) > 1:
        requirements_file = sys.argv[1]
    else:
        requirements_file = 'requirements.txt'
    
    print(f"\n📄 Reading: {requirements_file}")
    
    # Parse requirements
    packages = parse_requirements(requirements_file)
    
    if packages is None:
        print(f"\n❌ File not found: {requirements_file}")
        print("\nTo create a requirements.txt file:")
        print("   pip freeze > requirements.txt")
        return
    
    if not packages:
        print("\n⚠️  No packages found in requirements file")
        return
    
    print(f"   Found {len(packages)} packages to check\n")
    print("-" * 70)
    print(f"{'Package':<25} {'Current':<12} {'Latest':<12} {'Status':<15}")
    print("-" * 70)
    
    # Track statistics
    up_to_date = 0
    minor_updates = 0
    major_updates = 0
    not_found = 0
    
    updates_available = []
    
    for name, req_version, spec in packages:
        # Get installed version
        installed = get_installed_version(name)
        
        # Get latest version
        latest = get_latest_version(name)
        
        # Determine status
        if installed is None:
            status = "❌ Not installed"
            not_found += 1
            current_display = "---"
            latest_display = latest or "???"
        elif latest is None:
            status = "⚠️  Can't check"
            current_display = installed
            latest_display = "???"
        elif installed == latest:
            status = "✅ Up to date"
            up_to_date += 1
            current_display = installed
            latest_display = latest
        elif is_major_upgrade(installed, latest):
            status = "🔴 MAJOR update"
            major_updates += 1
            current_display = installed
            latest_display = latest
            updates_available.append((name, installed, latest, 'major'))
        elif is_minor_upgrade(installed, latest):
            status = "🟡 Minor update"
            minor_updates += 1
            current_display = installed
            latest_display = latest
            updates_available.append((name, installed, latest, 'minor'))
        else:
            status = "🟢 Patch update"
            current_display = installed
            latest_display = latest
            updates_available.append((name, installed, latest, 'patch'))
        
        print(f"{name:<25} {current_display:<12} {latest_display:<12} {status}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"   ✅ Up to date:     {up_to_date}")
    print(f"   🟢 Patch updates:  {len([u for u in updates_available if u[3] == 'patch'])}")
    print(f"   🟡 Minor updates:  {minor_updates}")
    print(f"   🔴 Major updates:  {major_updates}")
    print(f"   ❌ Not installed:  {not_found}")
    
    # Warnings for major updates
    if major_updates > 0:
        print("\n" + "=" * 70)
        print("⚠️  MAJOR VERSION WARNINGS")
        print("=" * 70)
        print("The following packages have major version updates available.")
        print("Major updates may contain breaking changes!\n")
        
        for name, current, latest, update_type in updates_available:
            if update_type == 'major':
                print(f"   🔴 {name}: {current} → {latest}")
                print(f"      Review changelog before updating!")
    
    # Update commands
    if updates_available:
        print("\n" + "=" * 70)
        print("💡 UPDATE COMMANDS")
        print("=" * 70)
        
        # Safe updates (patches only)
        patches = [u for u in updates_available if u[3] == 'patch']
        if patches:
            print("\n🟢 Safe updates (patches):")
            for name, current, latest, _ in patches:
                print(f"   pip install --upgrade {name}")
        
        # Minor updates
        minors = [u for u in updates_available if u[3] == 'minor']
        if minors:
            print("\n🟡 Minor updates (test after updating):")
            for name, current, latest, _ in minors:
                print(f"   pip install --upgrade {name}")
        
        # Major updates
        majors = [u for u in updates_available if u[3] == 'major']
        if majors:
            print("\n🔴 Major updates (review changelog first!):")
            for name, current, latest, _ in majors:
                print(f"   pip install {name}=={latest}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
