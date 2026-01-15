# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: exercise_2_5_6_solution.py

import os
from collections import Counter, defaultdict

def organize_files(directory="."):
    """Organize and count files by extension"""
    
    # Get all items in directory
    items = os.listdir(directory)
    
    # Separate files from directories
    files = []
    directories = []
    
    for item in items:
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            files.append(item)
        elif os.path.isdir(path):
            directories.append(item)
    
    # Group files by extension
    file_groups = defaultdict(list)
    extension_counter = Counter()
    
    for filename in files:
        if '.' in filename:
            # Get extension
            extension = filename.split('.')[-1].lower()
            file_groups[extension].append(filename)
            extension_counter[extension] += 1
        else:
            # Files with no extension
            file_groups['no_extension'].append(filename)
            extension_counter['no_extension'] += 1
    
    # Display results
    print(f"\n📁 File Organization Report 📁")
    print("=" * 50)
    print(f"Directory: {os.path.abspath(directory)}")
    print(f"Total files: {len(files)}")
    print(f"Total directories: {len(directories)}")
    
    print("\nFiles by extension:")
    for ext, count in extension_counter.most_common():
        print(f"  .{ext}: {count} file(s)")
        # Show first 3 files of each type
        examples = file_groups[ext][:3]
        for example in examples:
            print(f"    - {example}")
        if len(file_groups[ext]) > 3:
            print(f"    ... and {len(file_groups[ext]) - 3} more")
    
    print("=" * 50)
    
    return dict(file_groups), dict(extension_counter)

# Run the organizer
groups, counts = organize_files()

# Create a summary file
import json
summary = {
    "scan_date": str(datetime.now()),
    "file_counts": counts,
    "total_files": sum(counts.values())
}

with open("file_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\n✅ Summary saved to file_summary.json")