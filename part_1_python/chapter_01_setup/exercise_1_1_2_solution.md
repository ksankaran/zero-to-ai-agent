# Exercise 1 1.2 Solution: Navigation Challenge

Using only terminal commands, complete the following tasks:

## The Challenge

1. Navigate to your Desktop
2. Create a folder called `terminal_practice`
3. Inside it, create three subfolders: `projects`, `notes`, `scripts`
4. Navigate into `scripts` and create an empty file called `test.py`
5. Navigate back to Desktop in one command

## Solution Commands

### Mac/Linux:

```bash
# Step 1: Navigate to Desktop
cd ~/Desktop

# Step 2: Create terminal_practice folder
mkdir terminal_practice

# Step 3: Navigate into it and create subfolders
cd terminal_practice
mkdir projects notes scripts

# Alternative: Create all at once
# mkdir projects && mkdir notes && mkdir scripts

# Step 4: Navigate to scripts and create test.py
cd scripts
touch test.py

# Step 5: Navigate back to Desktop in one command
cd ~/Desktop

# Verify your work
ls terminal_practice
ls terminal_practice/scripts
```

### Windows (PowerShell):

```powershell
# Step 1: Navigate to Desktop
cd ~\Desktop
# Or: cd $HOME\Desktop

# Step 2: Create terminal_practice folder
mkdir terminal_practice

# Step 3: Navigate into it and create subfolders
cd terminal_practice
mkdir projects
mkdir notes
mkdir scripts

# Step 4: Navigate to scripts and create test.py
cd scripts
New-Item test.py

# Step 5: Navigate back to Desktop in one command
cd ~\Desktop

# Verify your work
dir ..\..
dir .
```

### Windows (Command Prompt):

```cmd
# Step 1: Navigate to Desktop
cd %USERPROFILE%\Desktop

# Step 2: Create terminal_practice folder
mkdir terminal_practice

# Step 3: Navigate into it and create subfolders
cd terminal_practice
mkdir projects
mkdir notes
mkdir scripts

# Step 4: Navigate to scripts and create test.py
cd scripts
echo. > test.py

# Step 5: Navigate back to Desktop in one command
cd %USERPROFILE%\Desktop

# Verify your work
dir terminal_practice
dir terminal_practice\scripts
```

## Verification

After completing the exercise, your folder structure should look like:

```
Desktop/
└── terminal_practice/
    ├── projects/
    ├── notes/
    └── scripts/
        └── test.py
```

## Bonus Commands to Explore

```bash
# See the full tree structure (if tree is installed)
tree terminal_practice

# Alternative: Use ls with recursion
ls -R terminal_practice    # Mac/Linux
dir /s terminal_practice   # Windows

# Check you're in the right place
pwd     # Mac/Linux
cd      # Windows (just cd with no arguments shows current directory)
```

## Key Takeaways

- `cd` moves between directories
- `mkdir` creates new folders
- `touch` (Mac/Linux) or `New-Item` (PowerShell) creates files
- `~` represents your home directory
- `cd ~/Desktop` goes directly to Desktop from anywhere
- `cd ..` goes up one level
- `cd ../..` goes up two levels
