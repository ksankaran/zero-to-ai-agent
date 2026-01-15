# Exercise 1 1.3 Solution: Multi-Environment Project

This exercise demonstrates how virtual environments isolate package versions.

## Step-by-Step Commands

### Project 1: Old NumPy Version

```bash
# Navigate to Desktop
cd ~/Desktop  # Mac/Linux
cd Desktop    # Windows

# Create and enter project folder
mkdir project_old
cd project_old

# Create virtual environment
python -m venv venv_old

# Activate (choose your OS)
# Windows PowerShell:
.\venv_old\Scripts\Activate.ps1
# Windows CMD:
venv_old\Scripts\activate.bat
# Mac/Linux:
source venv_old/bin/activate

# Install specific old version
pip install numpy==1.21.0

# Verify the version
python -c "import numpy; print(f'Project 1 NumPy: {numpy.__version__}')"
# Output: Project 1 NumPy: 1.21.0

# Save requirements
pip freeze > requirements.txt

# Deactivate
deactivate
```

### Project 2: Latest NumPy Version

```bash
# Go back to Desktop
cd ..

# Create and enter project folder
mkdir project_new
cd project_new

# Create virtual environment
python -m venv venv_new

# Activate (choose your OS)
# Windows PowerShell:
.\venv_new\Scripts\Activate.ps1
# Windows CMD:
venv_new\Scripts\activate.bat
# Mac/Linux:
source venv_new/bin/activate

# Install latest version
pip install numpy

# Verify the version
python -c "import numpy; print(f'Project 2 NumPy: {numpy.__version__}')"
# Output: Project 2 NumPy: 2.x.x (latest version)

# Save requirements
pip freeze > requirements.txt

# Deactivate
deactivate
```

## Verification Script

Create this file to verify both environments:

```python
# Save as: verify_environments.py
import subprocess
import os

def check_numpy_version(env_path, project_name):
    """Activate an environment and check numpy version."""
    if os.name == 'nt':  # Windows
        python_path = os.path.join(env_path, 'Scripts', 'python.exe')
    else:  # Mac/Linux
        python_path = os.path.join(env_path, 'bin', 'python')
    
    result = subprocess.run(
        [python_path, '-c', 'import numpy; print(numpy.__version__)'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"{project_name}: NumPy {result.stdout.strip()}")
    else:
        print(f"{project_name}: Error - {result.stderr}")

# Check both projects
check_numpy_version('../project_old/venv_old', 'Project Old')
check_numpy_version('../project_new/venv_new', 'Project New')
```

## Expected Output

```
Project Old: NumPy 1.21.0
Project New: NumPy 2.1.0
```

## Key Takeaways

1. **Isolation works**: Each project has its own NumPy version
2. **No conflicts**: Installing in one environment doesn't affect the other
3. **requirements.txt**: Each project documents its exact dependencies
4. **Professional workflow**: This is how real projects manage dependencies
