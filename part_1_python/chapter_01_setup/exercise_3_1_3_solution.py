# Save as: exercise_3_1_3_solution.py
"""
Exercise 3 1.3 Solution: Requirements Comparison

This script compares two requirements.txt files and shows:
- Packages unique to each environment
- Packages with different versions
- Packages that are identical
"""

import sys
from pathlib import Path


def parse_requirements(filepath):
    """
    Parse a requirements.txt file into a dictionary.
    
    Returns: dict of {package_name: version}
    """
    packages = {}
    
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return packages
    
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Handle different formats:
            # package==version
            # package>=version
            # package~=version
            # package (no version)
            
            if '==' in line:
                name, version = line.split('==', 1)
            elif '>=' in line:
                name, version = line.split('>=', 1)
                version = f">={version}"
            elif '~=' in line:
                name, version = line.split('~=', 1)
                version = f"~={version}"
            elif '<=' in line:
                name, version = line.split('<=', 1)
                version = f"<={version}"
            else:
                name = line
                version = "any"
            
            # Normalize package name (lowercase, replace underscores)
            name = name.lower().replace('_', '-').strip()
            packages[name] = version.strip()
    
    return packages


def compare_requirements(file1, file2):
    """
    Compare two requirements files and categorize differences.
    
    Returns: dict with 'only_in_first', 'only_in_second', 
             'different_versions', 'identical'
    """
    pkgs1 = parse_requirements(file1)
    pkgs2 = parse_requirements(file2)
    
    if not pkgs1 and not pkgs2:
        return None
    
    names1 = set(pkgs1.keys())
    names2 = set(pkgs2.keys())
    
    # Find unique packages
    only_in_first = names1 - names2
    only_in_second = names2 - names1
    
    # Find common packages
    common = names1 & names2
    
    # Categorize common packages
    different_versions = {}
    identical = {}
    
    for name in common:
        v1 = pkgs1[name]
        v2 = pkgs2[name]
        
        if v1 == v2:
            identical[name] = v1
        else:
            different_versions[name] = {'file1': v1, 'file2': v2}
    
    return {
        'only_in_first': {name: pkgs1[name] for name in only_in_first},
        'only_in_second': {name: pkgs2[name] for name in only_in_second},
        'different_versions': different_versions,
        'identical': identical,
        'file1_total': len(pkgs1),
        'file2_total': len(pkgs2)
    }


def print_comparison(results, name1="File 1", name2="File 2"):
    """Pretty print the comparison results."""
    
    if results is None:
        print("❌ Could not compare files (one or both may be missing)")
        return
    
    print("=" * 60)
    print("📊 REQUIREMENTS COMPARISON REPORT")
    print("=" * 60)
    
    print(f"\n📁 {name1}: {results['file1_total']} packages")
    print(f"📁 {name2}: {results['file2_total']} packages")
    
    # Packages only in first file
    only1 = results['only_in_first']
    print(f"\n🔵 Packages ONLY in {name1}: ({len(only1)})")
    print("-" * 40)
    if only1:
        for name, version in sorted(only1.items()):
            print(f"   • {name} == {version}")
    else:
        print("   (none)")
    
    # Packages only in second file
    only2 = results['only_in_second']
    print(f"\n🟢 Packages ONLY in {name2}: ({len(only2)})")
    print("-" * 40)
    if only2:
        for name, version in sorted(only2.items()):
            print(f"   • {name} == {version}")
    else:
        print("   (none)")
    
    # Different versions
    diff = results['different_versions']
    print(f"\n🟡 Packages with DIFFERENT versions: ({len(diff)})")
    print("-" * 40)
    if diff:
        for name, versions in sorted(diff.items()):
            print(f"   • {name}")
            print(f"     {name1}: {versions['file1']}")
            print(f"     {name2}: {versions['file2']}")
    else:
        print("   (none)")
    
    # Identical packages
    same = results['identical']
    print(f"\n✅ IDENTICAL packages: ({len(same)})")
    print("-" * 40)
    if same:
        for name, version in sorted(same.items()):
            print(f"   • {name} == {version}")
    else:
        print("   (none)")
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    print(f"   Only in {name1}: {len(only1)}")
    print(f"   Only in {name2}: {len(only2)}")
    print(f"   Different versions: {len(diff)}")
    print(f"   Identical: {len(same)}")
    print("=" * 60)


def create_sample_files():
    """Create sample requirements files for testing."""
    
    # Sample file 1 - AI/ML focused
    sample1 = """# AI Project Requirements
numpy==1.21.0
pandas==1.3.0
requests==2.28.0
openai==0.27.0
langchain==0.0.200
python-dotenv==1.0.0
"""
    
    # Sample file 2 - Updated versions + different packages
    sample2 = """# Updated AI Project Requirements  
numpy==1.24.0
pandas==2.0.0
requests==2.28.0
openai==1.0.0
tiktoken==0.5.0
httpx==0.25.0
python-dotenv==1.0.0
"""
    
    with open('requirements_old.txt', 'w') as f:
        f.write(sample1)
    
    with open('requirements_new.txt', 'w') as f:
        f.write(sample2)
    
    print("✅ Created sample files: requirements_old.txt, requirements_new.txt")


def main():
    """Main function to run the comparison."""
    
    print("🔍 Requirements File Comparator")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) == 3:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    elif len(sys.argv) == 2 and sys.argv[1] == '--demo':
        # Create and compare sample files
        print("\n📝 Demo mode: Creating sample files...")
        create_sample_files()
        file1 = 'requirements_old.txt'
        file2 = 'requirements_new.txt'
    else:
        print("\nUsage:")
        print("  python exercise_1_3_3_solution.py <file1> <file2>")
        print("  python exercise_1_3_3_solution.py --demo")
        print("\nExample:")
        print("  python exercise_1_3_3_solution.py requirements_old.txt requirements_new.txt")
        return
    
    # Run comparison
    print(f"\n📂 Comparing:")
    print(f"   File 1: {file1}")
    print(f"   File 2: {file2}")
    
    results = compare_requirements(file1, file2)
    print_comparison(results, Path(file1).name, Path(file2).name)


if __name__ == "__main__":
    main()
