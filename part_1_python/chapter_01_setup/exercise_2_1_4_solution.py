# Save as: exercise_1_4_2_solution.py
"""
Exercise 1 4.2 Solution: Dependency Detective

This script builds and displays a dependency tree for any package.
It recursively finds all dependencies and their sub-dependencies.
"""

import subprocess
import sys


def get_package_dependencies(package_name):
    """
    Get the direct dependencies of a package using pip show.
    
    Returns:
        list: List of dependency package names, or None if package not found
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return None
        
        for line in result.stdout.split('\n'):
            if line.startswith('Requires:'):
                requires = line.split(':', 1)[1].strip()
                if requires:
                    # Split by comma and clean up
                    deps = [d.strip() for d in requires.split(',')]
                    return [d for d in deps if d]  # Filter empty strings
                return []
        
        return []
    except Exception as e:
        print(f"Error getting dependencies for {package_name}: {e}")
        return None


def build_dependency_tree(package_name, visited=None, depth=0, max_depth=5):
    """
    Recursively build a dependency tree.
    
    Args:
        package_name: Name of the package to analyze
        visited: Set of already-visited packages (to avoid cycles)
        depth: Current recursion depth
        max_depth: Maximum depth to prevent infinite recursion
    
    Returns:
        dict: Tree structure with package info
    """
    if visited is None:
        visited = set()
    
    # Avoid cycles and excessive depth
    if package_name.lower() in visited or depth > max_depth:
        return {'name': package_name, 'dependencies': [], 'cyclic': package_name.lower() in visited}
    
    visited.add(package_name.lower())
    
    dependencies = get_package_dependencies(package_name)
    
    if dependencies is None:
        return {'name': package_name, 'dependencies': [], 'not_installed': True}
    
    tree = {
        'name': package_name,
        'dependencies': []
    }
    
    for dep in dependencies:
        subtree = build_dependency_tree(dep, visited.copy(), depth + 1, max_depth)
        tree['dependencies'].append(subtree)
    
    return tree


def print_tree(tree, prefix="", is_last=True, show_status=True):
    """
    Pretty-print the dependency tree.
    
    Args:
        tree: The dependency tree structure
        prefix: Current line prefix for indentation
        is_last: Whether this is the last item at this level
        show_status: Whether to show installation status indicators
    """
    # Determine the connector
    connector = "└── " if is_last else "├── "
    
    # Build status indicator
    status = ""
    if show_status:
        if tree.get('not_installed'):
            status = " ❌ (not installed)"
        elif tree.get('cyclic'):
            status = " 🔄 (circular ref)"
    
    # Print this node
    print(f"{prefix}{connector}{tree['name']}{status}")
    
    # Update prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    # Print children
    dependencies = tree.get('dependencies', [])
    for i, dep in enumerate(dependencies):
        is_last_child = (i == len(dependencies) - 1)
        print_tree(dep, child_prefix, is_last_child, show_status)


def count_dependencies(tree, seen=None):
    """Count total unique dependencies in the tree."""
    if seen is None:
        seen = set()
    
    seen.add(tree['name'].lower())
    
    for dep in tree.get('dependencies', []):
        count_dependencies(dep, seen)
    
    return len(seen) - 1  # Subtract 1 for the root package


def main():
    """Main function to run the dependency detective."""
    
    print("=" * 60)
    print("🔍 DEPENDENCY DETECTIVE")
    print("=" * 60)
    print("\nThis tool shows the complete dependency tree for any package.")
    
    # Get package name from command line or prompt
    if len(sys.argv) > 1:
        package_name = sys.argv[1]
    else:
        print("\nEnter a package name to investigate (or 'quit' to exit)")
        package_name = input("\nPackage name: ").strip()
    
    if not package_name or package_name.lower() == 'quit':
        print("Goodbye!")
        return
    
    print(f"\n🔎 Investigating: {package_name}")
    print("-" * 60)
    
    # Check if package is installed
    deps = get_package_dependencies(package_name)
    
    if deps is None:
        print(f"\n❌ Package '{package_name}' is not installed.")
        print(f"   Install it with: pip install {package_name}")
        return
    
    # Build and display the tree
    print(f"\n📦 Dependency Tree for '{package_name}':")
    print()
    
    tree = build_dependency_tree(package_name)
    
    # Print root package name
    print(f"📦 {package_name}")
    
    # Print dependencies
    dependencies = tree.get('dependencies', [])
    if dependencies:
        for i, dep in enumerate(dependencies):
            is_last = (i == len(dependencies) - 1)
            print_tree(dep, "", is_last)
    else:
        print("   └── (no dependencies)")
    
    # Summary
    total_deps = count_dependencies(tree)
    direct_deps = len(dependencies)
    
    print("\n" + "-" * 60)
    print("📊 Summary:")
    print(f"   Direct dependencies: {direct_deps}")
    print(f"   Total dependencies (including nested): {total_deps}")
    
    # List all unique dependencies
    if total_deps > 0:
        print("\n📋 All dependencies (flat list):")
        all_deps = set()
        
        def collect_deps(t):
            for d in t.get('dependencies', []):
                all_deps.add(d['name'])
                collect_deps(d)
        
        collect_deps(tree)
        
        for dep in sorted(all_deps):
            print(f"   • {dep}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
